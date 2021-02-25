"""Loads trained policies for rollout in structured environments."""
from typing import Union, Dict

import torch
from maze.core.agent.torch_policy import TorchPolicy
from maze.core.utils.registry import Registry
from maze.perception.models.model_composer import BaseModelComposer
from maze.perception.models.space_config import SpacesConfig
from omegaconf import DictConfig


class SerializedTorchPolicy(TorchPolicy):
    """Structured policy used for rollouts of trained models.

    Will build the models based on the model composer and spaces config and set the state of individual
    policies according to the state dict dump.

    Policies are set to eval mode by default.

    :param model: Model composer configuration
    :param state_dict_file: Path to dumped state dictionaries of the trained policies
    :param spaces_dict_file: Path to dumped spaces configuration (action and observation spaces of
                                  the env the policy was trained on, used for model initialization)
    """

    def __init__(self, model: Union[DictConfig, Dict], state_dict_file: str, spaces_dict_file: str, device: str):
        spaces_config = SpacesConfig.load(spaces_dict_file)
        model_composer = Registry(base_type=BaseModelComposer).arg_to_obj(
            model,
            action_spaces_dict=spaces_config.action_spaces_dict,
            observation_spaces_dict=spaces_config.observation_spaces_dict
        )

        super().__init__(networks=model_composer.policy.networks,
                         distribution_mapper=model_composer.distribution_mapper,
                         device=device)

        state_dict = torch.load(state_dict_file, map_location=torch.device(self._device))

        self.load_state_dict(state_dict)
        self.eval()
