#!/usr/bin/env python3
"""
Alastair Bennett    10:52 AM
1) Scan barcode
2) It's asks what Toolpath for Left robot to assign to that
3) It asks what Toolpath for Right robot to assign to that
4) Run by toolpath name
5) left and right robot
"""
import evasdk
import pickle


class LinnTwinRobotApp:
    def __init__(self, robot_1: dict, robot_2: dict):
        self.left_robot = evasdk.Eva(robot_1['ip'], robot_1['token'])
        self.right_robot = evasdk.Eva(robot_2['ip'], robot_2['token'])
        self.barcode_tp_pkl = "barcode_toolpath.pkl"

    def assign_barcode(self):
        barcode_toolpath: dict = {}
        barcode = ""
        toolpath = ""
        running = True

        while running:
            barcode = None
            toolpath = ""

            while not barcode:
                barcode = input("\nScan Barcode... (q to quit):")

                if barcode in barcode_toolpath:
                    override = input("Barcode already registered. Override? (y/n)")

                    if override == "n":
                        barcode = None

                if barcode == "q":
                    running = False

            while not toolpath:
                toolpath = input("Input Tootpath ID (l for list):")
                if toolpath == "l":
                    print(self.left_robot.toolpaths_list())

                    toolpath = int(input("Input Tootpath ID:"))

            barcode_toolpath[barcode] = toolpath

        print(barcode_toolpath)
        a_file = open(self.barcode_tp_pkl, "ab")  # EM: Changed
        pickle.dump(barcode_toolpath, a_file)
        a_file.close()

    def run_barcode_toolpath(self):
        running = True
        with open(self.barcode_tp_pkl, "rb") as pkl_file:
            barcode_toolpath = pickle.load(pkl_file)

        while running:
            barcode = input("\nScan Barcode... (q to quit):")

            if barcode == "q":
                running = False

            if barcode in barcode_toolpath:
                toolpath_id = barcode_toolpath.get(barcode)

                with eva.lock():
                    eva.control_wait_for_ready()
                    eva.toolpaths_use_saved(int(toolpath_id))  # EM: Changed
                    eva.control_home()
                    eva.control_run(loop=0, mode='automatic')  # EM: Changed
            else:
                print("Barcode Unregistered!")

    def run(self):
        ass_or_run = input("Do you wish to assign barcodes? (y/n)").lower()
        if ass_or_run == 'y':
            self.assign_barcode()
        elif ass_or_run == 'n':
            print("")
            self.run_barcode_toolpath()
        else:
            raise ValueError(f"Unexpected input: {ass_or_run}")


if __name__ == '__main__':
    robot_1_details = {'ip': '172.16.16.2', 'token': ''}
    robot_2_details = {'ip': '172.16.16.3', 'token': ''}
    app = LinnTwinRobotApp(robot_1_details, robot_2_details)
