from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from ..config import settings as proxy_settings
from .py_cli import ProxyFetcher
from ..utils import get_redis_conn
import random


def dict_from_module(module):
    context = {}
    for setting in dir(module):
        # you can write your filter here
        if setting.isupper():
            context[setting] = getattr(module, setting)

    return context


def get_redis_proxies_conn(settings):
    redis_args = {
        'host': settings.get('PROXY_REDIS_HOST', '127.0.0.1'),
        'port': settings.get('PROXY_REDIS_PORT', '6379'),
        'db': settings.get('PROXY_REDIS_DB', '0'),
        'password': settings.get('PROXY_REDIS_PASSWORD', ''),
    }
    if isinstance(redis_args, dict):
        conn = get_redis_conn(**redis_args)
    else:
        conn = get_redis_conn()
    return conn


class ProxyMiddleware:
    def __init__(self, spider_settings):
        settings = {**dict_from_module(proxy_settings), **spider_settings}
        self.redis_args = {
            'host': settings.get('PROXY_REDIS_HOST', '127.0.0.1'),
            'port': settings.get('PROXY_REDIS_PORT', '6379'),
            'db': settings.get('PROXY_REDIS_DB', '0'),
            'password': settings.get('PROXY_REDIS_PASSWORD', ''),
        }
        self.strategy = settings.get('STRATEGY', 'robin')
        self.proxy_usage = settings.get('PROXY_USAGE', 'https')
        self.enable = settings.get('NEED_PROXY', False)
        # 这里从配置选取类型，是要https还是http
        # self.proxy_types = settings.get('PROXY_TYPE_LIST', ['https', 'http'])
        # self.chosen_proxy = ''
        # # ip代理列表
        # self.proxies = []
        # # 选择ip的复用模式
        # self.strategy = settings.get('strategy', 'greedy')
        # # ip 成绩等级
        # self.ip_level = settings.get('IP_LEVEL', 8)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # 使用代理
        if self.enable:
            pass  # use proxy
            fetcher = ProxyFetcher(self.proxy_usage, strategy=self.strategy, redis_args=self.redis_args)
            proxy = fetcher.get_proxy()
            request.meta["proxy"] = proxy
            print('使用代理====>', proxy)
            # request.meta["proxy"] = random.choice(self.proxies)


class ProxyRetryMiddleware(RetryMiddleware):
    def __init__(self, settings):
        self.conn = get_redis_proxies_conn(settings)

    def delete_proxy(self, proxy):
        # 删除逻辑暂时没实现
        pass

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            print('返回值异常, 进行重试...')
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            # 删除该代理
            self.delete_proxy(request.meta.get('proxy', False))
            print('连接异常, 进行重试...')

            return self._retry(request, exception, spider)
