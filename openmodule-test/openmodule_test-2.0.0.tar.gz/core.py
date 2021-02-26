from typing import Dict

from openmodule.core import init_openmodule, shutdown_openmodule, OpenModuleCore
from openmodule_test.health import HealthTestMixin


class OpenModuleCoreTestMixin(HealthTestMixin):
    init_kwargs: Dict = {}
    config_kwargs: Dict = {}

    core: OpenModuleCore

    def get_config_kwargs(self):
        return self.config_kwargs

    def get_init_kwargs(self):
        return self.init_kwargs

    def setUp(self):
        super().setUp()
        self.init_kwargs.setdefault("sentry", False)
        self.init_kwargs.setdefault("dsgvo", False)
        self.core = init_openmodule(
            config=self.zmq_config(**self.get_config_kwargs()),
            context=self.zmq_context(),
            **self.get_init_kwargs()
        )
        self.zmq_client.subscribe(b"healthz")
        self.wait_for_health(self.zmq_config().NAME)

    def tearDown(self):
        try:
            super().tearDown()
        finally:
            shutdown_openmodule()
