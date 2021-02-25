import plistlib
import os, sys
def get_bundle_identifier():
	try:
		plist = plistlib.readPlist(os.path.abspath(os.path.join(sys.executable, '..', 'Info.plist')))
		print("get_bundle")
		return '{CFBundleIdentifier}'.format(**plist)
	except Exception:
		return "error"

def is_pythonista_3():
	return get_bundle_identifier() == 'com.omz-software.Pythonista3'

def is_pythonista_2():
	return get_bundle_identifier() == 'com.omz-software.Pythonista'
