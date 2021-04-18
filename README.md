### Notes
- Trying to use OpenAI gym, working through dependency issues.
- Seems like gym does not support python 3.9 because of a dependency: https://github.com/openai/gym/issues/2203
- python3.7.10 had no issues
- making your own environment:https://github.com/openai/gym/blob/master/docs/creating-environments.md
- openai gym baselines: https://github.com/openai/baselines
- When building baselines: gym 0.15.7 has requirement cloudpickle~=1.2.0, but you'll have cloudpickle 1.6.0 which is incompatible.
- Just downgraded cloudpickle to required package.