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
#            代码千万条，注释第一条，注释不规范，同事两行泪

import json
import time
from collections import defaultdict, deque
import random
import sys
import math
import utils


health_point = {'full':3,'high':4,'mid':5,'low':6}

class Agent:
    # construct Agent object
    def __init__ (self, alpha=0.3, gamma=1, epsilon=0.5, n=1):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.n = n
        self.weapon = 1
        self.q_table = dict()
        self.MonsterHeart = 20
        self.Heart = 20
        self.action = 0
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
            if mob['name'] in utils.enemies:
                distList.append(abs(mob['z'] - zpos))
        if len(distList) > 0:
            return min(distList)
        else:
            return -1

    # get current state with observation
    # current assumes enemies are all aimed!
    def getState (self, observations):
        floatDistance = self.getMobDistance(observations['ZPos'], observations['entities'])
        floatLife = observations["Life"]
        if floatLife <= 5:
            life = "low"
        elif floatLife <= 10:
            life = "mid"
        elif floatLife <= 15:
            life = "high"
        else:
            life = "full"
        if floatDistance < 0:
            floatDistance = -1
        if floatDistance > 15:
            floatDistance = 20
        elif floatDistance > 10:
            floatDistance = 15
        elif floatDistance > 5:
            floatDistance = 10
        if 'LineOfSight' not in observations.keys():
            return (int(floatDistance), life, 0)
        if observations['LineOfSight']['hitType'] == 'entity':
            return (int(floatDistance), life, 1)
        else:
            return (int(floatDistance), life, 0)
    # get all possible actions with current state
    # currently returns 7 actions for all states
    def getActions (self, state):
        if state[2] == 0:
            return utils.action_list
        else:
            return utils.action_list_aimed

    # let agent host do action
    def act (self, action, agent_host):
        self.action+=1
        if action == 'go_front':
            agent_host.sendCommand('move 1')
            time.sleep(0.25)
            agent_host.sendCommand('move 0')
        elif action == 'go_back':
            agent_host.sendCommand('move -1')
            time.sleep(0.25)
            agent_host.sendCommand('move 0')
        elif action == 'aim':
            return 0
        
        elif action.startswith('attack'):
            utils.weapon_count_map[action] += 1
            self.swapWeapon(int(action[7:]), agent_host)
            self.closeAttack(agent_host)
        else:
            utils.weapon_count_map['shoot'] += 1
            self.swapWeapon(1, agent_host)
            self.rangeShoot(float(action[6:]), agent_host)
        
    # swap to other weapons in hotbar, with weapon slot id
    def swapWeapon (self, id, agent_host):
        assert id >= 1, "Weapon ID out of range"
        assert id <= 3, "Weapon ID out of range"
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
    
    # update Q-table, performs relevant updates for state tau.
    def updateQTable(self, tau, S, A, R, T,i):
        """
            tau: <int>  state index to update
            S:   <dequqe>   states queue
            A:   <dequqe>   actions queue
            R:   <dequqe>   rewards queue
            T:   <int>      terminating state index
            """

        
        curr_s, curr_a, curr_r = S[i], A[i], R[i+1]
        
        #G = sum([self.gamma ** i * R[i] for i in range(len(S))])
        #if tau + self.n < T:
        #    G += self.gamma ** self.n * self.q_table[S[-1]][A[-1]]
        
        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (curr_r - old_q)

    # agent choose actions among possible_action list
    def chooseActions(self,curr_state, possible_actions, eps):
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
    

    
    # returns damage dealt to enemy

    def damageDone(self,agent_host,observations,action):
        if action == 'go_back' or action == 'go_front':
            return 0
        if action.startswith('shoot'): # special care for shoot actions
            action = 'shoot'
        damage = -1
        life =1000000
        for mob in observations['entities']:
            if mob['name'] in utils.enemies:
                life = mob['life']
        if life < self.MonsterHeart:
            damage += (self.MonsterHeart - life)
            self.MonsterHeart = life
            return damage*3
        
        return damage
    """
    def damageDone(self,agent_host,observations,action):
        if action == 'go_back' or action == 'go_front':
            return 0

        damage = 0
        if (observations['DamageDealt'] > self.damageD):
            damage = observations['DamageDealt'] - self.damageD
            print(observations['DamageDealt'])
            print(self.damageD)
            self.damageD = observations['DamageDealt']

        return damage

    """
    # return damage dealt by ememy
    def receiveDamage(self,agent_host,observations,state):
        total = 0
        for mob in observations['entities']:
            if mob['name'] == 'Monster Killer':
                life = mob['life']
        if life < self.Heart:
            total = self.Heart-life
            self.Heart = life
        return total*health_point[state[1]]
    
    # calculate weapon usage penalty
    def maxAttack(self,agent_host,observations,action):
        if action.startswith('shoot'): # special care for shoot actions
            action = 'shoot'
        if utils.rewards_map[action][1] == 0:
            return 0
        if utils.weapon_count_map[action] > utils.rewards_map[action][1]:
            return -20
        return 0
    
    # deduct reward calculated by accumulated number round of actions
    def timeDecay(self):
        reward = math.exp(0.125*self.action) -1
        return -reward
    
    # calculate reward with damage, weapon penalty
    def rewardCalculate(self,agent_host,observations,action,state):
        total = 0
        if action == 'go_back':
            total += 2
        elif action == 'go_front':
            total += 2
        elif action == 'aim':
            return 10
        elif action.startswith('shoot'): # special care for shoot actions
            action = 'shoot'
        total += self.damageDone(agent_host,observations,action)
        total += self.receiveDamage(agent_host,observations,state)
        total += self.maxAttack(agent_host,observations,action)
        #total += self.timedeclay()
        return total
    
    # change direction to face closest enemy
    def changeDirection(self,agent_host,observations):
        zx = 0
        zz = 0
        ax = 0
        az = 0
        
        for mob in observations['entities']:
            if mob['name'] == 'Monster Killer':
                ax = mob['x']
                az = mob['z']
        mob = utils.getClostestMobPosition(ax,az,observations['entities'])
        if (mob != -1):
        
            utils.turnFacingByAgentTargetPosition(ax, az, mob[0], mob[1], agent_host)
    
    # main loop
    def run(self,agent_host):
        aimflag = 0
        for action in utils.weapon_count_map:
            utils.weapon_count_map[action] = 0
        deadflag = 0
        S, A, R = [],[],[]
        present_reward = 0
        done_update = False
        while not done_update:
            world_state = agent_host.getWorldState()
            # get observation until it's not empty
            observations = self.getObservations(world_state)
            while len(observations) <= 1:
                observations = self.getObservations(world_state)
            
            for mob in observations['entities']:
                if mob['name'] in utils.enemies:
                    self.MonsterHeart = mob['life']
            s0 = self.getState(observations)
            possible_actions = self.getActions(s0)
            a0 = self.chooseActions(s0, possible_actions, self.epsilon)
            self.pastActions.append(a0)
            S.append(s0)
            A.append(a0)
            R.append(0)
            T = sys.maxsize
            for t in range(sys.maxsize):
                if t < T:
                    # print state and action
                    #print(S[-1], ",", A[-1], end=' , ')
                    # change direction and act
                    if aimflag == 1:
                        self.changeDirection(agent_host,observations)
                        aimflag = 0
                    if A[-1] == 'aim':
                        aimflag = 1
                        self.changeDirection(agent_host,observations)
                    
                    self.act(A[-1],agent_host)
                    
                    if A[-1][0] == 's':
                        time.sleep(0.7)
                    if A[-1][0] == 'a':
                        time.sleep(0.1)
                    world_state = agent_host.getWorldState()
                    for mob in observations['entities']:
                        if mob['name'] == 'Monster Killer':
                            life = mob['life']
                    self.Heart = life
                    
                    observations = self.getObservations(world_state)
                    attempt = 0
                    while len(observations) <= 1:
                        observations = self.getObservations(world_state)
                        attempt += 1
                        if attempt == 10:
                            deadflag = 1
                            break
                    if deadflag == 1:
                        done_update = True
                        break
                    #get reward
                   
                    current_r = self.rewardCalculate(agent_host,observations,A[-1],S[-1])
                    #print(current_r)
                    R.append(current_r)
                    if not observations['IsAlive'] or S[-1][0] < 0:
                        # Terminating state
                        T = t + 1
                        S.append('Term State')
                        present_reward = current_r
                    else:
                        s = self.getState(observations)
                        S.append(s)
                        possible_actions = self.getActions(s)
                        next_a = self.chooseActions(s, possible_actions, self.epsilon)
                        self.pastActions.append(next_a)
                        A.append(next_a)
                tau = t - self.n + 1
                if tau == T - 1:
                    for i in range(len(S)-1):
                        tau = tau + 1
                        self.updateQTable(tau, S, A, R, T,i)
                    done_update = True
                    break

        if deadflag == 1:
            for i in range(len(S)-1):
                tau = tau + 1
                self.updateQTable(tau, S, A, R, T,i)

