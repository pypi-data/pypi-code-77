import datetime
import requests
import getpass
import os


class Horoscope:

    sign_dates = {
        "CAPRICORN" : datetime.date(2021, 12, 23),
        "AQUARIUS" : datetime.date(2021, 1, 22),
        "PISCES" : datetime.date(2021, 2, 21),
        "ARIES" : datetime.date(2021, 3, 20),
        "TAURUS" : datetime.date(2021, 4, 21),
        "GEMINI" : datetime.date(2021, 5, 22),
        "CANCER" : datetime.date(2021, 6, 23),
        "LEO" : datetime.date(2021, 7, 23),
        "VIRGO" : datetime.date(2021, 8, 23),
        "LIBRA" : datetime.date(2021, 9, 23),
        "SCORPIO" : datetime.date(2021, 10, 23),
        "SAGITTARIUS" : datetime.date(2021, 11, 13),
    }

    def __init__(self, data_filepath=f"/home/{getpass.getuser()}/.horo"):
        self.data_filepath = data_filepath

        self.sign = False

        if not os.path.exists(data_filepath): self._save_user_sign(self.get_user_sign())
        else: self.print_user_horoscope()

    def print_user_horoscope(self) -> None:
        self._read_user_sign()
        res = requests.get(f"http://sandipbgt.com/theastrologer/api/horoscope/{self.sign.lower()}/today")
        print(res.json()["horoscope"])

    def _read_user_sign(self):
        with open(self.data_filepath, "r") as f:
            self.sign = f.readlines()[0]

    def _save_user_sign(self, sign: str):
        self.sign = sign
        with open(self.data_filepath, "w") as f:
            f.write(sign)

    @staticmethod
    def _get_user_permission(message):
        return input(message + " [y/N]") == "y"

    @staticmethod
    def get_user_sign():
        if not Horoscope._get_user_permission(
            "It appears this is your first time running this program,\nin order to continue, you must provide your birthday."): quit()

        day, month = input("what's your birthday? e.g. '<day:int> <month:int>' '5 5' for 5 May : ").split()
        user_birthday = datetime.date(2021, int(month), int(day))

        closest_sign_diff = None
        for key in Horoscope.sign_dates.keys():
            if 0 < user_birthday.toordinal() - Horoscope.sign_dates[key].toordinal() < 30:
                return key


def main():
    Horoscope()


if __name__ == "__main__":
    main()

