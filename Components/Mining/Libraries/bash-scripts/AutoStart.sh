#!/bin/bash
# AutoStart
#	Simple script used to automatically re-start a rig if it goes down
# * - Requires SCREEN [sudo apt install screen]
# * - Add following text to /etc/rc.local [sudo nano /etc/rc.local]
#	'/home/MINER_NAME/AutoStart.sh 15 &'
# * - Requires execution permission(?) [sudo chmod +x AutoStart.sh]

DEFAULT_DELAY=0
if [ "x$1" = "x" -o "x$1" = "xnone" ]; then
   DELAY=$DEFAULT_DELAY
else
   DELAY=$1
fi
sleep $DELAY
cd /usr/local/claymore10.2
su MINER_NAME[REPLACE] -c "screen -dmS ethm ./mine.sh"


