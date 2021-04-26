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
    self.viewer = None

  def step(self, action):
    err_msg = "%r (%s) invalid" % (action, type(action))
    assert(self.action_space.contains(action), err_msg)

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
    return get_state(self.ego_actor, self.merging_actor)

  def render(self, mode='human'):
    # mostly copied from cartpole-v1 example: https://github.com/openai/gym/blob/master/gym/envs/classic_control/cartpole.py
    screen_width = 600
    screen_height = 400

    if self.viewer is None:
      from gym.envs.classic_control import rendering
      self.viewer = rendering.Viewer(screen_width, screen_height)
      self.ego_circle = rendering.make_circle(10.0)
      self.ego_circle.set_color(.5,.5,.8)
      self.egotrans = rendering.Transform()
      self.ego_circle.add_attr(self.egotrans)
      self.viewer.add_geom(self.ego_circle)

      self.merging_circle = rendering.make_circle(10.0)
      self.merging_circle.set_color(.8,.8,.5)
      self.mergingtrans = rendering.Transform()
      self.merging_circle.add_attr(self.mergingtrans)
      self.viewer.add_geom(self.merging_circle)

      self.critical_line = rendering.make_polyline([(250.0,200.0), (350.0, 200.0)])
      self.viewer.add_geom(self.critical_line)

    if self.state is None:
      return None

    # ego road goes up from middle of the screen
    self.egotrans.set_translation(250.0, self.ego_actor.s + 200.0)

    self.mergingtrans.set_translation(350.0, self.merging_actor.s + 200.0)

    return self.viewer.render(return_rgb_array=mode == 'rgb_array')
  def close(self):
    if self.viewer:
      self.viewer.close()
      self.viewer = None
    return
