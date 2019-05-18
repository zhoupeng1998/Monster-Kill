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

from malmo import MalmoPython
import os
import sys
import time
import json
from agent import Agent

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
    
    iRepeat = 1
    agent = Agent()

    for i in range(iRepeat):
        my_mission = MalmoPython.MissionSpec(missionXML, True)
        my_mission_record = MalmoPython.MissionRecordSpec()

        # Start mission
        max_retries = 3
        for retry in range(max_retries):
            try:
                agent_host.startMission(my_mission, my_mission_record)
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

        # Mission processing
        a = 0
        while world_state.is_mission_running:
            time.sleep(0.1)

            world_state = agent_host.getWorldState()
            for error in world_state.errors:
                print("Error:", error.text)

            # get observation, state, action
            observations = agent.getObservations(world_state)
            state = agent.getState(observations)
            print("State:", state)
            print("Actions: ",agent.getActions(state))

            print("shot!")
            a += 1
        print("Mission ended")
        agent.weapon = 1
