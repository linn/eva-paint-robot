from evasdk import Eva, RobotState, EvaError


class EvaPair:
    def __init__(self, robot_l: Eva, robot_r: Eva):
        self.robot_pair = [robot_l, robot_r]
        self.reset_attempts = 3

    def check_and_reset_state(self, eva: Eva, recur_count: int = 0) -> bool:
        eva_name = eva.name()['name']
        eva_state = eva.data_snapshot_property('control')['state']
        if eva_state == RobotState.READY.value:
            return True
        elif eva_state == RobotState.RUNNING.value:
            eva.control_stop_loop(wait_for_ready=True)
            return True
        elif eva_state == RobotState.ERROR.value and recur_count < self.reset_attempts:
            print(f"{eva_name}: Attempt number {recur_count + 1} to reset...")
            eva.control_reset_errors()
            self.check_and_reset_state(eva, recur_count=(recur_count + 1))
        elif eva_state == RobotState.DISABLED.value:
            raise EvaError(f"Unable to reset robot {eva_name} - CHECK E-STOP")
        elif eva_state == RobotState.ERROR.value and recur_count == self.reset_attempts:
            raise EvaError(f"Unable to reset robot: {eva.name}")

    @staticmethod
    def check_in_ready_state(eva: Eva) -> bool:
        eva_name = eva.name()['name']
        eva_state = eva.data_snapshot_property('control')['state']
        if eva_state == RobotState.READY.value:
            print(f"{eva_name}: READY TO RUN")
            return True
        else:
            return False

    def send_home_pair(self) -> None:
        for eva in self.robot_pair:
            with eva.lock():
                self.check_and_reset_state(eva)
        for eva in self.robot_pair:
            with eva.lock():
                print(f"{eva.name()['name']}: SENDING HOME")
                eva.control_home(wait_for_ready=True)

    @staticmethod
    def set_active_toolpath(eva: Eva, toolpath_id: int) -> None:
        eva.toolpaths_use_saved(toolpath_id)

    def run_toolpath_pair(self) -> None:
        for eva in self.robot_pair:
            self.check_in_ready_state(eva)
        for eva in self.robot_pair:
            with eva.lock():
                print(f"{eva.name()['name']}: STARTING TOOLPATH")
                eva.control_run(loop=0, wait_for_ready=False, mode='automatic')

    def stop_toolpath_pair(self) -> None:
        for eva in self.robot_pair:
            with eva.lock():
                eva.control_stop_loop(wait_for_ready=True)


if __name__ == '__main__':
    robot_1_eva = Eva('10.10.60.175', '357abe95ba3b3b412a09f765f5395ae533616eb7')
    robot_2_eva = Eva('10.10.60.189', '19a397843a066a8838d62630c88f060db76fd25b')
    eva_x2 = EvaPair(robot_1_eva, robot_2_eva)
    eva_x2.send_home_pair()
    eva_x2.run_toolpath_pair()
    eva_x2.stop_toolpath_pair()
