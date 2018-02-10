#!/bin/sh

admin=$1
grep -v $2 /Users/${admin}/.ssh/authorized_keys > /Users/${admin}/.ssh/tmp_auth
mv /Users/${admin}/.ssh/tmp_auth /Users/${admin}/.ssh/authorized_keys