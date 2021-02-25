from crawlab.constants import DedupMethod
from crawlab.db.es import index_item
from crawlab.db.kafka import send_msg
from crawlab.db.mongo import get_col
from crawlab.db.sql import insert_item, get_item, update_item
from crawlab.utils.config import get_task_id, get_is_dedup, get_dedup_field, get_dedup_method





def save_item_mongo(item):
    col = get_col()
    # 缓存数据的buffer
    item_buffer = []
    # 配置
    config = {
        buffer: 1000,
        append_timestamp:true,
    }
    # 赋值task_id
    item['task_id'] = get_task_id()

    # 是否开启去重
    is_dedup = get_is_dedup()

    # if is_dedup == '1':
    #     # 去重
    #     dedup_field = get_dedup_field()
    #     dedup_method = get_dedup_method()
    #     if dedup_method == DedupMethod.OVERWRITE:
    #         # 覆盖
    #         if col.find_one({dedup_field: item[dedup_field]}):
    #             col.replace_one({dedup_field: item[dedup_field]}, item)
    #         else:
    #             col.save(item)
    #     elif dedup_method == DedupMethod.IGNORE:
    #         # 忽略
    #         col.save(item)
    #     else:
    #         # 其他
    #         col.save(item)
    # else:
    #     # 不去重
    #     col.save(item)
    if config['buffer']:   
        self.current_item += 1

        if self.config['append_timestamp']:
            item['scrapy-mongodb'] = {'ts': datetime.datetime.utcnow()}

        item_buffer.append(item)

        if self.current_item == config['buffer']:
            self.current_item = 0
            try:
                return self.insert_item(item_buffer, spider)
            finally:
                item_buffer = []

        return item

    self.insert_item(item, spider)

def save_item_sql(item):
    # 是否开启去重
    is_dedup = get_is_dedup()

    # 赋值task_id
    item['task_id'] = get_task_id()

    if is_dedup == '1':
        # 去重
        dedup_field = get_dedup_field()
        dedup_method = get_dedup_method()
        if dedup_method == DedupMethod.OVERWRITE:
            # 覆盖
            if get_item(item, dedup_field):
                update_item(item, dedup_field)
            else:
                insert_item(item)
        elif dedup_method == DedupMethod.IGNORE:
            # 忽略
            insert_item(item)
        else:
            # 其他
            insert_item(item)
    else:
        # 不去重
        insert_item(item)


def save_item_kafka(item):
    item['task_id'] = get_task_id()
    send_msg(item)


def save_item_es(item):
    item['task_id'] = get_task_id()
    index_item(item)
