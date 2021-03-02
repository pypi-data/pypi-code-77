def validate_dataCompleteness(data_completeness: dict):
    return next((value for value in data_completeness.values() if isinstance(value, bool)), False) or {
        'level': 'warning',
        'dataPath': '.dataCompleteness',
        'message': 'may not all be set to false'
    }
