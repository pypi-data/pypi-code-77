import zlib

import base64
import json
import logging

from tqdm import tqdm
from typing import Optional, Any, Dict, List, Text

import rasa.utils.io
# import rasa.shared.utils.io
# from rasa.shared.constants import DOCS_URL_POLICIES
# from rasa.shared.core.domain import State, Domain
# from rasa.shared.core.events import ActionExecuted
from rasa.core.featurizers.tracker_featurizers import (
    TrackerFeaturizer,
    MaxHistoryTrackerFeaturizer,
)
# from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.core.policies.policy import Policy, PolicyPrediction
# from rasa.shared.core.trackers import DialogueStateTracker
# from rasa.shared.core.generator import TrackerWithCachedStates
# from rasa.shared.utils.io import is_logging_disabled
from rasa.core.constants import MEMOIZATION_POLICY_PRIORITY

logger = logging.getLogger(__name__)

# temporary constants to support back compatibility
MAX_HISTORY_NOT_SET = -1
OLD_DEFAULT_MAX_HISTORY = 5

from rasa.core.policies.memoization import MemoizationPolicy

class CustomMemoizationPolicy(MemoizationPolicy):

    def __init__(
        self,
        policy_probability = 1.0,
        featurizer: Optional[TrackerFeaturizer] = None,
        priority: int = MEMOIZATION_POLICY_PRIORITY,
        max_history: Optional[int] = None,
        lookup: Optional[Dict] = None,
    ) -> None:

        super().__init__(featurizer, priority, max_history, lookup)

        self.policy_probability = policy_probability

    def predict_action_probabilities(
        self, tracker, domain
    ) -> List[float]:
        """Predicts the next action the bot should take after seeing the tracker.
        Returns the list of probabilities for the next actions.
        If memorized action was found returns 1 for its index,
        else returns 0 for all actions.
        """
        result = self._default_predictions(domain)

        if not self.is_enabled:
            return result

        tracker_as_states = self.featurizer.prediction_states([tracker], domain)
        states = tracker_as_states[0]
        logger.debug(f"Current tracker state {states}")
        recalled = self.recall(states, tracker, domain)
        if recalled is not None:
            logger.debug(
                f"There is a memorised next action '{domain.action_names[recalled]}'"
            )

            if self.USE_NLU_CONFIDENCE_AS_SCORE:
                # the memoization will use the confidence of NLU on the latest
                # user message to set the confidence of the action
                score = tracker.latest_message.intent.get("confidence", self.policy_probability)
            else:
                score = self.policy_probability

            result[recalled] = score
        else:
            logger.debug("There is no memorised next action")

        return result

    def persist(self, path: Text) -> None:

        self.featurizer.persist(path)

        memorized_file = os.path.join(path, "memorized_turns.json")
        data = {
            "priority": self.priority,
            "max_history": self.max_history,
            "lookup": self.lookup,
            "policy_probability": self.policy_probability,
        }
        rasa.utils.io.create_directory_for_file(memorized_file)
        rasa.utils.io.dump_obj_as_json_to_file(memorized_file, data)

    @classmethod
    def load(cls, path: Text) -> "CustomMemoizationPolicy":

        featurizer = TrackerFeaturizer.load(path)
        memorized_file = os.path.join(path, "memorized_turns.json")
        if os.path.isfile(memorized_file):
            data = json.loads(rasa.utils.io.read_file(memorized_file))
            return cls(
                policy_probability=data["policy_probability"],featurizer=featurizer, priority=data["priority"], lookup=data["lookup"]
            )
        else:
            logger.info(
                "Couldn't load memoization for policy. "
                "File '{}' doesn't exist. Falling back to empty "
                "turn memory.".format(memorized_file)
            )
        return cls()
