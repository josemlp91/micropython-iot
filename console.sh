#!/bin/bash

# Install minicom: sudo apt-get install minicom
# NOTE: Run as superuser.

minicom --baudrate 115200 --device /dev/ttyUSB0
