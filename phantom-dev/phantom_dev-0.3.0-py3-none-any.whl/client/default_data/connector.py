"""
A basic Phantom App connector implementation.

Customise the Connector class using `ActionHandler` methods, or define your
own implementation.
"""
from phantom_dev.action_handler import ActionHandler, contains, smart_connector


@contains('text')
class Text(str):
    """A string-based type that contains ['text']"""


@contains('url')
class Url(str):
    """A string-based type that contains ['url']"""


@smart_connector
class Connector:
    """
    Use a class decorated with `smart_connector` as a simple way to implement
    a Phantom App connector.

    Decorate member functions with `@ActionHandler` to register them as action
    handler methods.
    Handler methods should accept the `context` keyword argument and whichever
    parameters the action requires to run.
    Parameter annotations can be used to infer the parameter type if they are
    Python primitives (`int`, `float`, `str`, or `bool`).
    Handler docstrings can similarly be used to infer the description of each
    action.
    Parameter default values are reflected in the metadata, and are also used
    to infer whether a parameter is mandatory.

    Handler methods should return iterables of result data dictionaries.
    They can return iterables as functions, or be implemented as data
    dictionary generators.
    See the `test_connectivity` and `dummy_generator` methods below for
    examples of each approach.

    Once an action handler method has been defined and decorated with
    `@ActionHandler`, the handler method has a member called `summary` that
    can be used to register another method as the action summary method.
    The action summary method should take an iterable of the results from the
    handler method and return an action result summary dict.
    See the `summarise` method for an example using the `dummy_action` handler
    method to register it as the summary method for `dummy_action`.

    As a result of using `smart_connector`, this class inherits from
    `phantom.base_connector.BaseConnector`, as well as implementing the testing
    interface when this module is run as the main script.

    See the official Phantom documentation for information about
    `phantom.base_connector.BaseConnector` and its members.
    """

    @ActionHandler
    def test_connectivity(self):
        """
        Reports a simple message to Phantom.
        """
        self.save_progress("The app runs, but this tests nothing else")
        return []

    @ActionHandler.data_contains({'name': Text, 'value': Text, 'type': Text})
    def dummy_action(
            self,
            required_number: int,
            required_str: str,
            required_bool: bool,
            optional_number: float = 42.69,
            optional_str: str = 'spam',
            optional_bool: bool = False,
            context=None,
    ):
        """
        Takes a variety of parameters and reports them back to Phantom.

        The parameter type annotations are used to infer the `data_type` for
        each parameter in the generated metadata unless new values are manually
        specified.

        :param required_number: A mandatory number
        :param required_str: A mandatory string
        :param required_bool: A mandatory bool
        :param optional_number: An optional number
        :param optional_str: An optional string
        :param optional_bool: An optional bool
        """
        names = [
            'required_number',
            'required_str',
            'required_bool',
            'optional_number',
            'optional_str',
            'optional_bool',
        ]
        local_vars = locals()
        for x in names:
            value = local_vars[x]
            yield {'name': x, 'value': value, 'type': type(value).__name__}

    @dummy_action.summary_contains(
        {
            'message': Text,
            'results.name': Text,
            'results.value': Text,
            'results.type': Text,
        },
    )
    def summarise(self, results):
        """
        Create a summary object from the result of dummy_action.

        :param iterable results: The output of a call to dummy_action
        :return: A dictionary summarising the result of dummy_action
        :rtype: dict
        """
        return {'message': 'Dummy action ran', 'results': results}
