#!/usr/bin/env python
from new_linn import LinnTwinRobotApp
import sys
""" Main file to run application """

"""
Commands to run to install and run

pipenv install
pipenv run python main.py
OR
pipenv run python main.py --headerless
"""

if __name__ == '__main__':
    robot_1_details = {'ip': '10.10.60.175', 'token': '357abe95ba3b3b412a09f765f5395ae533616eb7'}
    robot_2_details = {'ip': '10.10.60.189', 'token': '19a397843a066a8838d62630c88f060db76fd25b'}
    app = LinnTwinRobotApp(robot_1_details, robot_2_details)
    if '--headerless' in sys.argv:
        app.scan_and_run_barcode(headerless=True)
    else:
        app.run()

