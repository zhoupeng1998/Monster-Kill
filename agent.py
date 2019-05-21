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
from collections import defaultdict, deque
import random
import sys
import math

class Agent:
    # construct Agent object
    def __init__ (self, alpha=0.3, gamma=1, epsilon=0.2, n=1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n = n
        self.weapon = 1
        self.q_table = dict()

        self.pastActions = []
    
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
                distList.append(mob['z'] - zpos)
        if len(distList) > 0:
            return min(distList)
        else:
            return -100000

    # get current state with observation
    def getState (self, observations):
        floatDistance = self.getMobDistance(observations['ZPos'], observations['entities'])
        return int(floatDistance)
        
        if floatDistance == -100000:
            intDistance = -100000
        elif floatDistance < 0:
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
      #state = list((intDistance, self.weapon))
            #for i in self.pastActions:
            #state.append(i)
#return tuple(state)
        return intDistance
    
    # get all possible actions with current state
    def getActions (self, state):
        actionList = ['go_back']
        if state < 0:
            return actionList
        
        if state > 1:
            actionList.append('go_front')
        for wid in range(1,7):
            actionList.append('swap_' + str(wid))

        return actionList
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
            #elif action == 'attack':
            #self.closeAttack(agent_host)
        elif action.startswith('swap'):
            print(self.weapon)
            if int(action[5:]) != 1:
                self.swapWeapon(int(action[5:]), agent_host)
                time.sleep(0.1)
                self.closeAttack(agent_host)
            else:
                self.swapWeapon(1, agent_host)
                time.sleep(0.1)
                self.rangeShoot(0.6, agent_host)
#elif action.startswith('shot'):
# self.rangeShoot(float(action[5:]), agent_host)

        return 0
        
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
        time.sleep(0.1)
        agent_host.sendCommand("attack 0")
    
    # agent range shot with given time
    def rangeShoot (self, floatTime, agent_host):
        assert self.weapon == 1, "Wrong range attack weapon"
        agent_host.sendCommand("use 1")
        time.sleep(floatTime)
        agent_host.sendCommand("use 0")
        
    def update_q_table(self, tau, S, A, R, T):
        """Performs relevant updates for state tau.
            
            Args
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
            """
        curr_s, curr_a, curr_r = S.popleft(), A.popleft(), R.popleft()
        
        
        G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        if tau + self.n < T:
            G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]
        
        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

    
        # agent choose actions among possible_action list
    def choose_actions(self,curr_state, possible_actions, eps):
        if curr_state not in self.q_table:
            self.q_table[curr_state] = {}
        for action in possible_actions:
            if action not in self.q_table[curr_state]:
                self.q_table[curr_state][action] = 0
        
        
        
        
        rnd = random.random()
        if rnd <= eps:
            action = random.randint(0, len(possible_actions)-1)
        else:
            sortedlist = [(k, self.q_table[curr_state][k]) for k in sorted(self.q_table[curr_state], key = self.q_table[curr_state].get, reverse = True)]
            if (len(sortedlist)) >= 2 and sortedlist[0][1] == sortedlist[1][1]:
                action = random.randint(0, len(possible_actions) - 1)
            else:
                a = sortedlist[0][0]
                for i in range(len(possible_actions)):
                    if a == possible_actions[i]:
                        action = i
                        break
        return possible_actions[action]

        
        
    def faceEnemy(self,observations,agent_host):
        
        
        
        
        
        
        for mob in observations['entities']:
            if mob['name'] == 'Zombie':
                zomx = float(mob['x'])
                zomy = float(mob['y'])
                zomz = float(mob['z'])
            if mob['name'] == 'Monster Killer':
                agentx = float(mob['x'])
                agenty = float(mob['y'])
                agentz = float(mob['z'])

        newx = agentx - zomx
        newz = agentz - zomz

        dis = self.getMobDistance(observations['ZPos'], observations['entities'])
        c = newx/dis
        print(c)
        #c = math.sqrt(math.pow(newx,2) + math.pow(newz,2))
        A = math.acos(c)
        angle = A * 180/3.1415926
        print(angle)
        
#print(A)

#print(observations['entities'])
    def run(self,agent_host):
        S, A, R = deque(), deque(), deque()
        present_reward = 0
        done_update = False
        while not done_update:
            world_state = agent_host.getWorldState()
            observations = self.getObservations(world_state)
            while len(observations) <= 1:
                observations = self.getObservations(world_state)
            
            
            s0 = self.getState(observations)
            possible_actions = self.getActions(s0)
            a0 = self.choose_actions(s0, possible_actions, self.epsilon)
            self.pastActions.append(a0)
            S.append(s0)
            A.append(a0)
            R.append(0)
            T = sys.maxsize
            for t in range(sys.maxsize):
                time.sleep(0.8)
                if t < T:
              
                    current_r = self.act(A[-1],agent_host)
                    R.append(current_r)
                    
                    if not observations['IsAlive'] or S[-1] == -100000:
                        # Terminating state
                        T = t + 1
                        S.append('Term State')
                        present_reward = current_r
                        print("Reward:", present_reward)
                    else:
                        world_state = agent_host.getWorldState()
                        observations = self.getObservations(world_state)
                        while len(observations) <= 1:
                            observations = self.getObservations(world_state)
                        #self.faceEnemy(observations,agent_host)
    
                        #print(observations)
                        s = self.getState(observations)
               
                        S.append(s)
                        possible_actions = self.getActions(s)
                        next_a = self.choose_actions(s, possible_actions, self.epsilon)
                        self.pastActions.append(next_a)
                        A.append(next_a)
            
                tau = t - self.n + 1
    
                if tau >= 0:
                    
                    self.update_q_table(tau, S, A, R, T)

                if tau == T - 1:
                    while len(S) > 1:
                        tau = tau + 1
                        self.update_q_table(tau, S, A, R, T)
                    done_update = True
                    break
