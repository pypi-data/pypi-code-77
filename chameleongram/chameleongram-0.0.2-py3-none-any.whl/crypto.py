import os
from random import randint

import cryptg
import rsa


class RSA:
    _ = 1 << 64  # Compute that once

    public_key_fingerprints = {
        0xC3B42B026CE86B21
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAwVACPi9w23mF3tBkdZz+zwrzKOaaQdr01vAbU4E1pvkfj4sqDsm6\n"
            "lyDONS789sVoD/xCS9Y0hkkC3gtL1tSfTlgCMOOul9lcixlEKzwKENj1Yz/s7daS\n"
            "an9tqw3bfUV/nqgbhGX81v/+7RFAEd+RwFnK7a+XYl9sluzHRyVVaTTveB2GazTw\n"
            "Efzk2DWgkBluml8OREmvfraX3bkHZJTKX4EQSjBbbdJ2ZXIsRrYOXfaA+xayEGB+\n"
            "8hdlLmAjbCVfaigxX0CDqWeR1yFL9kwd9P0NsZRPsmoqVwMbMu7mStFai6aIhc3n\n"
            "Slv8kg9qv1m6XHVQY3PnEw+QQtqSIXklHwIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),  # DC 1
        0x9A996A1DB11C729B
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAxq7aeLAqJR20tkQQMfRn+ocfrtMlJsQ2Uksfs7Xcoo77jAid0bRt\n"
            "ksiVmT2HEIJUlRxfABoPBV8wY9zRTUMaMA654pUX41mhyVN+XoerGxFvrs9dF1Ru\n"
            "vCHbI02dM2ppPvyytvvMoefRoL5BTcpAihFgm5xCaakgsJ/tH5oVl74CdhQw8J5L\n"
            "xI/K++KJBUyZ26Uba1632cOiq05JBUW0Z2vWIOk4BLysk7+U9z+SxynKiZR3/xdi\n"
            "XvFKk01R3BHV+GUKM2RYazpS/P8v7eyKhAbKxOdRcFpHLlVwfjyM1VlDQrEZxsMp\n"
            "NTLYXb6Sce1Uov0YtNx5wEowlREH1WOTlwIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),
        0xB05B2A6F70CDEA78
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAsQZnSWVZNfClk29RcDTJQ76n8zZaiTGuUsi8sUhW8AS4PSbPKDm+\n"
            "DyJgdHDWdIF3HBzl7DHeFrILuqTs0vfS7Pa2NW8nUBwiaYQmPtwEa4n7bTmBVGsB\n"
            "1700/tz8wQWOLUlL2nMv+BPlDhxq4kmJCyJfgrIrHlX8sGPcPA4Y6Rwo0MSqYn3s\n"
            "g1Pu5gOKlaT9HKmE6wn5Sut6IiBjWozrRQ6n5h2RXNtO7O2qCDqjgB2vBxhV7B+z\n"
            "hRbLbCmW0tYMDsvPpX5M8fsO05svN+lKtCAuz1leFns8piZpptpSCFn7bWxiA9/f\n"
            "x5x17D7pfah3Sy2pA+NDXyzSlGcKdaUmwQIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),
        0x71E025B6C76033E3
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAwqjFW0pi4reKGbkc9pK83Eunwj/k0G8ZTioMMPbZmW99GivMibwa\n"
            "xDM9RDWabEMyUtGoQC2ZcDeLWRK3W8jMP6dnEKAlvLkDLfC4fXYHzFO5KHEqF06i\n"
            "qAqBdmI1iBGdQv/OQCBcbXIWCGDY2AsiqLhlGQfPOI7/vvKc188rTriocgUtoTUc\n"
            "/n/sIUzkgwTqRyvWYynWARWzQg0I9olLBBC2q5RQJJlnYXZwyTL3y9tdb7zOHkks\n"
            "WV9IMQmZmyZh/N7sMbGWQpt4NMchGpPGeJ2e5gHBjDnlIf2p1yZOYeUYrdbwcS0t\n"
            "UiggS4UeE8TzIuXFQxw7fzEIlmhIaq3FnwIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),
        0xBC35F3509F7B7A5
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAruw2yP/BCcsJliRoW5eBVBVle9dtjJw+OYED160Wybum9SXtBBLX\n"
            "riwt4rROd9csv0t0OHCaTmRqBcQ0J8fxhN6/cpR1GWgOZRUAiQxoMnlt0R93LCX/\n"
            "j1dnVa/gVbCjdSxpbrfY2g2L4frzjJvdl84Kd9ORYjDEAyFnEA7dD556OptgLQQ2\n"
            "e2iVNq8NZLYTzLp5YpOdO1doK+ttrltggTCy5SrKeLoCPPbOgGsdxJxyz5KKcZnS\n"
            "Lj16yE5HvJQn0CNpRdENvRUXe6tBP78O39oJ8BTHp9oIjd6XWXAsp2CvK45Ol8wF\n"
            "XGF710w9lwCGNbmNxNYhtIkdqfsEcwR5JwIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),
        0x15AE5FA8B5529542
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAvfLHfYH2r9R70w8prHblWt/nDkh+XkgpflqQVcnAfSuTtO05lNPs\n"
            "pQmL8Y2XjVT4t8cT6xAkdgfmmvnvRPOOKPi0OfJXoRVylFzAQG/j83u5K3kRLbae\n"
            "7fLccVhKZhY46lvsueI1hQdLgNV9n1cQ3TDS2pQOCtovG4eDl9wacrXOJTG2990V\n"
            "jgnIKNA0UMoP+KF03qzryqIt3oTvZq03DyWdGK+AZjgBLaDKSnC6qD2cFY81UryR\n"
            "WOab8zKkWAnhw2kFpcqhI0jdV5QaSCExvnsjVaX0Y1N0870931/5Jb9ICe4nweZ9\n"
            "kSDF/gip3kWLG0o8XQpChDfyvsqB9OLV/wIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),
        0xAEAE98E13CD7F94F
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAs/ditzm+mPND6xkhzwFIz6J/968CtkcSE/7Z2qAJiXbmZ3UDJPGr\n"
            "zqTDHkO30R8VeRM/Kz2f4nR05GIFiITl4bEjvpy7xqRDspJcCFIOcyXm8abVDhF+\n"
            "th6knSU0yLtNKuQVP6voMrnt9MV1X92LGZQLgdHZbPQz0Z5qIpaKhdyA8DEvWWvS\n"
            "Uwwc+yi1/gGaybwlzZwqXYoPOhwMebzKUk0xW14htcJrRrq+PXXQbRzTMynseCoP\n"
            "Ioke0dtCodbA3qQxQovE16q9zz4Otv2k4j63cz53J+mhkVWAeWxVGI0lltJmWtEY\n"
            "K6er8VqqWot3nqmWMXogrgRLggv/NbbooQIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),
        0x5A181B2235057D98
        - _: (
            "-----BEGIN RSA PUBLIC KEY-----\n"
            "MIIBCgKCAQEAvmpxVY7ld/8DAjz6F6q05shjg8/4p6047bn6/m8yPy1RBsvIyvuD\n"
            "uGnP/RzPEhzXQ9UJ5Ynmh2XJZgHoE9xbnfxL5BXHplJhMtADXKM9bWB11PU1Eioc\n"
            "3+AXBB8QiNFBn2XI5UkO5hPhbb9mJpjA9Uhw8EdfqJP8QetVsI/xrCEbwEXe0xvi\n"
            "fRLJbY08/Gp66KpQvy7g8w7VB8wlgePexW3pT13Ap6vuC+mQuJPyiHvSxjEKHgqe\n"
            "Pji9NP3tJUFQjcECqcm0yV7/2d0t/pbCm+ZH1sadZspQCEPPrtbkQBlvHb4OLiIW\n"
            "PGHKSMeRFvp3IWcmdJqXahxLCUS1Eh6MAQIDAQAB\n"
            "-----END RSA PUBLIC KEY-----"
        ),
    }

    @classmethod
    def encrypt(cls, data_with_hash: bytes, public_key_fingerprint: int) -> bytes:
        key = rsa.PublicKey.load_pkcs1(
            cls.public_key_fingerprints[public_key_fingerprint]
        )
        return rsa.core.encrypt_int(
            int.from_bytes(data_with_hash, "big"), key.e, key.n
        ).to_bytes(256, "big")


class Prime:
    # Recursive variant
    # @classmethod
    # def gcd(cls, a: int, b: int) -> int:
    #     return cls.gcd(b, a % b) if b else a

    @staticmethod
    def gcd(a: int, b: int) -> int:
        while b:
            a, b = b, a % b

        return a

    @classmethod
    def decompose(cls, pq: int) -> int:
        # https://comeoncodeon.wordpress.com/2010/09/18/pollard-rho-brent-integer-factorization/
        if pq % 2 == 0:
            return 2

        y, c, m = randint(1, pq - 1), randint(1, pq - 1), randint(1, pq - 1)
        g = r = q = 1
        x = ys = 0

        while g == 1:
            x = y

            for _ in range(r):
                y = (pow(y, 2, pq) + c) % pq

            k = 0

            while k < r and g == 1:
                ys = y

                for _ in range(min(m, r - k)):
                    y = (pow(y, 2, pq) + c) % pq
                    q = q * (abs(x - y)) % pq

                g = cls.gcd(q, pq)
                k += m

            r *= 2

        if g == pq:
            while True:
                ys = (pow(ys, 2, pq) + c) % pq
                g = cls.gcd(abs(x - ys), pq)

                if g > 1:
                    break

        return g


class AES(object):
    @staticmethod
    def decrypt_ige(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
        return cryptg.decrypt_ige(encrypted_data, key, iv)

    @staticmethod
    def encrypt_ige(data: bytes, key: bytes, iv: bytes) -> bytes:
        data += os.urandom(-len(data) % 16)
        return cryptg.encrypt_ige(data, key, iv)
