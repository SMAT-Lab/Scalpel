#!/usr/bin/env python
# coding: utf-8
# In[1]:
import time
import numpy as np
from math import sqrt, log
from abc import ABCMeta, abstractmethod
from collections import defaultdict
# In[2]:
class BAMCP(object, metaclass=ABCMeta):
    actions = None
    states = None
    max_reward = None
    def __init__(self, discount=0.95, epsilon=0.5, exploration=3):
        self.discount = discount
        self.epsilon = epsilon
        self.exploration = exploration
        self.N = None
        self.Q = None
    @abstractmethod
    def mdp_dist(self, history):
        """Sampling distribution for MDPs. Must be overwritten by subclasses."""
        pass
    @abstractmethod
    def reward_func(self, state, action, mdp):
        """Reward function for the given state/action. Must be overwritten
        by subclasses."""
        pass
    @abstractmethod
    def transition_func(self, state, action, mdp):
        """Transition function for the given state/action. Must be overwritten
        by subclasses."""
        pass
    @abstractmethod
    def valid_actions(self, state, mdp):
        """Returns a list of valid actions that can be taken in the given
        state. Must be overwritten by subclasses."""
        pass
    def rollout_policy(self, state, history, mdp):
        """Uniform rollout policy."""
        actions = self.valid_actions(state, mdp)
        if len(actions) == 0:
            return None
        else:
            return np.random.choice(actions)
    def tree_policy(self, state, history, mdp):
        """UCT tree policy."""
        actions = self.valid_actions(state, mdp)
        if len(actions) == 0:
            return None
        elif len(actions) == 1:
            return actions[0]
        N = self.N[(state, history)]
        values = np.empty(len(actions))
        for i in range(len(actions)):
            Q = self.Q[(state, history)][actions[i]]
            Ni = self.N[(state, history, actions[i])]
            if Ni == 0:
                values[i] = np.inf
            else:
                values[i] = Q + self.exploration * sqrt(log(N / Ni))
        return np.random.choice(actions[values == np.max(values)])
    def value_func(self, state, history):
        """Returns the value of the given state, as well as the best action to take."""
        actions = list(self.Q[(state, history)].keys())
        values = np.empty(len(actions))
        for i in range(len(actions)):
            values[i] = self.Q[(state, history)][actions[i]]
        if len(actions) == 1:
            return values[0], actions[0]
        idx = np.random.choice(np.nonzero(values == np.max(values))[0])
        return values[idx], actions[idx]
    def search(self, state, history, max_time=1):
        """Run a search from the root of the tree. Return the value of the root
        and the next action to take.
        """
        self.N = defaultdict(lambda: 0)
        self.Q = defaultdict(lambda: defaultdict(lambda: 0))
        t = time.time()
        while (time.time() - t) < max_time:
            self.simulate(state, history, self.mdp_dist(history))
        return self.value_func(state, history)
    def rollout(self, state, history, mdp, depth):
        """Execute a rollout simulation from a leaf node in the tree."""
        if state is None:
            return 0
        if (self.discount ** depth * self.max_reward) < self.epsilon:
            return 0
        action = self.rollout_policy(state, history, mdp)
        new_state = self.transition_func(state, action, mdp)
        new_history = history + ((state, action, new_state),)
        curr_reward = self.reward_func(state, action, mdp)
        future_reward = self.rollout(new_state, new_history, mdp, depth + 1)
        reward = curr_reward + self.discount * future_reward
        return reward
    def simulate(self, state, history, mdp, depth=0):
        """Simulate an episode from the given state, following the tree policy
        until a leaf node is reached, at which point the rollout policy is used.
        """
        if state is None:
            return 0
        if (self.discount ** depth * self.max_reward) < self.epsilon:
            return 0
        # leaf node
        if self.N[(state, history)] == 0:
            action = self.rollout_policy(state, history, mdp)
            new_state = self.transition_func(state, action, mdp)
            new_history = history + ((state, action, new_state),)
            curr_reward = self.reward_func(state, action, mdp)
            future_reward = self.rollout(new_state, new_history, mdp, depth)
            reward = curr_reward + self.discount * future_reward
            self.N[(state, history)] = 1
            self.N[(state, history, action)] = 1
            self.Q[(state, history)][action] = reward
        # non-leaf node
        else:
            action = self.tree_policy(state, history, mdp)
            new_state = self.transition_func(state, action, mdp)
            new_history = history + ((state, action, new_state),)
            curr_reward = self.reward_func(state, action, mdp)
            future_reward = self.simulate(new_state, new_history, mdp, depth + 1)
            reward = curr_reward + self.discount * future_reward
            self.N[(state, history)] += 1
            self.N[(state, history, action)] += 1
            dQ = (reward - self.Q[(state, history)][action]) / self.N[(state, history, action)]
            self.Q[(state, history)][action] += dQ
        return reward
# In[3]:
class ToyBAMCP(BAMCP):
    actions = np.array([0, 1])
    states = np.array([0, 1, 2, 3, 4, 5])
    max_reward = 2
    def __init__(self, p, *args, **kwargs):
        super(ToyBAMCP, self).__init__(*args, **kwargs)
        self.p = p
        self.MDP1 = np.zeros((6, 2, 6))
        self.MDP1[0, 1, 5] = 1
        self.MDP1[0, 0, 1] = 0.8
        self.MDP1[0, 0, 2] = 0.2
        self.MDP1[1, 0, 3] = 1
        self.MDP1[1, 1, 4] = 1
        self.MDP1[2, 0, 4] = 1
        self.MDP1[2, 1, 3] = 1
        self.MDP2 = np.zeros((6, 2, 6))
        self.MDP2[0, 1, 5] = 1
        self.MDP2[0, 0, 1] = 0.2
        self.MDP2[0, 0, 2] = 0.8
        self.MDP2[1, 0, 4] = 1
        self.MDP2[1, 1, 3] = 1
        self.MDP2[2, 0, 3] = 1
        self.MDP2[2, 1, 4] = 1
    def mdp_dist(self, history):
        p1 = self.p
        p2 = 1 - self.p
        for sas in history:
            p1 *= self.MDP1[sas]
            p2 *= self.MDP2[sas]
        Z = p1 + p2
        p1 = p1 / Z
        p2 = p2 / Z
        if np.random.rand() < p1:
            return self.MDP1
        else:
            return self.MDP2
    def reward_func(self, state, action, mdp):
        if state == 3:
            return 2
        elif state == 4:
            return -2
        else:
            return 0
    def transition_func(self, state, action, mdp):
        p = mdp[state, action]
        if (p == 0).all():
            return None
        return np.random.choice(self.states, p=p)
    def valid_actions(self, state, mdp):
        ok = ~((mdp[state] == 0).all(axis=1))
        if not ok.any():
            return np.array([])
        else:
            return self.actions[ok]
# In[4]:
planner = ToyBAMCP(0.5)
# In[5]:
state = 0
history = tuple()
planner.search(0, history)
# In[6]:
state = 1
history = ((0, 0, 1),)
planner.search(state, history)
# In[7]:
state = 3
history = ((0, 0, 1), (1, 0, 3))
planner.search(state, history)