import yaml
from moocxing.robot import Constants
import logging

log = logging.getLogger(__name__)
with open(Constants.DEFAULT_CONFIG_PATH) as f:
    allConfig = yaml.safe_load(f)


def get(items):
    config = allConfig

    for item in items.split("/"):
        config = config.get(item)

    if config:
        return config
    else:
        log.warning(f"参数不存在：{Constants.DEFAULT_CONFIG_NAME}中没有找到{items}参数")
