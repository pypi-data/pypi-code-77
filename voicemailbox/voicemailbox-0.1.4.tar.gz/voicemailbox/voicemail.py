import datetime
import re
import operator
import pathlib


class Voicemail:

    def __init__(self, source):

        if not isinstance(source, pathlib.Path):
            raise ValueError("source must be a Path object")

        self.source = source
        self._read = False

        # filename follows the format
        # « De_[PhoneNumber]_[JJMMAAAA]_[HH]h[MM]_[xxxxxxxxxxxxx].mp3 »
        filename = self.source.name

        day = int(filename.split("_")[2][0:2])
        month = int(filename.split("_")[2][2:4])
        year = int(filename.split("_")[2][4:8])
        hour = int(filename.split("_")[3][0:2])
        minute = int(filename.split("_")[3][3:5])

        self.datetime = datetime.datetime(year=year, month=month, day=day,
                                          hour=hour, minute=minute)
        self.date = self.datetime.date()
        self.time = self.datetime.time()

        self.numero = filename.split("_")[1]

        # Define an attribute for a human readable time and numero
        # The same is done with date (but a property is required)
        self.pretty_time = f"{self.time.hour:02d}h{self.time.minute:02d}"
        self.pretty_numero = (" ".join(re.findall(r"[0-9]{2}", self.numero))
                              if not self.numero == "anonymous"
                              else "numéro inconnu")

    def __eq__(self, other):
        if isinstance(other, Voicemail):
            return self.source == other.source
        else:
            return False

    @property
    def pretty_date(self):
        d = self.datetime
        if d.date() == datetime.date.today():
            return "aujourd’hui"
        elif d.date() == datetime.date.today() - datetime.timedelta(days=1):
            return "hier"
        else:
            return f"{d:%A} {d.day} {d:%B} {d.year}"

    @property
    def read(self):
        return self._read

    @read.setter
    def read(self, value):

        if not isinstance(value, bool):
            raise ValueError("'read' must be a boolean")

        if not self._read == value:
            if value is True:
                VoicemailManager.move_to_read_dir(self)
            else:
                # VMManager.move_to_read_dir()
                pass


class VoicemailManager:

    PATH = pathlib.Path.home() / "Messages vocaux"
    PATH_NEW = PATH / "non lus"
    PATH_READ = PATH / "lus"

    MAIL_PATTERN = re.compile(
        r"^De_([0-9]{10}|anonymous)_"
        r"[0-9]{8}_[0-9]{2}h[0-9]{2}_[0-9a-f]*\.mp3$")

    def __init__(self):

        # Create voicemails directories if they do not exist
        self.PATH_NEW.mkdir(parents=True, exist_ok=True)
        self.PATH_READ.mkdir(parents=True, exist_ok=True)

    @property
    def new_voicemails(self):
        return sorted([Voicemail(file) for file in self.PATH_NEW.iterdir()
                       if self.MAIL_PATTERN.match(file.name)],
                      key=operator.attrgetter("datetime"))

    @classmethod
    def move_to_read_dir(cls, voicemail):
        new_src = voicemail.source.replace(
            cls.PATH_READ / voicemail.source.name)
        voicemail.source = new_src
