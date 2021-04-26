import gym

from stable_baselines3 import PPO, DQN

env = gym.make('gym_merge:merge-v0')
# env = gym.make("CartPole-v1")


model = DQN("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        env.render()
        print(observation)
        # action = env.action_space.sample()
        action, _states = model.predict(observation, deterministic=True)
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
