def get_unique_light_identifier(light):
    """Returns a unique identifier for the given light."""
    return f'{light.topic}@{light.device}'
