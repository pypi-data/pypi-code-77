import sys
from typing import Any, Dict

from sphinx.application import Sphinx

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__)


def setup(app: Sphinx) -> Dict[str, Any]:
    from sphinx_thrift.documenter import ThriftModuleDocumenter
    from sphinx_thrift.domain import ThriftDomain

    app.add_config_value('thrift_executable', 'thrift', 'env', [str])
    app.add_autodocumenter(ThriftModuleDocumenter)
    app.add_domain(ThriftDomain)
    return {
        'version': __version__,
        'env_version': 0,
        'parallel_read_safe': True,
        'parallel_write_safe': True
    }
