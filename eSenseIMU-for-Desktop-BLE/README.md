# eSenseIMU-for-Desktop-BLE

# **ESENSE - EARABLE IMU DATA COLLECTOR**

**Setup**


Install Dependencies: Make sure you have the following Python libraries installed:
 - asyncio
 - Bleak
 - nest_asyncio
 - pandas
 - matplotlib


**YOU CAN DIRECTLY RUN THE requirement.txt FILE.**


**Follow the video for connection steps**


https://youtu.be/AERe5T_Sv1E


**Configuring IMU Parameters**

Once the connection is established, you can proceed to the configuration section in the notebook. Adjust the IMU parameters as desired:
You can tweek:
 - Offsets
 - Sensing Range
 - Low pass filter cut off Freq.
 - Sampling rate


This notebook will connect to your esense earable having IMU and will create a csv file with name 'imu_data.csv' in the same directory. it will replace everytime you run the data collection code.

Official esense BLE Sheet is used. 
https://www.esense.io/share/eSense-BLE-Specification.pdf


**Troubleshooting**


If the connection to the eSense device is unsuccessful, consider the following:

- Verify MAC Address: Ensure that the MAC address entered in the code matches the MAC address of your eSense device.

 - Reconnect the Device: Disconnect and reconnect your eSense device to the computer.

 - Check for Other Connections: Ensure that no other device is currently connected to the eSense earable.

**Contributors
Sameeran Zingre**

Welcome for contribution...


