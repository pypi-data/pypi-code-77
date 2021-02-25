import pyotp


class OTP:
    """Library for generating OTP's from a secret

    Generates TOTP's based on a base32 secret
    """


    def get_otp(self, secret, timestamp=False):
        """Takes 1 argument and an optional timestamp argument.

        Example:
        | base32secret |
        | base32secret | timestamp |
        """
        totp = pyotp.TOTP(secret)
        if timestamp:
            return totp.at(timestamp)
        else:
            return totp.now()
