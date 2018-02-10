#!/bin/sh

sudo dscl . -create /Users/$1
sudo dscl . -create /Users/$1 UserShell /bin/bash
maxid=$(dscl . -list /Users UniqueID | awk '{print $2}' | sort -ug | tail -1)
newid=$((maxid+1))
sudo dscl . -create /Users/$1 UniqueID ${newid}
sudo dscl . -create /Users/$1 PrimaryGroupID 80
sudo dscl . -create /Users/$1 NFSHomeDirectory /Users/$1
sudo dscl . -passwd /Users/$1 $2
cp -R /System/Library/User\ Template/English.lproj /Users/$1
sudo chown -R $1:staff /Users/$1