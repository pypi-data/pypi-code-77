import djclick as click
import djclick as click
from django_safe_settings.settings import DJANGO_SAFE_SETTINGS_CIPHER

@click.command()
@click.argument("plain_value", nargs=1, required=True)
def django_safe_settings_encrypt(plain_value):
    """Encrypt plain value and print out the result, so that you can copy it to your settings.py.
    """
    result = DJANGO_SAFE_SETTINGS_CIPHER.encrypt(plain_value)
    print("    plain value =", plain_value)
    print("encrypted value =", result)
