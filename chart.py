"""
version: chart.py v1.2

author: OpenSource@ultimate-solar.com

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

"""
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import DateFormatter

import os
import re

debug = True

data_path = '/home/user/projects/temper/data'
timestamps = []
internal_temps = []
external_temps = []

# Iterate over all files in the directory
for filename in os.listdir(data_path):
    file = os.path.join(data_path, filename)

    if os.path.isfile(file): # Check if the current item is a file (not a subdirectory)
        # open the data file
        file = open(file)
        # read the file as a list
        lines = file.readlines()
        # close the file
        file.close()

        length = len(lines)
        for counter in range(length):
            counter += 1
            if debug:
                if counter > 1000: break # currently only view first 100 lines for debugging

            try:
                line = lines[counter]
                next_line = lines[counter+1]
                next_next_line = lines[counter+2]

                line = re.sub('\s+','',line) # remove all whitespace
                next_line = re.sub('\s+','',next_line)
                next_next_line = re.sub('\s+','',next_next_line)

                if len(line) == 0: # ignore empty lines
                    continue
    
                if "===" in line and "internaltemperature" in next_line and "externaltemperature" in next_next_line: # a time line was found
                    element_array = line.split("===") # try to detect 2024-01-24===11:16:5 lines
                    date_string = re.sub('\s+','',element_array[0])
                    time_string = re.sub('\s+','',element_array[1])
                    timestamps.append(date_string+" "+time_string)
    
                    element_array = next_line.split(":") # try to detect 2024-01-24===11:16:5 lines
                    internaltemperature = re.sub('\s+','',element_array[1])
                    internaltemperature = internaltemperature.replace(",", "")
                    internal_temps.append(internaltemperature)
    
                    element_array = next_next_line.split(":") # try to detect 2024-01-24===11:16:5 lines
                    externaltemperature = re.sub('\s+','',element_array[1])
                    externaltemperature = externaltemperature.replace(",", "")
                    external_temps.append(externaltemperature)
            except IndexError:
                status = "IndexError: list index out of range"
                    

# Sample data for both temperature measurements
# timestamps = ['2024-01-24 11:16:57', '2024-01-24 12:30:00', '2024-01-24 14:45:30', '2024-01-24 16:00:00']
# print(internal_temps+"\n")
internal_temps_len = len(internal_temps)
# print(external_temps+"\n")
external_temps_len = len(external_temps)
# print(timestamps+"\n")
timestamps_len = len(timestamps)

"""
# output data to file
file_path = "./output.txt"
with open(file_path, 'a') as file:
    # Iterate over the array and append each element to the file
    for element in internal_temps:
        file.write(element + '\n')
    for element in external_temps:
        file.write(element + '\n')
    for element in timestamps:
        file.write(element + '\n')
"""


# Convert timestamps to datetime objects
x_values = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

# Plotting the External temperature chart
plt.plot(x_values, external_temps, marker='o', linestyle='-', color='orange', label='External')

# to display the 12°C value at every dot uncomment next 2 lines:
# for x, y in zip(x_values, external_temps):
#    plt.text(x, y, f'{y}', ha='center', va='bottom', fontsize=8)

# Plotting the Internal temperature chart
plt.plot(x_values, internal_temps, marker='o', linestyle='-', color='blue', label='Internal')

# to display the 12°C value at every dot uncomment next 2 lines:
#for x, y in zip(x_values, internal_temps):
#    plt.text(x, y, f'{y}', ha='center', va='bottom', fontsize=8)

# Adding labels and title
plt.xlabel('Time')
plt.ylabel('Temperature (°C)')
plt.title('TEMPer2 Chart')

# Formatting the x-axis to display the date and time
plt.xticks(rotation=45, ha='right', rotation_mode='anchor', fontsize=8)

# Formatting the x-axis to display the date and time in YYYY-MM-DD hh:mm format
date_formatter = DateFormatter('%Y-%m-%d %H:%M')
plt.gca().xaxis.set_major_formatter(date_formatter)
plt.gcf().autofmt_xdate()

# Adding legend
plt.legend()

# Display the plot
plt.show()
