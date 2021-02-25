# Code generated by generate_init.py. DO NOT EDIT.

from .vegatradingclient import VegaTradingClient
from .vegatradingdataclient import VegaTradingDataClient
from .faucetclient import FaucetClient
from .helpers import grpc_error_detail
from .walletclient import WalletClient
from .generated import (
    api,
    tm,
    assets_pb2 as assets,
    assets_pb2_grpc as assets_grpc,
    chain_events_pb2 as chain_events,
    chain_events_pb2_grpc as chain_events_grpc,
    events_pb2 as events,
    events_pb2_grpc as events_grpc,
    governance_pb2 as governance,
    governance_pb2_grpc as governance_grpc,
    markets_pb2 as markets,
    markets_pb2_grpc as markets_grpc,
    vega_pb2 as vega,
    vega_pb2_grpc as vega_grpc,
)

__all__ = [
    "VegaTradingClient",
    "VegaTradingDataClient",
    "FaucetClient",
    "WalletClient",
    "grpc_error_detail",
    "api",
    "tm",
    "assets",
    "assets_grpc",
    "chain_events",
    "chain_events_grpc",
    "events",
    "events_grpc",
    "governance",
    "governance_grpc",
    "markets",
    "markets_grpc",
    "vega",
    "vega_grpc",
]
