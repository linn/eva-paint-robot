#!/usr/bin/env python3
""" Supporting module for controlling a pair of robots """
from evasdk import Eva, RobotState, EvaError


class EvaPair:
    """ Class to support a pair of robots """
    def __init__(self, robot_l: Eva, robot_r: Eva):
        self.robot_pair = [robot_l, robot_r]
        self.reset_attempts = 3

    def check_and_reset_state(self, eva: Eva, recur_count: int = 0) -> None:
        """ Checks and resets the state of Eva, must be called under with eva.lock() """
        eva_name = eva.name()['name']
        eva_state = eva.data_snapshot_property('control')['state']
        if eva_state == RobotState.READY.value:
            pass
        elif eva_state == RobotState.RUNNING.value:
            eva.control_stop_loop(wait_for_ready=True)
        elif eva_state == RobotState.ERROR.value and recur_count < self.reset_attempts:
            print(f"{eva_name}: Attempt number {recur_count + 1} to reset...")
            eva.control_reset_errors()
            self.check_and_reset_state(eva, recur_count=(recur_count + 1))
        elif eva_state == RobotState.DISABLED.value:
            raise EvaError(f"Unable to reset robot {eva_name} - CHECK E-STOP")
        elif eva_state == RobotState.ERROR.value and recur_count == self.reset_attempts:
            raise EvaError(f"Unable to reset robot: {eva.name}")

    def check_in_ready_state(self, eva: Eva) -> None:
        """ Checks whether the robot is in READY state """
        eva_name = eva.name()['name']
        eva_state = eva.data_snapshot_property('control')['state']
        if eva_state == RobotState.READY.value:
            print(f"{eva_name}: READY TO RUN")
        else:
            with eva.lock():
                self.check_and_reset_state(eva)

    def send_home_pair(self) -> None:
        """ Sends both robots to the home position of the toolpath active """
        for eva in self.robot_pair:
            with eva.lock():
                self.check_and_reset_state(eva)
        for eva in self.robot_pair:
            with eva.lock():
                print(f"{eva.name()['name']}: SENDING HOME")
                eva.control_home(wait_for_ready=True)

    def run_toolpath_pair(self) -> None:
        """ Runs both robots """
        for eva in self.robot_pair:
            self.check_in_ready_state(eva)
        for eva in self.robot_pair:
            with eva.lock():
                print(f"{eva.name()['name']}: STARTING TOOLPATH")
                eva.control_run(loop=0, wait_for_ready=False, mode='automatic')

    def stop_toolpath_pair(self) -> None:
        """ Stops both robots providing they are running """
        for eva in self.robot_pair:
            eva_state = eva.data_snapshot_property('control')['state']
            if eva_state == RobotState.RUNNING.value:
                with eva.lock():
                    eva.control_stop_loop(wait_for_ready=True)
