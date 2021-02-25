import json
import subprocess
from datetime import datetime, date


QUERY = (
    'traces | order by timestamp | project timestamp, '
    'input = customDimensions["input"], '
    'prediction = customDimensions["prediction"]'
)


def query(app, resource_group, subscription, start_date, end_date):
    """
    TODO

    :param str app: Azure Application Insight app name
    :param str resource_group: Azure Resource group
    :param str subscription: Azure Subscription
    :param date start_date: Start date (included)
    :param date end_date: End date (included)
    :rtype: typing.Dict[str, typing.Any]
    """
    command = ['az', 'monitor', 'app-insights', 'query']
    command.extend(('--apps', app))
    command.extend(('--resource-group', resource_group))
    command.extend(('--subscription', subscription))
    command.extend(('--start-time', start_date.isoformat()))
    command.extend(('--end-time', end_date.isoformat()))
    command.extend(('--analytics-query', QUERY))

    output = subprocess.check_output(command)

    return json.loads(output)


def parse_return_json(return_json):
    """
    :param typing.Dict[str, typing.Any] return_json:
    :rtype: typing.Dict[str, typing.Any]
    """
    columns = [c['name'] for c in return_json['tables'][0]['columns']]

    for row in return_json['tables'][0]['rows']:
        result = dict(zip(columns, row))
        result['timestamp'] = datetime \
            .strptime(result['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ') \
            .replace(microsecond=0)

        try:
            result['inputJson'] = json.loads(result['input'])
            result.pop('input')
        except json.decoder.JSONDecodeError:
            # SDK version 0.5.12 and earlier did not JSON encode correctly
            pass

        try:
            result['predictionJson'] = json.loads(result['prediction'])
            result.pop('prediction')
        except json.decoder.JSONDecodeError:
            # SDK version 0.5.12 and earlier did not JSON encode correctly
            pass

        yield result


def query_predictions(*args, **kwargs):
    """
    Perform an Application Insight query to get inputs with their respective
    predictions from a deployed model. These are the entries logged by models
    when deployed in Azure using the SDK.

    Example usage:

        from datetime import date
        from energinetml import query_predictions

        entries = query_predictions(
            app='MyApplicationInsightAppName',
            resource_group='MyAzureResourceGroup',
            subscription='MyAzureSubscription',
            start_date=date(2021, 1, 1),
            end_date=date(2021, 12, 31),
        )
    """
    return_json = query(*args, **kwargs)
    parsed_json = parse_return_json(return_json)
    return parsed_json
