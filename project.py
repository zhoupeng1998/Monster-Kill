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

import MalmoPython
import os
import sys
import time
import json
from agent import Agent
import random

if __name__ == "__main__":

    # read mission
    with open('mission.xml','r') as iFile:
        missionXML = iFile.read()
        iFile.close()

    agent_host = MalmoPython.AgentHost()
    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print('ERROR:', e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        print(agent_host.getUsage())
        exit(0)
    
    iRepeat = 10
    agent = Agent()

    for i in range(iRepeat):
        agent.pastActions = []
        my_mission = MalmoPython.MissionSpec(missionXML, True)
        my_mission_record = MalmoPython.MissionRecordSpec()

        # Start mission
        max_retries = 3
        my_client_pool = MalmoPython.ClientPool()
        my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
        for retry in range(max_retries):
            try:
                agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "Monster Killer")
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)
        
        # Wait until mission starts:
        print("Waiting for the mission to start")
        world_state = agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.1)
            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:", error.text)
        print("Mission started")

        # Mission processing, TODO: move actions to agent class
        observations = agent.getObservations(world_state)
        time.sleep(1)
        while world_state.is_mission_running:
            time.sleep(0.1)

            
            #for error in world_state.errors:
            #   print("Error:", error.text)

            # get observation, state, action
            
            #if len(observations) <= 1:
            #   continue
            agent.run(agent_host)
            
            
            #actions = agent.getActions(state)
            #print("State:", state)
            #print("Actions:", actions)
            # randomize an action
            
            
            #actind = random.randint(0, len(actions) - 1)
            #agent.pastActions.append(actions[actind])
            
            
            

            #agent.act(actions[actind], agent_host)
            
            
            
            #getQ_tableKey(state)
            #print("Action:", actions[actind])
            world_state = agent_host.getWorldState()
            observations = agent.getObservations(world_state)
            while len(observations) <= 1:
                observations = self.getObservations(world_state)
            state = agent.getState(observations)
            if not observations['IsAlive'] or state[0] < 0:
                break
        print("Mission ended")
        print(agent.q_table)
        agent.pastActions = []
        agent.weapon = 1
        time.sleep(1) # sleep for 1s, otherwise it will not restart





