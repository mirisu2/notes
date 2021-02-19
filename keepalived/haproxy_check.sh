#!/bin/sh
# HAProxy Service status check
SERVICE=haproxy
STATUS="$(sudo pidof $SERVICE | wc -w)"
if [ $STATUS -eq 0 ]
then
  exit 1
else
  exit 0
fi
