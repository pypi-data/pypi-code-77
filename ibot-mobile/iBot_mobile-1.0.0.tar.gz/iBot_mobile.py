import socket
import subprocess

class iBot_mobile_connecting():
	def __init__(self):
		proc_list = subprocess.Popen('screenfetch', stdout=subprocess.PIPE)
		data = proc_list.communicate()
		for liner in data:
			if liner:
				liner = liner.strip()
				line = liner.decode("cp866")
				print(line.split())
				print("\n")
				print(line[177:220])
				print(line[506:550])
				info = line[177:220]
				ROM = line[506:550]
		def connecting():
			global info
			global ROM
			print("connecting...")
			print(info)
			ptint(ROM)
		connecting()
