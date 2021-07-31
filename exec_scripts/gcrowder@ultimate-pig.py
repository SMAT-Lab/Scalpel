#!/usr/bin/env python
# coding: utf-8
# In[1]:
get_ipython().run_line_magic('matplotlib', 'inline')
import random
import statistics as st
import numpy as np
import matplotlib.pyplot as plt
# In[2]:
class Player:
    def __init__(self):
        self.total = 0
        self.last_roll = 0
    def is_roll_again(self, turn):
        return False
# In[11]:
class EagerPlayer(Player):
    def is_roll_again(self, turn):
        if self.last_roll == 1:
            return False
        elif turn == 0 or self.total < 10:
            return True
        elif self.total / turn < 15:
            return True
        else:
            return False
# In[4]:
class ArbitraryPlayer(Player):
    def is_roll_again(self, turn):
        if self.last_roll == 1:
            return False
        else:
            return random.choice([True, False])
# In[5]:
class OverlyCautiousPlayer(Player):
    def is_roll_again(self, turn):
        if self.last_roll == 1:
            return False
        elif turn == 0 or self.total < 4:
            return True
        elif self.total / turn > 4:
            return False
        else:
            return True
# In[7]:
def roll_die():
    return random.randint(1, 6)
def play(player):
    total = player.total
    roll = roll_die()
    player.last_roll = roll
    if roll == 1:
        return total
    else:
        total += roll
        return total
def game_loop(player):
    result = 0
    for turn in range(7):
        result = play(player)
        player.total = result
        while player.is_roll_again(turn):
            result = play(player)
            player.total = result
    return player.total
# In[26]:
trials = 1000
player_class_trials = []
for _ in range(trials):
    bob = Player()
    player_class_trials.append(game_loop(bob))
player_mean = st.mean(player_class_trials)
player_median = st.median(player_class_trials)
player_stdev = st.stdev(player_class_trials)
print("Player Mean: ", player_mean)
print("Player Median: ", player_median)
print("Player StDev: ", player_stdev)
plt.figure(1)
plt.boxplot(player_class_trials)
plt.ylabel('Game Score')
plt.show()
eager_player_trials = []
for _ in range(trials):
    sally = EagerPlayer()
    eager_player_trials.append(game_loop(sally))
eager_mean = st.mean(eager_player_trials)
eager_median = st.median(eager_player_trials)
eager_stdev = st.stdev(eager_player_trials)
print("Eager Player Mean: ", eager_mean)
print("Eager Player Median: ", eager_median)
print("Eager Player StDev: ", eager_stdev)
plt.figure(2)
plt.boxplot(eager_player_trials)
plt.ylabel('Game Score')
plt.show()
arbitrary_player_trials = []
for _ in range(trials):
    june = ArbitraryPlayer()
    arbitrary_player_trials.append(game_loop(june))
arbitrary_mean = st.mean(arbitrary_player_trials)
arbitrary_median = st.median(arbitrary_player_trials)
arbitrary_stdev = st.stdev(arbitrary_player_trials)   
print("Arbitrary Player Mean: ", arbitrary_mean)
print("Arbitrary Player Median: ", arbitrary_median)
print("Arbitrary Player StDev: ", arbitrary_stdev)
plt.figure(3)
plt.boxplot(arbitrary_player_trials)
plt.ylabel('Game Score')
plt.show()
overly_cautious_trials = []
for _ in range(trials):
    melvin = OverlyCautiousPlayer()
    overly_cautious_trials.append(game_loop(melvin))
overly_cautious_mean = st.mean(overly_cautious_trials)
overly_cautious_median = st.median(overly_cautious_trials)
overly_cautious_stdev = st.stdev(overly_cautious_trials)
print("Overly Cautious Player Mean: ", overly_cautious_mean)
print("Overly Cautious Player Median: ", overly_cautious_median)
print("Overly Cautious Player StDev: ", overly_cautious_stdev)
plt.figure(4)
plt.boxplot(overly_cautious_trials)
plt.ylabel('Game Score')
plt.show()
plt.figure(5)
plt.pie([player_mean, eager_mean, arbitrary_mean, overly_cautious_mean], labels=['Player Mean', 'Eager Mean', 'Arbitrary Mean', 'Overly Cautious Mean'], colors=('b', 'r', 'c', 'm'))
plt.show()
plt.figure(6)
plt.pie([player_stdev, eager_stdev, arbitrary_stdev, overly_cautious_stdev], labels=['Player Standard Deviation', 'Eager Standard Deviation', 'Arbitrary Standard Deviation', 'Overly Cautious Standard Deviation'], colors=('b', 'r', 'c', 'g'))
plt.show()