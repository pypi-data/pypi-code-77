from bson.int64 import Int64

from mindsdb.api.mongo.classes import Responder
import mindsdb.api.mongo.functions as helpers


class Responce(Responder):
    when = {'find': helpers.is_true}

    def result(self, query, request_env, mindsdb_env, session):
        models = mindsdb_env['mindsdb_native'].get_models()
        model_names = [x['name'] for x in models]
        table = query['find']
        where_data = query.get('filter', {})
        print(f'\n\n\nOperating on models: {models}\n\n\n')
        if table == 'predictors':
            data = [{
                'name': x['name'],
                'status': x['status'],
                'accuracy': str(x['accuracy']) if x['accuracy'] is not None else None,
                'predict': ', '.join(x['predict']),
                'select_data_query': '',
                'external_datasource': '',
                'training_options': ''
            } for x in models]
        elif table in model_names:
            # prediction
            model = mindsdb_env['mindsdb_native'].get_model_data(name=query['find'])

            columns = []
            columns += model['columns']
            columns += [f'{x}_original' for x in model['predict']]
            for col in model['predict']:
                if model['data_analysis_v2'][col]['typing']['data_type'] == 'Numeric':
                    columns += [f"{col}_min", f"{col}_max"]
                columns += [f"{col}_confidence"]
                columns += [f"{col}_explain"]

            columns += ['when_data', 'select_data_query', 'external_datasource']

            where_data_list = where_data if isinstance(where_data, list) else [where_data]
            for statement in where_data_list:
                if isinstance(statement, dict):
                    for key in statement:
                        if key not in columns:
                            columns.append(key)

            if 'select_data_query' in where_data:
                integrations = mindsdb_env['config']['integrations'].keys()
                connection = where_data.get('connection')
                if connection is None:
                    if 'default_mongodb' in integrations:
                        connection = 'default_mongodb'
                    else:
                        for integration in integrations:
                            if integration.startswith('mongodb_'):
                                connection = integration
                                break

                if connection is None:
                    raise Exception("Can't find connection from which fetch data")

                ds_name = 'temp'

                ds, ds_name = mindsdb_env['data_store'].save_datasource(
                    name=ds_name,
                    source_type=connection,
                    source=where_data['select_data_query']
                )
                where_data = mindsdb_env['data_store'].get_data(ds_name)['data']
                mindsdb_env['data_store'].delete_datasource(ds_name)

            if 'external_datasource' in where_data:
                ds_name = where_data['external_datasource']
                if mindsdb_env['data_store'].get_datasource(ds_name) is None:
                    raise Exception(f"Datasource {ds_name} not exists")
                where_data = mindsdb_env['data_store'].get_data(ds_name)['data']

            prediction = mindsdb_env['mindsdb_native'].predict(name=table, when_data=where_data)

            predicted_columns = model['predict']

            data = []
            keys = [x for x in list(prediction._data.keys()) if x in columns]
            min_max_keys = []
            for col in predicted_columns:
                if model['data_analysis_v2'][col]['typing']['data_type'] == 'Numeric':
                    min_max_keys.append(col)

            length = len(prediction._data[predicted_columns[0]])
            for i in range(length):
                row = {}
                explanation = prediction[i].explain()
                for key in keys:
                    row[key] = prediction._data[key][i]

                for key in predicted_columns:
                    row[key + '_confidence'] = explanation[key]['confidence']
                    row[key + '_explain'] = explanation[key]
                for key in min_max_keys:
                    row[key + '_min'] = min(explanation[key]['confidence_interval'])
                    row[key + '_max'] = max(explanation[key]['confidence_interval'])
                data.append(row)

        else:
            # probably wrong table name. Mongo in this case returns empty data
            data = []

        if 'projection' in query and len(data) > 0:
            true_filter = []
            false_filter = []
            for key, value in query['projection'].items():
                if helpers.is_true(value):
                    true_filter.append(key)
                else:
                    false_filter.append(key)

            keys = list(data[0].keys())
            del_id = '_id' in false_filter
            if len(true_filter) > 0:
                for row in data:
                    for key in keys:
                        if key != '_id':
                            if key not in true_filter:
                                del row[key]
                        elif del_id:
                            del row[key]
            else:
                for row in data:
                    for key in false_filter:
                        if key in row:
                            del row[key]

        db = mindsdb_env['config']['api']['mongodb']['database']

        cursor = {
            'id': Int64(0),
            'ns': f"{db}.$cmd.{query['find']}",
            'firstBatch': data
        }
        return {
            'cursor': cursor,
            'ok': 1
        }


responder = Responce()
