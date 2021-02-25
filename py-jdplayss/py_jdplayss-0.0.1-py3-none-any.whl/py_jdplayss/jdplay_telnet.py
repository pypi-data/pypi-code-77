# Library for contacting JdPlay through telnet.

# Imports
import telnetlib
import re
import json

# Error Imports
from socket import error as sockerr


# Exceptions
class JdPlayProcessError(Exception):
    """Something is wrong with JdPlay itself."""
    pass


class CommandError(Exception):
    """Something is wrong with the command."""
    pass


class ParseError(Exception):
    """Could not parse the information provided by JdPlay."""
    pass


class LuaError(Exception):
    """Problem with the JdPlay lua telnet."""
    pass


class ConnectionError(Exception):
    """Something is wrong with the connection to JdPlay."""
    pass


# JdPlay Telnet Class
class JdPlayTelnet(object):
    """Conection to JdPlay using Telnet."""

    # Non commands
    def __init__(self, host):
        # Connect to telnet. Host and port are __init__ arguments
        try:
            self.tn = telnetlib.Telnet(host, port=8000, timeout=10)
        except sockerr:
            raise ConnectionError(
                "Could not connect to JdPlay. Make sure the Telnet interface is enabled and accessible.")
        # Login to JdPlay using password provided in the arguments
        self.tn.set_debuglevel(2)
        # self.tn.read_until(b"Password: ")
        self.auth()

    def run_command(self, command):
        """Run a command and return a list with the output lines."""
        # Put the command in a nice byte-encoded variable
        full_command = json.dumps(command).encode('utf-8') + b'\n'
        # Write out the command to telnet
        self.tn.write(full_command)
        # Get the command output, decode it, and split out the junk
        command_output_org = self.tn.read_until(b'{').decode('utf-8').split()
        command_output = "{" + command_output_org[0]
        # command_output = self.tn.read_all()
        # Raise command error if JdPlay does not recognize the command.
        if command_output:
            command_error = re.match(r"Error in.*", command_output[0])
            if re.match(r"Unknown command `.*'\. Type `help' for help\.", command_output[0]):
                raise CommandError("Unknown Command")
            elif command_error:
                raise LuaError(command_error.group())
        # Return the split output of the command
        return ServerAnswer(command_output)

    def auth(self):
        """Add XYZ to playlist."""
        command = {"type": 1, "i0": 1, "i1": 240}
        self.run_command(command)

    def play(self):
        """Play stream."""
        self.run_command({"type": 3, "i0": 101, "seq": 1})

    def stop(self):
        """Stop stream."""
        self.run_command({"type": 3, "i0": 102, "seq": 1})

    def next(self):
        """Next playlist item."""
        self.run_command({"type": 3, "i0": 103, "seq": 1})

    def prev(self):
        """Previous playlist item."""
        self.run_command({"type": 3, "i0": 104, "seq": 1})

    def repeat(self, switch=True, setting='on'):
        """Toggle playlist repeat."""
        if switch:
            self.run_command({"type": 3, "i0": 101, "i1": 1, "seq": 1})
        # else:
        #     command = 'repeat ' + setting
        #     self.run_command(command)

    def loop(self, switch=True, setting='on'):
        """Toggle playlist loop."""
        if switch:
            self.run_command({"type": 3, "i0": 101, "i1": 0, "seq": 1})
        # else:
        #     command = {"type": 3, "i0": 101, "i1": 2,"seq": 1}
        #     self.run_command(command)

    def random(self, switch=True, setting='on'):
        """Toggle playlist random."""
        if switch:
            self.run_command({"type": 3, "i0": 101, "i1": 2, "seq": 1})
        # else:
        #     command = 'random ' + setting
        #     self.run_command(command)

    def status(self):
        """Current playlist status."""
        status_output = self.run_command({"type": 3, "i0": 100, "seq": 1})
        # if len(status_output) == 3:
        #     inputloc = '%20'.join(status_output[0].split(' ')[3:-1])
        #     volume = int(status_output[1].split(' ')[3])
        #     state = status_output[2].split(' ')[2]
        #     returndict = {'input': inputloc, 'volume': volume, 'state': state}
        # elif len(status_output) == 2:
        #     volume = int(status_output[0].split(' ')[3])
        #     state = status_output[1].split(' ')[2]
        #     returndict = {'volume': volume, 'state': state}
        # else:
        #     raise ParseError("Could not get status.")
        return status_output.s0

    # def set_title(self, setto):
    #     """Set title in current item."""
    #     command = 'title ' + setto
    #     self.run_command(command)

    def title(self):
        """Get title in current item."""
        return self.run_command('title')[0]

    def title_n(self):
        """Next title in current item."""
        self.run_command('title_n')

    def title_p(self):
        """Previous title in current item."""
        self.run_command('title_p')

    # def set_chapter(self, setto):
    #     """Set chapter in current item."""
    #     command = 'chapter ' + setto
    #     self.run_command(command)

    # Block 2
    def seek(self, time):
        """Seek in seconds, for instance 'seek 12'."""
        command = {"type": 3, "i0": 105, "i0": time, "seq": 1}
        self.run_command(command)

    def pause(self):
        """Toggle pause."""
        self.run_command({"type": 3, "i0": 102, "seq": 1})

    # def info(self):
    #     """Information about the current stream."""
    #     section = None
    #     data = {}
    #     for l in self.run_command({"type": 3, "i0": 100, "seq": 1}):
    #         if l[0] == '+':
    #             # Example: "+----[ Stream 5 ]" or "+----[ Meta data ]"
    #             if 'end of stream info' in l: continue
    #             section = l.split('[')[1].replace(']', '').strip().split(' ')[1]
    #             try:
    #                 section = int(section)
    #             except ValueError:
    #                 pass
    #             data[section] = {}
    #         elif l[0] == '|':
    #             # Example: "| Description: Closed captions 4"
    #             if len(l[2:]) == 0: continue
    #             key, value = l[2:].split(':', 1)
    #             try:
    #                 value = int(value)
    #             except ValueError:
    #                 try:
    #                     value = float(value)
    #                 except ValueError:
    #                     value = value.strip()
    #             data[section][key.strip()] = value
    #         else:
    #             raise ParseError("Unexpected line in info output")
    #     return data

    # Skipping stats
    def get_time(self):
        """Seconds elapsed since stream's beginning."""
        return int(self.run_command({"type": 3, "i0": 106, "seq": 1}).s0.split(":")[0])

    def is_playing(self):
        """True if a stream plays, False otherwise."""
        command_output = self.run_command({"type": 3, "i0": 100, "seq": 1})["playState"]
        return True if command_output == '1' else False

    def get_title(self):
        """The title of the current stream."""
        return self.run_command('get_title')[0]

    def get_length(self):
        """The length of the current stream."""
        return int(self.run_command({"type": 3, "i0": 106, "seq": 1}).s0.split(":")[1])

    # Block 3
    def set_volume(self, setto):
        """Set audio volume."""
        command = {"type": 3, "i0": 107, "i1": setto, "seq": 1}
        self.run_command(command)

    def volume(self):
        """Get audio volume (0 to 500)."""
        return int(self.run_command('volume')[0])

    # def volup(self, raiseby):
    #     """Raise audio volume X steps."""
    #     command = 'volup {}'.format(int(raiseby))
    #     self.run_command(command)

    # def voldown(self, raiseby):
    #     """Lower audio volume X steps."""
    #     command = 'voldown {}'.format(int(raiseby))
    #     self.run_command(command)

    # The following 'get' commands ARE NOT PARSED! Must do later :D
    # def set_adev(self, setto):
    #     """Set audio device."""
    #     command = 'adev ' + setto
    #     self.run_command(command)

    # def adev(self):
    #     """Get audio device."""
    #     return self.run_command('adev')[0]
    #
    # def set_achan(self, setto):
    #     """Set audio channels."""
    #     command = 'achan ' + setto
    #     self.run_command(command)

    # def achan(self):
    #     """Get audio channels."""
    #     return self.run_command('achan')[0]

    # def set_atrack(self, setto):
    #     """Set audio track."""
    #     command = 'atrack ' + str(setto)
    #     self.run_command(command)
    #
    # def atrack(self):
    #     """Get audio track."""
    #     return self.run_command('atrack')[0]

    def snapshot(self):
        """Take video snapshot."""
        self.run_command('snapshot')

    def set_strack(self, setto):
        """Set subtitles track."""
        command = 'strack ' + setto
        self.run_command(command)

    def strack(self):
        """Get subtitles track."""
        return self.run_command('strack')[0]

    # Block 4 - Skipping a few useless ones when using a library
    def vlm(self):
        """Load the VLM."""
        self.run_command('vlm')

    def logout(self):
        """Exit."""
        self.run_command('logout')

    def shutdown(self):
        """Shutdown JdPlay."""
        self.run_command({"type": 3, "i0": 201, "seq": 1})

    def tts(self, words):
        """Shutdown JdPlay."""
        self.run_command({"type": 3, "i0": 116, "s0": words, "seq": 1})


class ServerAnswer(object):

    def __init__(self, msg):
        # Connect to telnet. Host and port are __init__ arguments
        msg_info = json.loads(msg)
        self.type = msg_info.get("type",None)
        self.seq = msg_info.get("seq",None)
        self.s0 = msg_info.get("s0",None)
        self.s1 = msg_info.get("s1",None)
        self.i0 = msg_info.get("i0",None)
        self.i1 = msg_info.get("i1",None)