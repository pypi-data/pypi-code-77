"""Contains a dictionary observation space wrapper."""
import gym
import numpy as np

from maze.core.wrappers.wrapper import ObservationWrapper


class DictObservationWrapper(ObservationWrapper[gym.Env]):
    """Wraps a single observation into a dictionary space.
    """

    def __init__(self, env):
        super().__init__(env)
        self.observation_space = gym.spaces.Dict({"observation": env.observation_space})

    def observation(self, observation: np.ndarray):
        """Implementation of :class:`~maze.core.wrappers.wrapper.ObservationWrapper` interface.
        """
        return {"observation": observation.astype(np.float32)}
