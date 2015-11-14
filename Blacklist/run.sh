#!/bin/bash

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as sudo or root only!" 1>&2
   exit 1
fi

if ls -l blacklist.txt &> /dev/null; then
    while read line; do sudo ufw delete deny from $line; done < blacklist.txt
fi

if python3 Blacklister.py $*; then
    while read line; do sudo ufw deny from $line; done < blacklist.txt
fi


