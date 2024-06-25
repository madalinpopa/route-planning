#!/bin/zsh
curl -w "@scripts/curl-format.txt" -o /dev/null -s "http://localhost:5000/vehicle/list"