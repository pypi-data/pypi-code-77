def parse_config(gear_context):
    """Parses gear_context config.

    Args:
        gear_context (flywheel_gear_toolkit.GearToolkitContext): context

    Returns:
        (tuple): tuple containing
            - input file path
            - input filename
            - treshold percentile
            - inversion of image

    """

    filepath = gear_context.get_input_path("nifti")
    filename = gear_context.config_json["inputs"]["nifti"]["location"]["name"]
    threshold_percentile = gear_context.config["threshold_percentile"]
    invert_image = gear_context.config["invert_image"]

    return filepath, filename, threshold_percentile, invert_image
