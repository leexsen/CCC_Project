#!/bin/bash
  
# turn on bash's job control
set -m
  
# Start the primary process and put it in the background
python stream_harvester.py &
  
# Start the helper process
python history_harvester.py