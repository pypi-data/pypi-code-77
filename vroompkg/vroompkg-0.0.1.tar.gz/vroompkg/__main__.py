import argparse
from . import run5

if __name__ == '__main__':
	ap = argparse.ArgumentParser()
	ap.add_argument("-u", "--userid", required=True, help = "user's email id")
	ap.add_argument("-m", "--meetingid", required=True, help = "meeting id (10 digits)")
	args = vars(ap.parse_args())
	run5.vroom(args)