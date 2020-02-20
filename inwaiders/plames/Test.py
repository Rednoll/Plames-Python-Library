from inwaiders.plames.network import plames_client
from inwaiders.plames.network import data_packets

import time
import struct
import cProfile

plames_client.connect("localhost", 9090)


def test():

    discord_profile = plames_client.request("DiscordProfile", "getById", [44770])

    print(str(discord_profile.user.profiles_container.primary_profile.user))

test()
