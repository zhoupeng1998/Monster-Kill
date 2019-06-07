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

import math
import json

enemies = set(['WitherSkeleton','Stray','Husk','Giant','Spider','Zombie','Skeleton'
               ,'PigZombie','WitherBoss','VillagerGolem','Guardian','Witch','EnderDragon'
               ,'Blaze','Ghast','Creeper','VindicationIllager','ZombieVillager','ElderGuardian'])

action_list = ['shoot_0.4', 'shoot_0.6', 'shoot_0.9', 'attack_2', 'attack_3', 'go_back', 'go_front']

rewards_map = {'shoot':[-2,30],'attack_2':[-1,16],'attack_3':[-6.83,43],'go_back':[0,0],'go_front':[0,0]}

weapon_count_map = {'shoot':0,'attack_2':0,'attack_3':0,'go_back':0,'go_front':0}

def getObservations (world_state) -> dict:
    if world_state.number_of_observations_since_last_state > 0:
        msg = world_state.observations[-1].text
        return json.loads(msg)
    else:
        return dict()

# untested
# returns 2-tuple (MobX, MobZ)
def getClostestMobPosition (self, agtX, agtZ, entities):
    distDict = dict()
    for mob in entities:
        if mob['name'] in enemies:
            dist = math.sqrt(abs(mob['x'] - agtX)**2 + abs(mob['z'] - agtZ)**2)
            distDict[dist] = (mob['x'], mob['z'])
    if len(distDict) > 0:
        return distDict[min(distDict.keys())]
    else:
        return -1

def turnFacingByAgentTargetPosition (agtX, agtZ, tarX, tarZ, agent_host):
    diffX = tarX - agtX
    diffZ = tarZ - agtZ
    if diffZ == 0:
        if diffX > 0:
            agent_host.sendCommand("setYaw -90")
        else:
            agent_host.sendCommand("setYaw 90")
        return
    else:
        ang = math.degrees(math.atan2(abs(diffX), abs(diffZ)))
        print(ang)
    if diffZ < 0:
        if diffX > 0:
            agent_host.sendCommand("setYaw %f" % (ang-180))
        else:
            agent_host.sendCommand("setYaw %f" % (180-ang))
    else:
        if diffX > 0:
            agent_host.sendCommand("setYaw %f" % (0-ang))
        else:
            agent_host.sendCommand("setYaw %f" % (ang-0))