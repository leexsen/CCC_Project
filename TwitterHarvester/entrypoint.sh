#!/bin/bash
  
# turn on bash's job control
set -m
  
python stream_harvester.py &
python history_harvester.py