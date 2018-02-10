#!/bin/sh

sudo dscl . -delete /Users/$1
sudo rm -r /Users/$1