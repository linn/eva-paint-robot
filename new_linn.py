#!/usr/bin/env python3
""" App module, will be called by main.py """
import pickle
from evasdk import Eva
import eva_pair
import scanner

class LinnTwinRobotApp:
    """ Main running application class """

    def __init__(self, robot_left: dict, robot_right: dict):
        self.robot_left = Eva(robot_left['ip'], robot_left['token'])
        self.robot_right = Eva(robot_right['ip'], robot_right['token'])
        self.robot_order = {'left': self.robot_left, 'right': self.robot_right}
        self.eva_pair = eva_pair.EvaPair(self.robot_left, self.robot_right)
        self.barcode_tp_pkl = "barcode_toolpath.pkl"

    @staticmethod
    def toolpath_list_name(eva: Eva, left_right: str) -> None:
        """ Pulls toolpath list from the robot """
        toolpath_list_name_only = []
        print(f"Available toolpaths - Number to enter to set toolpath for {left_right} robot")
        for toolpaths in eva.toolpaths_list():
            print(f"{toolpaths['name']}    -    {toolpaths['id']}")
            toolpath_list_name_only.append(toolpaths['name'])

    @staticmethod
    def input_toolpath_name(eva: Eva, left_right: str, toolpath_id: int) -> None:
        """ Sets active toolpath on the robot """
        with eva.lock():
            print(f"{eva.name()['name']} ({left_right}): Setting active toolpath")
            eva.toolpaths_use_saved(toolpath_id)

    def load_toolpath_db(self) -> dict:
        """ Returns the latest barcode DB """
        with open(self.barcode_tp_pkl, 'rb') as pkl_file:
            toolpath_db = pickle.load(pkl_file)
        return toolpath_db

    def update_toolpath_db(self, toolpath_ids: dict) -> None:
        """ Updates the barcode DB """
        toolpath_db = self.load_toolpath_db()
        toolpath_db.update(toolpath_ids)
        with open(self.barcode_tp_pkl, 'wb') as db_update:
            pickle.dump(toolpath_db, db_update)

    def set_pair_toolpath(self, toolpath_dict: dict) -> None:
        """ Sets the toolpaths on both robots from dict passed to it """
        for left_right in self.robot_order:
            with self.robot_order[left_right].lock():
                self.eva_pair.check_and_reset_state(self.robot_order[left_right])
                self.robot_order[left_right].toolpaths_use_saved(toolpath_dict[left_right])

    def set_left_right_robot_toolpaths(self) -> dict:
        """ Prompts and then loads the requested toolpath to the robots individually """
        barcode_toolpaths = {'left': None, 'right': None}
        for left_right in self.robot_order:
            self.toolpath_list_name(self.robot_order[left_right], left_right)
            toolpath_num = int(input("Enter toolpath number: "))
            barcode_toolpaths.update({left_right: toolpath_num})
            self.input_toolpath_name(self.robot_order[left_right], left_right, toolpath_num)
        return barcode_toolpaths

    def scan_and_run_barcode(self, headerless: bool = False):
        """ Normal operation mode, scan, stop, run, add additional barcodes """
        print("ENTERING OPERATION MODE")
        default_toolpath = {'left': 1, 'right': 1}  # You would change this to the default toolpath number
        while True:
            # scanned_barcode = input("Scan barcode (stop to halt): ")
            print("Scan barcode: ", end="")
            scanned_barcode = scanner.wait_for_input()
            toolpath_db = self.load_toolpath_db()
            if scanned_barcode == 'stop':
                self.eva_pair.stop_toolpath_pair()
            elif scanned_barcode in toolpath_db:
                tp_dict = toolpath_db.get(scanned_barcode)
                self.eva_pair.stop_toolpath_pair()
                self.set_pair_toolpath(tp_dict)
                self.eva_pair.send_home_pair()
                self.eva_pair.run_toolpath_pair()
            elif scanned_barcode not in toolpath_db and headerless:
                print("BARCODE NOT IN DATABASE - RUNNING DEFAULT")
                self.eva_pair.stop_toolpath_pair()
                self.set_pair_toolpath(default_toolpath)
                self.eva_pair.send_home_pair()
                self.eva_pair.run_toolpath_pair()
            elif scanned_barcode not in toolpath_db and not headerless:
                print("BARCODE NOT IN DATABASE")
                self.eva_pair.stop_toolpath_pair()
                self.assign_barcode(scanned_barcode)

    def assign_barcode(self, scanned_barcode: str = None):
        """ Scan and assign toolpaths to barcodes """
        if not scanned_barcode:
            # scanned_barcode = input("Scan barcode: ")
            print("Scan barcode: ", end="")
            scanned_barcode = scanner.wait_for_input()
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
        """ Initial startup loop """
        while True:
            ass_or_run = input("Do you wish to assign barcodes? (y/n)").lower()
            if ass_or_run == 'y':
                self.assign_barcode()
            elif ass_or_run == 'n':
                self.scan_and_run_barcode()
            else:
                print(f"Unexpected input: {ass_or_run}")
