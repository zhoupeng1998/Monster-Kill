#
#                             _ooOoo_
#                            o8888888o
#                            88" . "88
#                            (| -_- |)
#                            O\  =  /O
#                         ____/`---'\____
#                       .'  \\|     |//  `.
#                      /  \\|||  :  |||//  \
#                     /  _||||| -:- |||||-  \
#                     |   | \\\  -  /// |   |
#                     | \_|  ''\---/''  |   |
#                     \  .-\__  `-`  ___/-. /
#                   ___`. .'  /--.--\  `. . __
#                ."" '<  `.___\_<|>_/___.'  >'"".
#               | | :  `- \`.;`\ _ /`;.`/ - ` : | |
#               \  \ `-.   \_ __\ /__ _/   .-` /  /
#          ======`-.____`-.___\_____/___.-`____.-'======
#                             `=---='
#          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#                     佛祖保佑        永无BUG
#

import json

class Agent:
    # construct Agent object
    def __init__ (self, alpha, gamma, epsilon, n):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n = n
        self.q_table = dict()
    
    # get observations from world state, returns a world state dictionary
    @staticmethod
    def getObservations (world_state) -> dict:
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            return json.loads(msg)
        else:
            return dict()
    
    

