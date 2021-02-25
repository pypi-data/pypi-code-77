#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from ssht00ls.classes.config import *
from ssht00ls.classes import utils
from ssht00ls.classes.smartcards import smartcards
from ssht00ls.classes.ssh import ssh

# the ssh agent object class.
class Agent(object):
	def __init__(self,
		# initialize as specific not global (optional).
		# the path to the public key.
		public_key=None,
		# the path to the private key.
		private_key=None,
		# the smart card boolean.
		smartcard=False,
	):

		# specific variables.
		self.specific = public_key != None or private_key != None
		self.private_key = private_key
		self.public_key = public_key
		self.smartcard = smartcard

		# set agent.
		if INTERACTIVE:
			ssh.utils.ssh_agent()
		
		#
	def add(self, 
		# the keys path.
		path=None, 
		# the keys passphrase.
		passphrase=None, 
		# enable if you are using a smart card.
		smartcard=False, 
		# the smart cards pin code
		pin=None, 
		# default timeout (do not use).
		timeout=0.5,
		# reattempt (do not use).
		reattempt=True,
	):

		# check specific.
		if self.specific:
			if path == None: path = self.private_key
			if smartcard == None: smartcard = self.smartcard

		# initialize.
		path = path.replace("//", "/")
		response = r3sponse.check_parameters(empty_value=None, parameters={
			"path":path
		})
		if not response["success"]: return response
		if smartcard:
			response = r3sponse.check_parameters(empty_value=None, parameters={
				"pin":pin
			})
			if not response["success"]: return response
		else:
			if not Files.exists(path):
				return r3sponse.error(f"Key path [{path}] does not exist.")
			public_key = path.replace("/private_key","/public_key")
			if not Files.exists(public_key):
				return r3sponse.error(f"Key path [{public_key}] does not exist.")

		# check agent connection.
		output = utils.__execute__(["ssh-add", "-L"])
		if "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
			if reattempt:
				ssh.utils.ssh_agent()
				return self.add(
					# the keys path.
					path=path,
					# the keys passphrase.
					passphrase=passphrase,
					# enable if you are using a smart card.
					smartcard=smartcard,
					# the smart cards pin code
					pin=pin,
					# default timeout (do not use).
					timeout=timeout,
					# reattempt (do not use).
					reattempt=False,
				)
			else:
				return r3sponse.error("Failed to communicate with the ssh-agent. Try logging out the current system user & logging back in (or execute [$ eval `ssh-agent`]).")

		# check already added.
		if not smartcard:
			response = self.check(public_key=public_key, raw=False)
			if response.success:
				return r3sponse.success(f"Key [{path}] is already added to the ssh agent.")

		# with passphrase.
		if smartcard or passphrase not in [False, None, "", "none", "None"]:
			if smartcard:
				path = smartcards.path
				if syst3m.defaults.vars.os in ["macos"]:
					os.system(f"rm -fr {smartcards.path}")
					os.system(f"cp {smartcards.original_path} {smartcards.path}")
					os.system(f"chmod 644 {smartcards.path}")
				#try:
				#	output = subprocess.check_output([f"ssh-add", "-e", f"{path}"])
				#	print("remove card output:",output)
				#except: a=1
				spawn = pexpect.spawn(f'ssh-add -s {path}')
			else:

				# start.
				spawn = pexpect.spawn(f'ssh-add {path}')

			# send lines.
			output = None
			try:

				# handle pincode.
				if smartcard:
					spawn.expect(
						f'Enter passphrase for PKCS#11:',
						timeout=timeout,
					)
					spawn.sendline(str(pin))
				
				# handle pass.
				else:
					spawn.expect(
						f'Enter passphrase for {path}:',
						timeout=timeout,
					)
					spawn.sendline(passphrase)

			except pexpect.exceptions.TIMEOUT:
				a=1
			except pexpect.exceptions.EOF:
				a=1
			
			# handle output.
			output = spawn.read().decode()

			# check success.
			if "incorrect passphrase" in output.lower():
				return r3sponse.error("Provided an incorrect passphrase.")
			elif "incorrect pin" in output.lower():
				return r3sponse.error("Provided an incorrect pin code.")
			elif "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
				if reattempt:
					ssh.utils.ssh_agent()
					return self.add(
						# the keys path.
						path=path,
						# the keys passphrase.
						passphrase=passphrase,
						# enable if you are using a smart card.
						smartcard=smartcard,
						# the smart cards pin code
						pin=pin,
						# default timeout (do not use).
						timeout=timeout,
						# reattempt (do not use).
						reattempt=False,
					)
				else:
					return r3sponse.error("Failed to communicate with the ssh-agent. Try logging out the current system user & logging back in (or execute [$ eval `ssh-agent`]).")
			elif "Identity added:" in output or "Card added:" in output: 
				return r3sponse.success(f"Successfully added key [{path}] to the ssh agent.")
			elif output != "": 
				return r3sponse.error(f"Failed to add key [{path}] to the ssh agent, error: {output}")
			else: 
				return r3sponse.error(f"Failed to add key [{path}] to the ssh agent, error: {output}")

			# handle eof.
			"""try:
				spawn.expect(pexpect.EOF, timeout=timeout)
			except pexpect.ExceptionPexpect as epe:
				return r3sponse.error(f"Failed to add key [{path}] to the ssh agent #3.")"""

		# without pass.
		else:
			output = utils.__execute__(command=["ssh-add", path], shell=False, timeout=timeout)

			# check success.
			if "Failed to communicate" in output or "agent refused operation" in output or "Error connecting to agent" in output or "Connection refused" in output:
				return r3sponse.error("Failed to communicate with the ssh-agent.")
			elif "Identity added:" in output: 
				return r3sponse.success(f"Successfully added key [{path}] to the ssh agent.")
			else: 
				return r3sponse.error(f"Failed to add key [{path}] to the ssh agent, error: {output}")

		#
	def delete(self):

		# delete keys.
		output = utils.__execute__(command=["ssh-add", "-D"])

		# check success.
		if "Could not open a connection to your authentication agent." in output:
			return r3sponse.error("Failed to communicate with the ssh-agent.")
		elif "All identities removed." in output: 
			return r3sponse.success(f"Successfully removed all keys from the ssh agent.")
		else: 
			return r3sponse.error(f"Failed to remove all keys from the ssh agent.")

		#
	def list(self):
		# initialize.
		keys = []

		# list keys.
		output = utils.__execute__(command=["ssh-add", "-L"], return_format="array")
		if "Failed to communicate" in output:
			return r3sponse.error("Failed to communicate with the ssh-agent.")
		elif "The agent has no identities." in output:
			keys = []
		else:
			keys = output
		return r3sponse.success(f"Successfully listed the agent's keys.", {
			"keys":keys,
		})

		#
	def check(self, public_key=None, raw=False):

		# check specific.
		if self.specific:
			if public_key == None:
				raw = False
				public_key = self.public_key

		# params.
		response = r3sponse.check_parameters({
			"public_key":public_key
		})
		if not response["success"]: return response

		# checks.
		if not raw and not Files.exists(public_key):
			return r3sponse.error(f"Public key path [{public_key}] does not exist.")

		# load public key.
		if not raw:
			try:
				public_key = Files.load(public_key)
			except FileNotFoundError:
				return r3sponse.error(f"Failed to load public key path [{public_key}].")

		# retrieve id from public key.
		"""
		try:
			public_key_id = public_key.split("[#id:")[1].split("]")[0]
		except IndexError:
			return r3sponse.error(f"Public key [{public_key}] does not contain any id.")

		# list.
		response = self.list()
		if response["error"] != None: return response
		success = False
		for key in response["keys"]:
			try:
				l_id = key.split("[#id:")[1].split("]")[0]
				if l_id == public_key_id:
					success = True 
					break
			except IndexError: a=1
		"""

		# list.
		response = self.list()
		if response["error"] != None: return response
		success = False
		for key in response["keys"]:
			if public_key.replace("\n","") in key:
				success = True 
				break

		# success.
		if success:
			return r3sponse.success(f"Public key [{public_key}] is added to the ssh agent.")
		else:
			return r3sponse.error(f"Public key [{public_key}] is not added to the ssh agent.")

		#
	def initialize(self):

		# check communication.
		output = utils.__execute__(command=["ssh-add", "-l"])
		#print("DEBUG; initialize output ssh-add -l:",output)
		if "Failed to communicate" in output or "Error connecting to agent" in output:
			if not self.delete()["success"]:
				l = subprocess.check_output(['eval', '"$(ssh-agent)"'], shell=True).decode()
				output = utils.__execute__(command=["ssh-add", "-l"])
				if "Failed to communicate" in output or "Error connecting to agent" in output:
					return r3sponse.error("Failed to communicate with the ssh-agent.")
				else:
					output = utils.__execute__(command=["ssh-add", "-l"])
					if "Failed to communicate" in output or "Error connecting to agent" in output:
						return r3sponse.error("Failed to communicate with the ssh-agent.")
			else:
				output = utils.__execute__(command=["ssh-add", "-l"])
				if "Failed to communicate" in output or "Error connecting to agent" in output:
					return r3sponse.error("Failed to communicate with the ssh-agent.")

		# success.
		return r3sponse.success(f"Successfully initialized the ssh agent.")

# Initialized objects.
agent = Agent()

"""

# --------------------
# SSH Agent.

# initialize the ssh agent.
response = agent.initialize()

# delete all keys from the agent.
response = agent.delete()

# add a key to the agent.
response = agent.add(
	path="/path/to/mykey/private_key", 
	passphrase="TestPass!",)

# add a smart cards key to the agent.
response = agent.add(
	path=smartcard.path, 
	smartcard=True,
	pin=123456,)

# check if a key is added to the agent.
response = agent.check("/path/to/mykey/private_key")

# list all agent keys.
response = agent.list()

"""






