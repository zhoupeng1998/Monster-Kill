---
layout: default
title:  Status
---

### Project Summary
- Would it be nice to kill monsters with least resources and time? In this project, the agent will learn how to kill mobs (hostile mobs especially) in Minecraft using the most efficient weapon combinations with least costs (health point costs, weapon durability, weapon craft costs,  time costs and etc. would be considered) and dodge attacks in a closed territory (20 x 20) under a “survival” mode setting. We would provide one kind of hostile mobs and multiple weapons as input while the output is expected to be the best combination of weapons and actions to kill the mob with lowest cost. The application of this projects offers players the most efficient approach to kill a specific mob. For beginners of Minecraft, application of this project includes how to survive in a dark night with a large number of different kinds of monsters. For advanced players, it could also be helpful by offering the best combination of weapons and actions to beat more powerful enemies, such as the Wither and the End Dragon. 

### Approach
#### Q-Learning
- The Monster Killer project applies reinforcement learning with Q-learning algorithm. With Q-learning, agent learns a policy that maximizes the reward by choosing the best action in each step. We create a Q-table to store reward of all actions in each state. During the learning process, we use a function to update Q-table with its output reward. The Q-learning function has two inputs: state and action, it returns the expected reward according to the action the agent performed in current state. The learning process contains following steps:
  - Initialize Q-table
  - Loop until learning stops:
    - Choose an action in current state based on current value in Q-table
    - Perform the action and observe the outcome
    - Update Q-table
- When the agent starts learning, all values in Q-table are zero, the best action is unknown, so we must weigh exploration and exploitation rate properly. We use epsilon greedy policy: when the agent chooses an action, it generates a random number. If the number is greater than epsilon, it will exploit the known information by choosing the action with best expected reward; otherwise, it will explore by choosing a random action. When the agent starts learning, we set epsilon value to be 1, then we decrease the epsilon value during learning process.
#### State Define
- States for our project would be defined by a tuple of two factors -- a discrete quantitative variable of the straight line distance from the nearest enemy to the agent and a binary variable of whether the facing direction of the agent aims at the enemy perfectly for attacks (which would be set to 1)  or not (which would be set to 0). Given that different weapons have different ranges to make successful attacks (swords can only do close attacks while bows and arrows can also perform range attacks), too much states in the same range (for instance, <5, 5-10, 10-15, 15-20, >20 are considered as same ranges when making attack) would lead to the misdirection for the agent with different q-values for each action in each state. Therefore, in order to reduce this misdirection of the unnecessary states for the agent, we would eliminate the number of states. Considering that we provide several close attack weapons like wooden swords, stone swords, iron swords, gold swords and diamond swords for the agent to choose, the data variability of close attacks would be higher and therefore need more states. We define distance, the first element in the state tuple,  as 0, 1, 2, 3, 4, 5 for the close range, while we also define range attack distance greater than 6 as 10, greater than 10 as 15, greater than 15 as 20, and greater than 20 as 25. The second element in the state tuple are a binary variable of 0 (the agent is not facing the mob) and 1 (the agent is facing the mob). In conclusion, there are 20 different states in total. For instance, (0, 0) is defined as the straight line distance between the agent and the enemy is 0, and the agent is not facing the enemy; (20, 1) is defined as the straight line distance between the agent and the enemy and the agent is facing the enemy for successful attacks. There are 10 values for distance variable and 2 values for the aiming flag, so there are 20 states possible.
#### Actions Define
- For the actions, the agent could move forward, move backward and aim the enemy for later attacks. The approach of calculating the turning angle to face the enemy perfectly is to calculate the arc tangent of the quotient of the difference on x-axis between the agent and the mob divided by the difference on z-axis between the agent and the mob. For attack actions, the agent would be able to shoot an enemy by a bow with different force by drawing the bow with different time interval. Given that we are in a 20 x 20 world, drawing the bow for 0.9 second would be able to make attack in 15-unit-long distance. Therefore, the agent would be able to draw the bow for 0.4, 0.6, or 0.9 second. It would also be able to attack an enemy with swords made of different materials, including wood, stone, iron, gold, and diamond. In conclusion, the action lists includes three kinds for bow shooting of shoot_0.4, shoot_0.6 and shoot_0.9, five kinds for sword attacking of wood, stone, iron, gold and diamond, and three kinds for movement actions of move_forward, move_backward, and aim. The total number of available actions is 11.
#### Rewards Setting
- For the reward setting, we take into account of weapon rarity, weapon durability, HP damage to the enemy, agent HP cost and time cost after each action the agent made. Details of calculation are explained in the following paragraphs.
- To get the weapon rarity data, we simulated a world of chunks with World Editor of Minecraft (MCEdit) and calculated the generation rates of different materials such as stone, iron, gold and diamond. In the 256 block tall and 16 x 16 chunks with 65,536 blocks, the rating of generation rates is Stone > Iron > Gold > Diamond, where the possibility of finding enough stones for crafting a sword is 25 times higher than that of finding an iron, 278 times higher than that of finding a gold and 928 times that of finding a Diamond. Let’s set the cost of one time attack regardless of damages C = -ln(x), where x is the possibility of finding enough materials to craft a sword based on the possibility of finding enough stones in order to reduce the huge difference. 
    |Weapons|Generation Rate|Effort needed to craft (Unit: effort to craft stone sword)|Cost = -ln(Effort)|
    |-------|-------|-------|------|
    |Wooden Sword|N/A|1|-1|
    |Stone Sword|0.0426|1|-1|
    |Bow|N/A|2|-2|
    |Iron Sword|0.0015564|25|-3.22|
    |Gold Sword|0.00014801|278|-5.36|
    |Diamond Sword|0.0000528|928|-6.83|
    ![Image Text](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure1.png)
- Analysis of the weapon durability data indicates that the rating of durability is Gold < Wood < Stone < Iron < Diamond. Let’s set the durability of gold sword as the basic case. The durability of wooden sword is 2 times longer than that of gold sword;  The durability of Arrow is 10 times longer than that of gold sword; The durability of iron is 7.6 times longer than that of gold sword; The durability of stone is 4 times longer than that of gold sword; The durability of Diamond is 47 times longer than that of gold sword. After considering the HPs of normal mobs (zombies would be killed by 5 times of close attacks) and the damages of different weapons, we set the maximum times of a weapon usage Umax = log(3y) * 20, where y is the durability of different weapons based on that of the gold sword to reduce the huge difference. 
    |Weapons|Durability|Attack Damage|Maximum times of usage = log(3*Durability) * 20|
    |-|-|-|-|
    |Wooden Sword|60|4|16|
    |Stone Sword|132|5|22|
    |Bow|384|6|30|
    |Iron Sword|251|6|27|
    |Gold Sword|33|4|10|
    |Diamond Sword|1562|7|43|
    ![Image Text](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure2.png)
- Rewards of causing damages to the enemy and receiving damages from the enemy are directly calculated by changes of health points (of Enemy or Agent) times some constant in order to increase the difference of different actions. By analyzing the attack damage data in Figure 4, we find that the advantages of greater weapons are not that strong so we modified the data to better display the differences. For instance, if the agent makes a close attack using a diamond sword and cause 7 points reduce to the enemy’s health points, then the rewards would be  3 x 7 = +21 to reward the action. However, if the agent receives damages from the enemy with 3 health points loss, then the rewards would -3 x 4 = -12 as punishment of getting hurt.
- Rewards of time cost are calculated by a linear function given that more time cost would lead to more costs. Therefore, we define T = - (0.5 + 0.1z), where z is the number of actions it has already made in order to punish more actions.
    ![Image Text](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure3.png)
- The reward calculation is applied after each action the agent had made with the function below: 
    ![Image Text](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure4.png)
### Evaluation
- The evaluation plan for this project is divided into two different aspects. One is for different monsters and another one is for different dimensional approach . When considering the aspect for different dimension, currently for this status report we make the agent only need to consider one dimensional approach, go front or go back, while in the future the agent also need to consider movement in three dimensions. For the aspect on enemie, we divided the enemies into four part. Ground close attack slow; Ground close attack fast; and flying type. Under the current one dimensional scope, we already accomplish two enemy types except flying as it move three dimensionally. Below are the result for each kind of enemy and the agent learning result.
- For the evaluation of Ground close attack slow, we choose zombie as the target. As zombie can only attack the agent in close range and it move very slow, we originally expect the agent to shoot the zombie most of the time and try to use weapon or go back when the zombie is to closed to the agent. The learning process is similar to what we expected. Here is a picture of action the agent choose to do in the beginning. 
    Beginning (n = 1): [Picture](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure5.png)
    End (n=1): [Picture](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure6.png)
- As we can see in the picture, the agent don't know anything about what to do in the beginning. However, It choose to only to shot the zombie when it is at range and use the appropriate weapon in close attack. A [video](https://youtu.be/WYGCHZLbv-M) is provided that record the learning progress for the agent. However, it does not accomplish the evaluation where it should go back when the zombie can obviously attack (distance = 1) as the agent learn so fast that it never practice close range a lot. We then try to increase our n to 10.
- Increasing the n to 10 allow us to slow down the possibility of using bow at first and increase the chance to learn close combat as the reward is not updated until at least 10 actions.
- Final when n = 10
![Picture](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure5.png)
- As we can see in this picture the agent choose to use bow when it is unable to use close attack( range of 3 ) and the action go_back is the priority when the agent is adjacent to the zombie. For the close combat weapon choice, the wooden weapon is taking the lead but not too much. In the final project we will try to modify our state or other value in order to make it more consistent. [Video](https://youtu.be/q7DSRw9kz3Y) is stated followed. 
- The next evaluation is Vindication Villager. This mod sprint when seeing the agent and have the second highest damage beside boss. We do not think that this mob is easy to kill as it may approach our agent so fast that our agent may not have enough time to make a command. So since our agent cannot sprint but the mob can, we are expecting the agent to shoot arrow at first and immediately run when the mob is chasing and try to kill the mob with a sword. Since our environment is only one dimensionally right now we are not expecting the agent to kill the mob every run but to have a similar action list as we expected. The first kill for our first run on this mob happened on the 47 round and it merely happened again. Since our eps start to decrease at rate of 0.01 after 30 round we are not satisfied with the result so we want to change our decision on eps decent. Here is a [video](https://youtu.be/rSCD-aySpaU) link for our first run if interested. 
- We modify our algorithm to change eps only on following circumstances. The eps is only changed when the agent successfully kill the mod or if not, lowered every 10 turns. By doing so the agent has more chance to experience with action as it die way quicker than facing a zombie. It have a success kill at round 20 but I think that is just a random round. The result is interesting and it does not follow our expectation but we think it has a reason behind. It choose to run when the mob is not close and choose to use sward when the zombie is within the combat range. We think the main reason our agent choose to not run is agent cannot out run the mob so that it can only choose to attack in order to have a chance to beat the mob. After 150 round with eps around 0.3, the agent has a decent chance of killing the mob than before. We consider that as a success since there is no space to run but we think our agent will achieve our expectation in our final version as it is able to run in 3 dimensions. [Video](https://youtu.be/yOX0X00f9cw) [Picture](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure8.png)
### Remaining Goals and Challenges
- Currently, the project is only consider killing a single zombie in one-dimension: we limit the space to 1*20 blocks, where the agent and the zombie are always in the same vertical line, so the agent does not have to consider turning its aiming angle. We will later expand the territory with full 20*20 block, so the aiming angle will be added to consideration. 
- To simulate more complicated real-world situations, we may add various kinds of enemies into our consideration, including in skeletons and creepers. The agent will learn to attack targets with different strategies when it faces different kinds of enemies. To achieve this, we may need to add the type of target enemy into state variable.
- Another option is to add multiple enemies into the battlefield. The enemies with various kinds will be placed in different positions, so the agent will need to adjust its view angle to aim on the enemy. In this case, the agent’s ability to aim on the desirable enemy will be crucial.
- The most challenging task in this project is to improve reward function and q-learning parameters. It is hard to properly define the cost and reward function for each weapon, the agent may choose to use an undesirable weapon after learning process. We’ve calculated reward value and maximum usage for each weapon, but they are still possible to be improved. The other challenge is to set q-learning parameters properly, including in changing learning rate and discount rate. As we mentioned above, we also need to change the epsilon value, the probability of choosing random strategy, when learning proceeds. 
### Resources Used
- Microsoft provided documentations for classes and XML schemas of Malmo. The class documentary provides library function for Malmo project. The XML schema documentary provides options of world and agent setting in mission specification XML. Viewing Malmo source code is also valuable, it provides detailed information for library functions and mission specifications.
- Minecraft Wiki is very helpful when we are doing researches on different weapons. It presents data of durability, attack damages and lifetime damage inflicted. Based on those data, we defined the reward systems more smoothly. For the rarity data, we get it manually from using MCEdit.
- For the AIML sources, we use the assignment2.py for reference given that we are also applying a Q-learning algorithm.






















