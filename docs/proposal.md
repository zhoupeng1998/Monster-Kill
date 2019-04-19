---
layout: default
title:  Proposal
---

### Summary of the Project
- Would it be nice to kill monsters with least resources and time? In this project, we will learn how to kill mobs (hostile mobs especially) in Minecraft using the most efficient weapons with least costs (health point costs, weapon durability, time costs and etc. would be considered) and dodge attacks in a closed territory (20 x 20 x 20) under a “survival” mode setting.
The input for this project are one kind of mobs and multiple weapons for choosing. The output is expected to be the best combination of weapon and actions to kill the mob with lowest cost.
Application of this project includes surviving a dark night with a large number of monsters for rookies. For advanced players, it could also help them to beat more powerful enemies, such as the Wither and the End Dragon.

### AI/ML Algorithms 
- We would like to apply Reinforcement learning with Q-learning.

### Evaluation Plan
- The metrics for our project is how many health point we can lose, what kind of monster we are able to kill(base on the weapon learning), and if killed, what should be our maximum time to kill one monster under a limit-time learning schedule. The health point we can lose is set to 8(maxim 10). The monster we will be able to kill are set to basic mobs, and the time limit we can kill that mob is set to 5 seconds(since human player can easily kill a mob(zombie I forget the word) is about 5 second. However, the baseline for this project is pretty easy. We want to train our agent to kill a pig in this mission. Since pig is unable to attack and only able to run, we only need to train on path finding and action performing. Throughout the training process, we want to decrease our health lose at least to 5 and able to kill some complicated monster in underworld. 
- Some potential basic sanity tests for this project can be given a monster, we use our own own ability to kill that monster and put our best result as the basic sanity test. The result contains our health lose, the time we use, and the weapon cost we choose. However, I believe the agent should be perform better than us thus the normal sanity test should be better. For the visualisation process we are currently considering one that is similar to the mobs_fun.py where it is a map and it show where the agent is and the monster. The map also will contain projectile throw by monster and the agent if applicable. It also contain the health data on both agent and the monster. The moonshot case for us right now could be killing a End Dragon or the Wither, since they will attack multiple blocks at the same time and sometime it is impossible for the agent to reach the Dragon at some time