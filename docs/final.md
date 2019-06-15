---
layout: default
title:  Final Report
---

### Video
LINK HERE

### Project Summary
- Is it frustrating to be in trouble of the high damage taken by enemies in a dark night? Would it be nice to kill monsters smartly with less time and resources? Finding the best way to beat enemies with the lowest resource and damage taken cost is not easy for new Minecraft players, but we can use AI to learn an optimal policy to kill monsters.
- In Monster Killer project, we place a Minecraft agent in an open plain terrain with one hostile mob and multiple available weapons to let the agent kill the mob with least count of actions and health costs.
- The application of this project serves as a guide for players in survival mode. For new players, it teaches them how to beat monsters efficiently. For advanced players, it helps them to beat more powerful enemies and bosses.


### Approach
#### Q-Learning
- The Monster Killer project applies reinforcement learning with Q-learning algorithm. With Q-learning, agent learns a policy that maximizes the reward by choosing the best action in each step. We create a Q-table to store reward of all actions in each state. During the learning process, we use a function to update Q-table with its output reward. The Q-learning function has two inputs: state and action, it returns the expected reward according to the action the agent performed in current state. The learning process contains following steps:
  - Initialize Q-table
  - Loop until learning stops:
    - Choose an action in current state based on current value in Q-table
    - Perform the action and observe the outcome
    - Update Q-table
- When the agent starts learning, all values in Q-table are zero, the best action is unknown, so we must weigh exploration and exploitation rate properly. We use epsilon greedy policy: when the agent chooses an action, it generates a random number. If the number is greater than epsilon, it will exploit the known information by choosing the action with the best expected reward; otherwise, it will explore by choosing a random action. 
- We set epsilon to be 0.5 when the agent begins learning. Starting at the 50th round, we decrease epsilon by 0.1 at the end of each episode until it reaches zero. Then we continue to learn for 50 more episodes before the agent stops learning.
- We update Q-table after an episode of all actions. The updated Q-value for an action in a state is affected by the discounted cumulative reward given the state and action. Here is an image for the equation below:
    ![Image Text](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/final-img/fig1.png)

#### State Define
- We define states with three factors:
  1. Absolute straight line distance between the agent and the enemy. We discretize the distance value into 6 close range values (0, 1, 2, 3, 4, 5) and 4 long range values (5-10, 10-15, 15-20, 20+).
  2. Life point left by the agent. The agent could act differently according to their life point status. We discretize life points into 4 states of string values: “Full” for 15-20; “High” for 10-15, “Medium” for 5-10; “Low” for 5 or below.
  3. A binary variable for whether the agent is facing the enemy. We expect the agent learn to turn to face the enemy when the agent is not facing it.
- In total, there are 10*4*2 = 80 states possible.

#### Actions Define
- We provide the agent with a bow and two kinds of swords. With the bow, the agent can shoot arrows with two different time to draw the bow: 0.4 or 0.7 seconds, which makes different damage and range of shooting. The agent can attack front using wooden sword or diamond sword. The agent can also move forward or backward for one distance unit. If the agent is not facing the enemy, it can make action to aim on the enemy. In total, there are total 7 actions for each state. 

#### Rewards Setting
- CONSTRUCTING

### Evaluation
- We evaluate our project with four aspects: number of actions, attack accuracy (the percentage that agent attack hits the enemy with positive reward), reward per action, and life points remaining. 
- We generally expect the number of actions becomes lower, and the rest of the measurements to be higher gradually during the learning process. We also expect the number to become stable with more rounds of learning.
- We evaluate the performance of the AI with several kinds of enemies.
- Evaluation results: CONSTRUCTING


### Resources Used
- Microsoft provided documentations for classes and XML schemas of Malmo. The class documentary provides library function for Malmo project. The XML schema documentary provides options of world and agent setting in mission specification XML. Viewing Malmo source code is also valuable, it provides detailed information for library functions and mission specifications.
- Minecraft Wiki is very helpful when we are doing researches on different weapons. It presents data of durability, attack damages and lifetime damage inflicted. Based on those data, we defined the reward systems more smoothly. For the rarity data, we get it manually from using MCEdit.
- For the AIML sources, we use the assignment2.py for reference given that we are also applying a Q-learning algorithm.






















