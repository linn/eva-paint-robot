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
        self.toolpath_db = None

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

    def load_toolpath_db(self) -> dict:
        with open(self.barcode_tp_pkl, 'rb') as pkl_file:
            toolpath_db = pickle.load(pkl_file)
        return toolpath_db

    def update_toolpath_db(self, toolpath_ids: dict) -> None:
        toolpath_db = self.load_toolpath_db()
        toolpath_db.update(toolpath_ids)
        with open(self.barcode_tp_pkl, 'wb') as db_update:
            pickle.dump(toolpath_db, db_update)

    def set_pair_toolpath(self, toolpath_dict: dict) -> None:
        for left_right in self.robot_order:
            with self.robot_order[left_right].lock():
                self.robot_order[left_right].toolpaths_use_saved(toolpath_dict[left_right])

    def set_left_right_robot_toolpaths(self) -> dict:
        barcode_toolpaths = {'left': None, 'right': None}
        for left_right in self.robot_order:
            self.toolpath_list_name(self.robot_order[left_right], left_right)
            toolpath_num = int(input("Enter toolpath number: "))
            barcode_toolpaths.update({left_right: toolpath_num})
            self.input_toolpath_name(self.robot_order[left_right], left_right, toolpath_num)
        return barcode_toolpaths

    def scan_and_run_barcode(self):
        print("ENTERING OPERATION MODE")
        running = True
        while running:
            scanned_barcode = input("Scan barcode (s to stop): ")
            toolpath_db = self.load_toolpath_db()
            if scanned_barcode == 's':
                self.eva_pair.stop_toolpath_pair()
            elif scanned_barcode in toolpath_db:
                tp_dict = toolpath_db.get(scanned_barcode)
                self.eva_pair.stop_toolpath_pair()
                self.set_pair_toolpath(tp_dict)
                self.eva_pair.send_home_pair()
                self.eva_pair.run_toolpath_pair()
            elif scanned_barcode not in toolpath_db:
                print("BARCODE NOT IN DATABASE")
                self.eva_pair.stop_toolpath_pair()
                self.assign_barcode(scanned_barcode)

    def assign_barcode(self, scanned_barcode: str = None):
        if not scanned_barcode:
            scanned_barcode = input("Scan barcode: ")
        toolpath_db = self.load_toolpath_db()

        if scanned_barcode not in toolpath_db:
            new_barcode = {scanned_barcode: self.set_left_right_robot_toolpaths()}
            self.update_toolpath_db(new_barcode)
        if scanned_barcode in toolpath_db:
            override = input("Toolpath already exists, override? (y/n)").lower()
            if override == 'y':
                new_barcode = {scanned_barcode: self.set_left_right_robot_toolpaths()}
                self.update_toolpath_db(new_barcode)
            elif override == 'n':
                print("Ignoring barcode")

    def run(self):
        while True:
            ass_or_run = input("Do you wish to assign barcodes? (y/n)").lower()
            if ass_or_run == 'y':
                self.assign_barcode()
            elif ass_or_run == 'n':
                self.scan_and_run_barcode()
            else:
                print(f"Unexpected input: {ass_or_run}")


if __name__ == '__main__':
    robot_1_details = {'ip': '10.10.60.175', 'token': '357abe95ba3b3b412a09f765f5395ae533616eb7'}
    robot_2_details = {'ip': '10.10.60.189', 'token': '19a397843a066a8838d62630c88f060db76fd25b'}
    app = LinnTwinRobotApp(robot_1_details, robot_2_details)
    app.run()
