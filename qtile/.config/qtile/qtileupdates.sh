#!/bin/sh

up="$(checkupdates 2> /dev/null | wc -l)"
ua="$(paru -Qum 2> /dev/null | wc -l)"
updates=$(( $up + $ua ))

[ $updates -eq 0 ] && echo "N/A" || echo "$updates"
