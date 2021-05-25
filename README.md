### Description

This sets up a very simple OpenAI gym `merge_env` imitating a "forced-merge" road scenario.
One actor is initialized in the merging lane with a random travel and velocity and continues at constant velocity.
The observation space is the actor `s,v` and merging object `s,v`.
The action space is a discrete acceleration to the ego vehicle `-1.0, 0.0, 1.0` and the environment steps forward with `dT = 0.5`

TODO: Add option to gym to allow merging actors to move following different motion models.

### Notes
- Seems like gym does not support python 3.9 because of a dependency: https://github.com/openai/gym/issues/2203. python3.7.10 had no issues
- Made environment using tutorial:https://github.com/openai/gym/blob/master/docs/creating-environments.md
- Training using stable_baselines3: https://github.com/DLR-RM/stable-baselines3