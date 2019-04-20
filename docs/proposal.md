---
layout: default
title:  Proposal
---

### Summary of the Project
- Would it be nice to kill monsters with least resources and time? In this project, we will learn how to kill mobs (hostile mobs especially) in Minecraft using the most efficient weapons with least costs (health point costs, weapon durability, time costs and etc. would be considered) and dodge attacks in a closed territory (20 x 20 x 20) under a “survival” mode setting.
The input for this project are one kind of mobs and multiple weapons for choosing. The output is expected to be the best combination of weapon and actions to kill the mob with lowest cost.
Application of this project includes surviving a dark night with a large number of monsters for rookies. For advanced players, it could also help them to beat more powerful enemies, such as the Wither and the End Dragon.

### AI/ML Algorithms 
- We would like to apply Reinforcement learning with Q-learning and neural network.

### Evaluation Plan
- The metrics for our project include how many health points we can lose; which kinds of mobs we are able to kill (based on the weapon learning); and if killed the mob successfully, what should be our maximum time to finish this process under a limit-time learning schedule. The health point we can lose is set to 8 (with the maximum be set to 10). The monsters we will be able to kill include all basic mobs (hostile mobs especially). The time limit we should complete killing that mob is set to 5 seconds since human players can kill some kinds of basic mobs like zombies in about 5 second. However, the baseline for this project is relatively easier than the final expectation. We would train our agent to kill a passive mob such as pig or rabbit as the first stage of this mission. Since passive mobs are unable to attack players but escape from attacks from players, we would focus on training the path of finding and following a mob target and actions for attacks. Throughout the training process, we expect to improve by killing more complicated mobs like hostile mobs in the underworld along with a lower HP cost setting (from 8 to 5,  or even less).
- Some potential basic sanity tests for this project can be set as following:
given a specific monster, we would record the data (HP lose, time cost and weapon cost) of human players killing the monster as a basic standards for our projects — it could be hard to find the average data for general users, so we would assume our group members as general users and record our own data for comparison. For the visualization process, we would like to build one that is similar to the visualization in mobs_fun.py, which is a map of the overall territory and indicates the location of agent and the monster. The map also will contain projectile throw by monster and the agent if applicable. The visualization should also contain the HP data on both agent and the monster. The moonshot case for us right now could be killing a End Dragon or the Wither, since they will attack multiple blocks at the same time and sometime it is impossible for the agent to reach the Dragon.

### Appointment
- The upcoming appointment is schedule for 01:30pm on Thursday, April 25, 2019.
