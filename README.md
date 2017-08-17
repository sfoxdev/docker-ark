# ark
Automated dedicated Ark: Survival Evolved server

[![Docker Build Status](https://img.shields.io/docker/build/sfoxdev/ark.svg?style=flat-square)]()
[![Docker Build Status](https://img.shields.io/docker/automated/sfoxdev/ark.svg?style=flat-square)]()
[![Docker Build Status](https://img.shields.io/docker/pulls/sfoxdev/ark.svg?style=flat-square)]()
[![Docker Build Status](https://img.shields.io/docker/stars/sfoxdev/ark.svg?style=flat-square)]()

## ToDo
**Planned features:**

* Try to optimize the baking in of envs one might one to change
* Auto-Restart on mods update, with broadcast & delayed until no more players present

## Usage

### Start

In order to run the server, you should perform the following operations:

The save game folder `/home/steam/ark/ShooterGame/Saved` is a data volume. You should either mount in a host path or a named Docker volume container, or else Docker will create a new volume container on every start. Since Ark stores the configs inside a sub-folder `Config`, we consider them part of the save game and you can edit them there (`Game.ini`, `GameUserSettings.ini`, ...).

You will need to publish the following ports: `PORT`, `RAWPORT`, and `QUERYPORT`, the defaults of which are:

- 7777/udp
- 7778/udp
- 27015/udp
- 32330 (if you want rcon support, the password can be found and/or replaced in `/home/steam/ark/rcon_pass`)

Just changing the environment variables will not suffice for the server to work on a different port, probably the protocol has some ports hard-coded.

If turned on, the auto-update feature will automatically shut down the server when it's empty and the version mismatches. This means you must either configure the container to auto-restart (`--restart=always`) or disable the `AUTO_UPDATE=false`.

### Stop

Stopping or restarting the server will cause it to try to save the save game, however the default timeout is only 10 seconds for this. In case your save is large or your machine is slow, be sure to include a longer timeout by adding `-t 60`.

### Envs

- `SERVER_NAME` **must** be set to your desired server name (visible in the server browser)
- `MAP_NAME` can be set to load a different map (default `TheIsland`), other options at the time of writing are the DLCs `TheCenter`, `ScorchedEarth_P` and `Ragnarok`
- `MOD_LIST` can be set to a comma-separated list of mod ids to include them on the server
- `DIFFICULTY` can be set to an `OverrideOfficialDifficulty` value, if so desired, otherwise it will not be used in the start command line
- `MAX_PLAYERS` can be set to change the maximum players allowed at the same time on the server (default 70)
- `BATTLE_EYE` can be set to any value besides `true` to disable it (default `true`)
- `RCON_HOST` can be set to the external IP/DNS that your server should be reachable on
- `RCON_GAME_LOG_BUFFER` sets the max length of the game log via `?RCONServerGameLogBuffer` (default 100)
- `WHITELIST_PLAYERS` can be set to a comma-separated list of [steamID64s](https://steamid.io/) which will initialize the `PlayersJoinNoCheckList.txt` file, if it does not exist yet, and set `-exclusivejoin`. To manage the whitelisted users you can use the RCON commands `AllowPlayerToJoinNoCheck <SteamID>` and `DisallowPlayerToJoinNoCheck <SteamID>`.
- `ADDITIONAL_COMMAND_LINE` can be set to all the additional server parameters (*if they are not already supported through another env*) you want to use on start-up, e.g. `?NonPermanentDiseases=true?PreventOfflinePvP=true -insecure -noantispeedhack`. The [Ark Gamepedia](http://ark.gamepedia.com/Server_Configuration) is probably a good source for this.
- `AUTO_UPDATE` can be set to any value besides `true` to disable it (default `true`)
- `SAVE_GAME_NAME` can be set to an individual save game name (useful mainly for clusters, game default is `SavedArks`)
- `CLUSTER_NAME` can be set to a cluster id (for `-clusterid`) so that you can join multiple servers in a cluster. This will also set `-NoTransferFromFiltering`. If you want to do this make sure that:
-- You have multiple servers running, e.g. by creating a local image via `docker commit` and starting multiple instances (so you don't have to re-download all game files)
-- All the servers have the same `CLUSTER_NAME` set
-- All the servers have the same data volume mounted in
-- All the servers have a distinct `SAVE_GAME_NAME` set
-- All the servers have the default ports in the container published to distinct ports on the host
-- AFAIK the servers do **not** need to share a network
- `PORT` can be set to the desired gameport (default 7777)
- `RAWPORT` must be set to exactly `PORT+1` (never set explicitly, is only used for exposing) (default 7778)
- `QUERYPORT` can be set to the desired query port (default 27015)

### Example

1. Initial start, in this step ARK installing:

`docker run -it -p 7777:7777/udp -p 7778:7778/udp -p 27015:27015/udp --name=ark-tmp sfoxdev/ark`

2. After server started, terminate it and copy server files:

`docker cp ark-tmp:/home/steam /srv`

and

`docker stop ark-tmp && docker rm ark-tmp`

3. Make test start of server with mounted server files:

`docker run -it -v /srv/steam:/home/steam -p 7777:7777/udp -p 7778:7778/udp -p 27015:27015/udp sfoxdev/ark`

4. Run server in background:

`docker run -d -e BATTLE_EYE=true -v /srv/steam:/home/steam --restart=always --health-start-period=2m -p 7777:7777/udp -p 7778:7778/udp -p 27015:27015/udp --name=ark sfoxdev/ark`

or

`docker run -d \
-e SERVER_NAME=<server-name> \
-e MOD_LIST=<list-of-mods> \
-e DIFFICULTY=5.0 \
-e MAX_PLAYERS=10 \
-e BATTLE_EYE=false \
-e WHITELIST_PLAYERS=<censored> \
-e ADDITIONAL_COMMAND_LINE=?AllowCrateSpawnsOnTopOfStructures=true?AllowRaidDinoFeeding=true?DestroyUnconnectedWaterPipes=true?EnableExtraStructurePreventionVolumes=false?OverrideStructurePlatformPrevention=true -ForceAllowCaveFlyers -noantispeedhack -NoBattlEye \
-e CLUSTER_NAME=xcqcluster \
-v /srv/steam/ark/ShooterGame/Saved:/home/steam/ark/ShooterGame/Saved \
-p 7777:7777/udp -p 7778:7778/udp -p 27015:27015/udp \
--health-start-period=2m \
--restart=always \
sfoxdev/ark`
