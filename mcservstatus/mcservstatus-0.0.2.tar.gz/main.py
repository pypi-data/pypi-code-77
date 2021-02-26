import mcservstatus

client = mcservstatus.MCServStatsClient()

hypixel = client.check_server("mc.hypixel.net")
print(client.uncenter_motd(hypixel["motd"]["clean"])[2])
