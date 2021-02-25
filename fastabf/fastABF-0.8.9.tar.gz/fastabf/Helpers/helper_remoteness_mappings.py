# Module that generates mappings to remoteness category
# The code below performs mappings from
# - postcode to RA16 (remoteness category)
# - SA2 to RA16 (remoteness category)

import pandas as pd

from fastabf.datatypes import Remoteness_Category_RA16

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
finally:
    from .. import csvstores  # relative-import the *package* containing the templates

# load postcode to RA2016 mapper
filename_postcode_to_ra16mapper = "postcode_to_ra16mapper.csv"
location_postcode_to_ra16mapper = pkg_resources.open_text(
    csvstores, filename_postcode_to_ra16mapper)


postcode_to_ra16mapper = pd.read_csv(
    location_postcode_to_ra16mapper,
    converters={
        'ra_name_2016': lambda x: Remoteness_Category_RA16(int(x))
    },
    index_col=0).squeeze()


def get_remoteness_cat_for_postcode(post_code: int) -> Remoteness_Category_RA16:
    return postcode_to_ra16mapper.get(post_code, Remoteness_Category_RA16.Unknown)


# load SA2 to RA2016 mapper

filename_sa2_to_ra16_mapper = "sa2_to_ra16mapper.csv"
location_sa2_to_ra16_mapper = pkg_resources.open_text(
    csvstores, filename_sa2_to_ra16_mapper)

map_SA2_to_RA2016 = pd.read_csv(
    location_sa2_to_ra16_mapper,
    converters={
        "Remoteness_Category_RA16": lambda x: Remoteness_Category_RA16(int(x))},
    index_col=0).squeeze()


def get_remoteness_cat_for_SA2(SA2code: int) -> Remoteness_Category_RA16:
    return map_SA2_to_RA2016.get(SA2code, Remoteness_Category_RA16.Unknown)
