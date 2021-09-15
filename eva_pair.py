import evasdk


class EvaPair:
    def __init__(self, robot_1: dict, robot_2: dict):
        self.left_robot = evasdk.Eva(robot_1['ip'], robot_1['token'])
        self.right_robot = evasdk.Eva(robot_2['ip'], robot_2['token'])


if __name__ == '__main__':
    robot_1_details = {'ip': '172.16.16.2', 'token': ''}
    robot_2_details = {'ip': '172.16.16.3', 'token': ''}
    eva_x2 = EvaPair(robot_1_details, robot_2_details)
