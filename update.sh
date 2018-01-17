#!/bin/bash

# Install before adafruit-ampy
# pip install adafruit-ampy 
# More info: https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy
# NOTE: Run as superuser

for file in ./*
do
  #Update python files and json
  if [ ${file: -3} == ".py" ] || [ ${file: -5} == ".json" ]
  then
  	ampy --port /dev/ttyUSB0 put $file
  	echo "Update" $file
  fi
done



