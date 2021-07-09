import gym
import numpy as np
from collections import defaultdict
import functools
from tqdm import tqdm_notebook
def generate_zeros(n):
    return [0] * n


class TabularQAgent(object):
    def __init__(self, observation_space, action_space):
        self.observation_space = observation_space
        self.action_space = action_space
        self.action_n = action_space.n
        self.config = {
            "learning_rate": 0.5,
            "eps": 0.5,            # Epsilon in epsilon greedy policies
            "discount": 0.99,
            "n_iter": 10000}        # Number of iterations

        self.q = defaultdict(functools.partial(generate_zeros, n=self.action_n))

    def act(self, observation, eps=None):
        if eps is None:
            eps = self.config["eps"]      
        # epsilon greedy.
        action = np.argmax(self.q[observation]) if np.random.random() > eps else self.action_space.sample()
        return action

    def learn(self, env):
        obs = env.reset()

        rAll = 0
        step_count = 0

        for t in range(self.config["n_iter"]):
            action = self.act(obs)
            obs2, reward, done, _ = env.step(action)

            future = 0.0
            if not done:
                future = np.max(self.q[obs2])
            self.q[obs][action] = (1 - self.config["learning_rate"]) * self.q[obs][action] + self.config["learning_rate"] * (reward + self.config["discount"] * future)

            obs = obs2

            rAll += reward
            step_count += 1

            if done:
                break

        return rAll, step_count

    def test(self, env):
        obs = env.reset()
        env.render(mode='human')

        for t in range(self.config["n_iter"]):
            env.render(mode='human')

            action = self.act(obs, eps=0)
            obs2, reward, done, _ = env.step(action)
            env.render(mode='human')

            if done:
                break

            obs = obs2
def train(tabular_q_agent, env):
    for episode in tqdm_notebook(range(200000)):
        all_reward, step_count = tabular_q_agent.learn(env)
env = gym.make('FrozenLake-v0')
env.seed(0)  # 确保结果具有可重现性

tabular_q_agent = TabularQAgent(env.observation_space, env.action_space)
train(tabular_q_agent, env)
tabular_q_agent.test(env)
