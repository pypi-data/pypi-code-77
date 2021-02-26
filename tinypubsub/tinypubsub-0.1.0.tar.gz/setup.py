# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tinypubsub', 'tinypubsub.simple', 'tinypubsub.weakref']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tinypubsub',
    'version': '0.1.0',
    'description': 'Tiny pub-sub (observer) pattern implementation',
    'long_description': '# tinypubsub\n\n[![PyPI](https://img.shields.io/pypi/v/tinypubsub)](https://pypi.org/project/tinypubsub/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tinypubsub)](https://pypi.org/project/tinypubsub/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![license](https://img.shields.io/github/license/nekonoshiri/tinypubsub)](https://github.com/nekonoshiri/tinypubsub/blob/main/LICENSE)\n\nTiny pub-sub (observer) pattern implementation.\n\n## Usage\n\n```Python\nfrom tinypubsub.simple import SimplePublisher\n\npublisher = SimplePublisher()\n\nsubscription = publisher.subscribe(lambda message: print(message))\n\npublisher.publish("Hello!")\n\npublisher.unsubscribe(subscription)\n```\n\nOr:\n\n```Python\nfrom tinypubsub.simple import SimplePublisher\n\npublisher = SimplePublisher()\n\nwith publisher.subscribe(lambda message: print(message)):\n    publisher.publish("Hello!")\n```\n\n## Features\n\n- `tinypubsub.Publisher` has abstract methods: `publish`, `subscribe`, `unsubscribe`, `unsubscribe_all`.\n- `tinypubsub.simple.SimplePublisher`: Dict-based implementation of `Publisher`.\n- `tinypubsub.weakref.WeakrefPublisher`: WeakKeyDictionary-based implementation of `Publisher`.\n\n## API\n\n### Module `tinypubsub`\n\n#### *abstract class* `Publisher[Message]`\n\nAbstract publisher class.\n\n##### *type parameter* `Message`\n\nType of message that will be published.\n\n##### *abstract method* `publish(message: Message) -> None`\n\nPublish message to subscribers.\n\n##### *abstract method* `subscribe(subscriber: Callable[[Message], None]) -> Subscription`\n\nAdd subscriber.\n\n##### *abstract method* `unsubscribe(subscription: Subscription) -> None`\n\nDelete subscriber.\n\n##### *abstract method* `unsubscribe_all() -> None`\n\nDelete all subscribers.\n\n#### *class* `Subscription`\n\nReturn value of `Publisher.subscribe()`.\nIt can be used as a context manager as:\n\n```Python\nwith publisher.subscribe(...) as subscription:\n    ...\n```\n\nand `subscription.unsubscribe()` will be called when exit.\n\n##### *method* `unsubscribe() -> None`\n\n`subscription.unsubscribe()` is the same as `publisher.unsubscribe(subscription)`, where `subscription = publisher.subscribe(...)`.\n\n### Module `tinypubsub.simple`\n\n#### *class* `SimplePublisher[Message]`\n\nImplementation of `Publisher[Message]`.\n\n### Module `tinypubsub.weakref`\n\n#### *class* `WeakrefPublisher[Message]`\n\nImplementation of `Publisher[Message]`.\n\nThis implementation uses WeakKeyDictionary to manage subscribers.\nThis may prevent a memory leak if subscription loses all strong references before unsubscribed:\n\n```Python\npublisher = WeakrefPublisher()\n\nsubscription = publisher.subscribe(...)\n\nassert len(publisher._subscribers) == 1\n\ndel subscription\n\nassert len(publisher._subscribers) == 0\n```\n\nNote that the `unsubscribe` method will not be called in the above case,\nso normally you should unsubscribe explicitly or use context manager.\n\n',
    'author': 'Shiri Nekono',
    'author_email': 'gexira.halen.toms@gmail.com',
    'maintainer': 'Shiri Nekono',
    'maintainer_email': 'gexira.halen.toms@gmail.com',
    'url': 'https://github.com/nekonoshiri/tinypubsub',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
