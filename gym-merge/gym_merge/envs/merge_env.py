import gym
from gym import error, spaces, utils
from gym.utils import seeding

import gym_merge.envs.utils as merge_utils
import numpy as np

# accel to apply for each action
ACTION_LOOKUP = {
    0 : -1.0,
    1 : 0.0,
    2 : 1.0,
}

DT = 0.5

def get_state(ego_actor, merging_actor):
  return np.array([ego_actor.s, ego_actor.v, merging_actor.s, merging_actor.v])

class MergeEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.action_space = spaces.Discrete(3)
    # e.s, e.v, o.s, o.v
    self.observation_space = spaces.Box(low=np.array([-200.0, 0.0, -200.0, 0.0]),
                                        high=np.array([200.0, 40.0, 200.0, 40.0]))
    self.ego_actor = merge_utils.Actor()
    self.merging_actor = merge_utils.Actor()
    self.t = 0.0
    # ego s,v, object s,v
    self.state = get_state(self.ego_actor, self.merging_actor)

  def step(self, action):
    accel = ACTION_LOOKUP[action]
    self.ego_actor.step(accel, DT)
    self.merging_actor.step(0.0, DT)
    self.t += DT
    self.state = get_state(self.ego_actor, self.merging_actor)

    reward = merge_utils.get_reward(self.state, accel)
    episode_over = merge_utils.episode_over(self.state, self.t)
    return self.state, reward, episode_over, {}

  def reset(self):
    self.__init__()
  def render(self, mode='human'):
    # think about how to render this
    return
  def close(self):
    return
