import functools
from typing import Any, Callable, List, Literal, Mapping, Optional, Sequence, Tuple, Type, TypedDict, Union
from .funcs import composed

class BuildError(Exception):
    def __init__(self, build_step: Callable, message: str, *args: object) -> None:
        self.build_step = build_step
        self.message = message
        super().__init__(*args)


class BuilderError(Exception):
    """Exception throw by a builder instance"""


class BuildState(object):
    """Parent for a build object state"""
    error_message: str = 'Cannot {}, build already {}'
    build_result: str = ''

    def __init__(self, builder: 'Builder') -> None:
        self.builder = builder
        super().__init__()

    def _raise_builder_error(self, verb: str) -> None:
        message = self.error_message.format(
            verb, self.build_result
        )
        raise BuilderError(message)

    def build_step(self) -> 'BuildStepDecorator':
        self._raise_builder_error('add build step')

    def build(self) -> None:
        self._raise_builder_error('run build')


class BuildFinishedState(BuildState):
    """
    Parent class to determine if build is completed or completed with errors
    Can also use to define custom finished states as well
    """


class BuildCompleteState(BuildFinishedState):
    """Indicates that the auto build sequence is completed"""
    build_result = 'completed'


class BuildErrorState(BuildFinishedState):
    """Indicates that the auto build sequence has failed"""
    build_result = 'completed with errors'


class BuildRunningState(BuildState):
    """Indicates that the auto build sequence is running"""
    build_result = 'running'


BuildStepCallable = Callable[..., Union[Any, 'Builder']]
BuildStepDecorator = Callable[[BuildStepCallable], BuildStepCallable]
BuildStepResultCallable = Callable[[Any], None]
BuildStepProgressCallable = Callable[[float], None]

class BuildConfigureState(BuildState):
    """Indicates that the auto build sequence has not been started"""

    def build_step(self):
        """
        Counts each method decorated with this decorator and saves the function to the
        step queue
        """
        def decorator(func: BuildStepDecorator) -> BuildStepCallable:
            @functools.wraps(func)
            def decorated(*args, **kwargs):
                self.builder._executed_steps += 1
                ret = func(*args, **kwargs)
                return ret
            self.builder.steps_list.append(decorated)
            return decorated
        return decorator

    def build(self) -> None:
        self.builder.set_state(BuildRunningState)
        for fnc in self.builder.steps_list:
            try:
                res = fnc()
            except Exception as ex:
                raise BuildError(fnc, *ex.args) from ex
            if isinstance(res, Builder):
                res(
                    progress_weight=self.builder.steps,
                    previous_progress=(self.builder.executed_steps - 1) / self.builder.steps
                )
        self.builder.set_state(BuildCompleteState)


class Builder(object):
    def __init__(
            self,
            initial_state: Optional[Type[BuildState]] = None,
            **states: Type[BuildState]
    ) -> None:

        default_states = {
            'configure': BuildConfigureState,
            'running': BuildRunningState,
            'error': BuildErrorState,
            'complete': BuildCompleteState,
        }
        default_states.update(states)
        self.configured_states = default_states
        self._steps: List[BuildStepCallable] = []
        self._sub_steps: List[Builder] = []
        self._executed_steps: int = 0
        self._progress_weight: float = 1.0
        self._previous_progress: float = 0
        if initial_state is not None:
            self.set_state(initial_state)
        else:
            self.set_configured_state('configure')

    def set_configured_state(self, state_name: Literal['configure', 'running', 'error', 'complete']):
        self._state = self.configured_states[state_name](self)

    def set_state(self, state: Type[BuildState]) -> None:
        self._state = state(self)

    @property
    def steps(self) -> int:
        return len(self._steps)

    @property
    def steps_list(self) -> List[BuildStepCallable]:
        return self._steps

    @property
    def executed_steps(self) -> int:
        return self._executed_steps

    @property
    def progress(self) -> float:
        return self._previous_progress + (self.executed_steps / self.steps / self._progress_weight)

    @property
    def is_complete(self):
        return isinstance(self._state, BuildFinishedState)

    @property
    def state(self) -> BuildState:
        return self._state

    def build(self, progress_weight: float = 1, previous_progress: float = 0) -> None:
        try:
            self._progress_weight = progress_weight
            self._previous_progress = previous_progress
            self._state.build()
        except BuildError as ex:
            self.set_configured_state('error')
            raise ex

    def __call__(self, **kwargs) -> None:
        return self.build(**kwargs)

    def build_step(self) -> BuildStepCallable:
        """
        Counts each method decorated with this decorator and saves the function to the
        step queue. Should be this first decorator in the decorator stack.
        """
        return self._state.build_step()

    def capture_results(self, *args: BuildStepResultCallable) -> BuildStepDecorator:
        """Calls each function in *args with the result of the decorated function"""
        output_functions = args

        def decorator(func):
            @functools.wraps(func)
            def decorated(*args, **kwargs):
                ret = func(*args, **kwargs)
                if not isinstance(ret, Builder):
                    for output_func in output_functions:
                        output_func(ret)
                return ret
            return decorated
        return decorator

    def capture_progress(self, *args: BuildStepProgressCallable) -> BuildStepDecorator:
        """Calls each function in *args with the
        result of ```executed steps / steps```"""
        progress_functions = args

        def decorator(func):
            @functools.wraps(func)
            def decorated(*args, **kwargs):
                ret = func(*args, **kwargs)
                if not isinstance(ret, Builder):
                    for progress_func in progress_functions:
                        progress_func(self.progress)
                return ret
            return decorated
        return decorator

    def composed_step(self, *decorators: BuildStepDecorator) -> BuildStepDecorator:
        """Used to compose a decorator. Useful for defining specific
        outputs and progress reports to a build step and resusing"""
        decorator_list = list(decorators)
        decorator_list.insert(0, self.build_step())
        decorated = composed(*decorator_list)
        return decorated
