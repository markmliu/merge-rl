import gym
import time

from stable_baselines3 import PPO, DQN

env = gym.make('gym_merge:merge-v0')
# env = gym.make("CartPole-v1")

# TODO: do an eval of PPO vs DQN.
# DQN seems to do a bit worse for the first case i tried, but need to vary initial states a bit more.
# model = PPO("MlpPolicy", env, verbose=1)
model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

for i_episode in range(20):
    observation = env.reset()
    total_reward = 0
    for t in range(100):
        env.render()
        #time.sleep(0.1)
        print(observation)
        # action = env.action_space.sample()
        action, _states = model.predict(observation, deterministic=True)
        observation, reward, done, info = env.step(action)
        total_reward += reward
        if done:
            print ("total reward {}".format(total_reward))
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
