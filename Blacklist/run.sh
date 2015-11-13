#!/bin/bash

if ls -l blacklist.txt &> /dev/null; then
    while read line; do sudo ufw delete deny from $line; done < blacklist.txt
fi

python3 Blacklister.py $*;
while read line; do sudo ufw deny from $line; done < blacklist.txt


