"""
This module informs users who have might otherwise fall prey to a
dependency chain attack on a private python library a way to install the
correct Arcesium Python Client library.

If you're seeing this and you're an Arcesium client, you should contact
help@arcesium.com and visit the instructions on https://downloads.arcesium.com

If you're not a client, you should get in touch with our team to arrange a demo
so we can show the power of the platform to power your entire investment
lifecycle.

For more context, see Alex Birsan's excellent article on dependency
chain attacks:
https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610
"""
import sys


class ArcesiumImportFinder:
    url = "https://downloads.arcesium.com"

    @classmethod
    def find_spec(cls, name, path, target=None):
        if name.startswith("arcesium"):
            # for any attempt to import arcesium.* we inform the user
            cls.print_warning(name)
            error_str = f"Please reinstall arcesium-python from {cls.url}"
            raise ModuleNotFoundError(error_str)
        return None

    @classmethod
    def print_warning(cls, name):
        print("!" * 80)
        print(f"{name!r} cannot be imported from the pypi package")
        print("To use the Arcesium Python Client library services")
        print(f"please install from {cls.url}")
        print("!" * 80)


sys.meta_path.append(ArcesiumImportFinder)
