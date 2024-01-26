version: chart.py v1.2

author: OpenSource ÄÄÄT ultimate-solar DOOOOT com

What does it do?

plot a chart of TEMPer2 temperature data (1x internal temp sensor, 1x external (metal) temp sensor)

Requirements?

su - root

apt install python3

apt install python3-matplotlib

git clone https://github.com/greg-kodama/temper.git

cd temper/

git checkout TEMPer2_V4.1

How to install?

make the script TEMPer2.sh auto start and run as root on startup
and it will read every 60sec the values of all TEMPer2 USB thermometers to file
(modify sleep 60; line in script, but too much data = chart looks ugly)

this file ./data/2024-01-24.TEMPer2.log
will be read by chart.py to display a chart

Tested on:

hostnamectl; # debian and many other should work also
Operating System: Ubuntu 22.04.3 LTS              
          Kernel: Linux 5.15.0-91-generic
    Architecture: x86-64


