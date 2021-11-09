#!/usr/bin/env python3

from new_linn import LinnTwinRobotApp
import os
import sys
import dotenv

""" Main file to run application """

"""
Commands to run to install and run

pipenv install
pipenv run python main.py
OR
pipenv run python main.py --headerless
"""

if __name__ == '__main__':
    robot_1_details = {'ip': os.environ['ROBOT1IP'], 'token': os.environ['ROBOT1API']}
    robot_2_details = {'ip': os.environ['ROBOT2IP'], 'token': os.environ['ROBOT2API']}
    app = LinnTwinRobotApp(robot_1_details, robot_2_details)
    if '--headerless' in sys.argv:
        print("Running in headerless mode")
        print("Check the eva.log file for any output")
        app.scan_and_run_barcode(headerless=True)
    else:
        app.run()
