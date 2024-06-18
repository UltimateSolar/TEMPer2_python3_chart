# === version: chart.py v1.2 ===
creditz: OpenSource ÄÄÄÄT ultimate-solar DOOOOT com

## === What does it do? ===

plot a chart of TEMPer2 temperature data (1x internal temp sensor, 1x external (metal) temp sensor)

## === How to install? + Requirements? ===

connect TEMPer2 USB thermometer to PC

make the script TEMPer2.sh auto start and run as root on startup
and it will read every Xsec the values of all TEMPer2 USB thermometers to file

su - root
apt install python3
apt-get install python3-serial
apt install python3-matplotlib

# will need 2x tools that will be stored in
mkdir software
cd software

# tool1: to query the usb thermometer
git clone https://github.com/greg-kodama/temper.git
cd temper/
git checkout TEMPer2_V4.1

# give it a testrun
/usr/bin/python3 ./temper.py --json

# should print out
[
    {
        "vendorid": 13651,
        "productid": 40961,
        "manufacturer": "PCsensor",
        "product": "TEMPer2",
        "busnum": 1,
        "devnum": 3,
        "devices": [
            "hidraw1",
            "hidraw2"
        ],
        "port": "1-3",
        "firmware": "TEMPer2_V4.1",
        "hex_firmware": "54454d506572325f56342e3100000000",
        "hex_data": "8080092e4e200000800108664e200000",
        "internal temperature": 23.5,
        "external temperature": 21.5
    }
]

(if not open an issue https://github.com/ccwienk/temper/issues
as the company behind TEMPer2 might have changed firmware)

`
# tool2: will use tool1 to get data
git clone https://github.com/UltimateSolar/TEMPer2_python3_chart.git
mkdir /scripts
# modify script
vim ./TEMPer2_python3_chart/TEMPer2.sh
# absolute path to temper.py tool1
/home/user/software/temper/temper.py --json|grep "temperature"|tee -a $LOGFILE;
# interval between data taking (too much data = chart will look ugly)
sleep 60;

cp -rv ./TEMPer2_python3_chart/TEMPer2.sh /scripts
chmod +x /scripts/*.sh

# create a way to auto run this script (as root) on startup
echo '#!/bin/sh -e' >> /etc/rc.local
echo '/scripts/TEMPer2.sh &' >> /etc/rc.local
echo 'exit 0' >> /etc/rc.local

chmod +x /etc/rc.local;
systemctl daemon-reload;
systemctl start rc-local;
systemctl status rc-local;

# where data will be stored
mkdir /scripts/TEMPer2.data

# if the data shall be written somewhere else modify
vim chart.py
# modify where the data will be
pata_path = '/scripts/TEMPer2.data'

# as root run it and check it displays data
/scripts/TEMPer2.sh

# open 2nd terminal non-root
/usr/bin/python3 /home/user/software/TEMPer2_python3_chart/chart.py


it should display a graph with 2x lines (Internal (inside the usb stick) and external temps)
CONGRATS :)

hostnamectl; # tested on, but also Debian, should work on almost any GNU Linux
Operating System: Ubuntu 22.04.3 LTS              
          Kernel: Linux 5.15.0-91-generic
    Architecture: x86-64

PS: may the src be with the user!

test
