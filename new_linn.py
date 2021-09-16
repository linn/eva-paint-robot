#!/usr/bin/env python3
"""
Alastair Bennett    10:52 AM
1) Scan barcode
2) It's asks what Toolpath for Left robot to assign to that
3) It asks what Toolpath for Right robot to assign to that
4) Run by toolpath name
5) left and right robot
"""
from evasdk import Eva
import pickle
import eva_pair


class LinnTwinRobotApp:
    def __init__(self, robot_left: dict, robot_right: dict):
        self.robot_left = Eva(robot_left['ip'], robot_left['token'])
        self.robot_right = Eva(robot_right['ip'], robot_right['token'])
        self.robot_order = {'left': self.robot_left, 'right': self.robot_right}
        self.eva_pair = eva_pair.EvaPair(self.robot_left, self.robot_right)
        self.barcode_tp_pkl = "barcode_toolpath.pkl"

    @staticmethod
    def toolpath_list_name(eva: Eva, left_right: str) -> None:
        toolpath_list_name_only = []
        print(f"Available toolpaths - Number to enter to set toolpath for {left_right} robot")
        for toolpaths in eva.toolpaths_list():
            print(f"{toolpaths['name']}    -    {toolpaths['id']}")
            toolpath_list_name_only.append(toolpaths['name'])

    @staticmethod
    def input_toolpath_name(eva: Eva, left_right: str, toolpath_id: int) -> None:
        with eva.lock():
            print(f"{eva.name()['name']} ({left_right}): Setting active toolpath")
            eva.toolpaths_use_saved(toolpath_id)

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
                toolpath = input("Input Toolpath ID (l for list):")
                if toolpath == "l":
                    print(self.robot_left.toolpaths_list())
                    toolpath = int(input("Input Tootpath ID:"))

            barcode_toolpath[barcode] = toolpath
        print(barcode_toolpath)

        with open(self.barcode_tp_pkl, "ab") as pkl_file:  # EM: Changed
            pickle.dump(barcode_toolpath, pkl_file)

    def run_barcode_toolpath(self):
        running = True
        with open(self.barcode_tp_pkl, "rb") as pkl_file:
            barcode_toolpath = pickle.load(pkl_file)

        while running:
            barcode = input("\nScan Barcode... (q to quit):")
            if barcode == "q":
                running = False
            elif barcode in barcode_toolpath:
                toolpath_id = barcode_toolpath.get(barcode)

                """with eva.lock():
                    eva.control_wait_for_ready()
                    eva.toolpaths_use_saved(int(toolpath_id))  # EM: Changed
                    eva.control_home()
                    eva.control_run(loop=0, mode='automatic')  # EM: Changed"""
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

    def set_left_right_robot_toolpaths(self):
        for left_right in self.robot_order:
            self.toolpath_list_name(self.robot_order[left_right], left_right)
            toolpath_num = int(input("Enter toolpath number: "))
            self.input_toolpath_name(self.robot_order[left_right], left_right, toolpath_num)



if __name__ == '__main__':
    robot_1_details = {'ip': '10.10.60.175', 'token': '357abe95ba3b3b412a09f765f5395ae533616eb7'}
    robot_2_details = {'ip': '10.10.60.189', 'token': '19a397843a066a8838d62630c88f060db76fd25b'}
    app = LinnTwinRobotApp(robot_1_details, robot_2_details)
    app.set_left_right_robot_toolpaths()
