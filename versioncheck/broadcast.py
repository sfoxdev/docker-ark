import sys
import os
import re
sys.path.append(os.path.abspath("/home/steam/rcon"))
import SourceRcon

rcon = SourceRcon.SourceRcon(os.environ.get('RCON_HOST'), int(os.environ.get('RCON_PORT')), os.environ.get('RCON_PASSWORD'))
response = rcon.rcon('broadcast ' + sys.argv[1])
rcon.disconnect()