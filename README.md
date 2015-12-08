<p align="center">
<img src="https://camo.githubusercontent.com/e5f920c5307880a177e04dc98e3f717d1234e4f1/68747470733a2f2f687572726963616e656c6162732e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031342f31322f616e64726f69645f666f72656e736963735f6d656469756d2e6a7067" />
# Android Connections Forensics

This software enables a forensic investigator to map each connection to its originating process.

It doesn't require root privliges on the system, but do require adb & USB debugging.

# Installation

    pip install -r requirments.txt

# Usage

Make sure you device is connected, usb debugging is enabled and authorized.
    adb devices

To run Acf:
    python acf.py -d [Device serial number]

# Output
Acf create 3 different output types:
1. console output - live connections
2. acm-log file - live connections
3. metadata file - external IP's metadata results

acm-log example:
<img src="http://i.imgur.com/CkRp6LV.png" />
# Contact Us

Itayk@CyberHat.co.il