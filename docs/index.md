---
layout: default
title:  Home
---

Would it be nice to kill monsters with least resources and time? In this project, the agent will learn how to kill mobs (hostile mobs especially) in Minecraft using the most efficient weapon combinations with least costs (health point costs, weapon durability, weapon craft costs,  time costs and etc. would be considered) and dodge attacks in a closed territory (20 x 20) under a “survival” mode setting. We would provide one kind of hostile mobs and multiple weapons as input while the output is expected to be the best combination of weapons and actions to kill the mob with lowest cost.

Our goal is to let Minecraft agent to learn the most efficient way to kill different kinds and numbers of enemies. We apply reinforcement learning with Q-learning to solve this problem.

Source code: [https://github.com/zhoupeng1998/Monster-Kill](https://github.com/zhoupeng1998/Monster-Kill)

Authors:
- Jiashuo Liu - jiashul2 AT uci D0T edu
- Wenyu Ouyang - wenyuo AT uci D0T edu
- Peng Zhou - pzhou2 AT uci D0T edu

Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- Final - Comming soon

Videos:

- Status Report - Video below

[![Video](https://i9.ytimg.com/vi/CpJ8CY-qIeU/mq2.jpg?sqp=CMCRpOcF&rs=AOn4CLADLw5eVkYs1x7LANwizMZJJ72w1Q)](https://youtu.be/CpJ8CY-qIeU)
- [Learning to attack a Zombie, with n=1](https://youtu.be/WYGCHZLbv-M)
- [Learning to attack a Zombie, with n=10](https://youtu.be/q7DSRw9kz3Y)
- [Learning to attack a Vindication Villager](https://youtu.be/rSCD-aySpaU)
- [Learning to attack a Vindication Villager, modified](https://youtu.be/yOX0X00f9cw)

We attempted to let agent learn to attack zombies and vindication villagers. After several rounds of learning, the agent could choose disirable actions to make movements or to attack with different weapons according to its state. Here's a screenshot during the learning process. 
![Picture](https://raw.githubusercontent.com/zhoupeng1998/Monster-Kill-Resource/master/img/figure7.png)
    

