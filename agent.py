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
import time
import random

class Agent:
    # construct Agent object
    def __init__ (self, alpha=0.3, gamma=1, epsilon=0.2, n=1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n = n
        self.weapon = 1
        self.q_table = dict()
        self.pastActions = [];
    
    # get observations from world state, returns a world state dictionary
    @staticmethod
    def getObservations (world_state) -> dict:
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            return json.loads(msg)
        else:
            return dict()
    
    # get the position between agent and the clostest mob.
    # currently only considers zpos
    def getMobDistance (self, zpos, entities):
        distList = list()
        for mob in entities:
            if mob['name'] in set(['Zombie','Skeleton','PigZombie','WitherSkeleton','WitherBoss']):
                distList.append(abs(mob['z'] - zpos))
        if len(distList) > 0:
            return min(distList)
        else:
            return -1

    # get current state with observation
    def getState (self, observations):
        floatDistance = self.getMobDistance(observations['ZPos'], observations['entities'])
        if floatDistance < 0:
            intDistance = -1
        elif floatDistance <= 3:
            intDistance = 3
        elif floatDistance <= 5:
            intDistance = 5
        elif floatDistance <= 10:
            intDistance = 10
        elif floatDistance <= 15:
            intDistance = 15
        else:
            intDistance = 20
        
        state = list(intDistance, self.weapon)
        for i in sorted(self.pastActions):
            state.append(i)
        return tuple(state)
    
    # get all possible actions with current state
    def getActions (self, state):
        actionList = ['go_front', 'go_back']
        if state[0] <= 3:
            for wid in range(1,7):
                if not wid == state[1]:
                    actionList.append('swap_' + str(wid))
            if state[1] != 1:
                actionList.append('attack')
        elif state[1] != 1:
            actionList.append('swap_1')
        if state[1] == 1:
            actionList.append("shot_0.4")
            actionList.append("shot_0.6")
            actionList.append("shot_0.9")
        return actionList

    # let agent host do action
    def act (self, action, agent_host):
        if action == 'go_front':
            agent_host.sendCommand('move 1')
        elif action == 'go_back':
            agent_host.sendCommand('move -1')
        elif action == 'attack':
            self.closeAttack(agent_host)
        elif action.startswith('swap'):
            self.swapWeapon(int(action[5:]), agent_host)
        elif action.startswith('shot'):
            self.rangeShoot(float(action[5:]), agent_host)
        
    # swap to other weapons in hotbar, with weapon slot id
    def swapWeapon (self, id, agent_host):
        assert id >= 1, "Weapon ID out of range"
        assert id <= 6, "Weapon ID out of range"
        agent_host.sendCommand("hotbar.%s 1" % id)
        agent_host.sendCommand("hotbar.%s 0" % id)
        self.weapon = id

    # agent close attack. most possessing a sword
    def closeAttack (self, agent_host):
        assert self.weapon >= 1 and self.weapon <= 6, "Wrong close attack weapon"
        agent_host.sendCommand("attack 1")
        time.sleep(0.5)
        agent_host.sendCommand("attack 0")
    
    # agent range shot with given time
    def rangeShoot (self, floatTime, agent_host):
        assert self.weapon == 1, "Wrong range attack weapon"
        agent_host.sendCommand("use 1")
        time.sleep(floatTime)
        agent_host.sendCommand("use 0")

    # agent choose actions among possible_action list
    def choose_actions(curr_state, possible_actions, eps, q_table):
        rnd = random.random()
        if rnd <= eps:
            action = random.randiant(0, len(possible_actions)-1)
        else:
            sortedlist = [(k, q_table[curr_state][k]) for k in sorted(q_table[curr_state], key = q_table[curr_state].get, reverse = True)]
            if (len(sortedlist)) >= 2 and sortedlist[0][1] == sortedlist[1][1]:
                action = random.randient(0, len(possible_actions) - 1)
            else:
                a = sortedlist[0][0]
                for i in range(len(possible_actions)):
                    if a == possible_actions[i]:
                        action = i
                        break
        return possible_actions[action]




        
        
