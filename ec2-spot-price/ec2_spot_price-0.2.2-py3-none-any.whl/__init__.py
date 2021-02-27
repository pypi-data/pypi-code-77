from .ec2_spot_price import get_spot_prices, print_csv, print_table

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

__all__ = ['get_spot_prices', 'print_csv', 'print_table']
