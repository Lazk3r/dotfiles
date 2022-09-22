#!/bin/sh

playing="$(playerctl metadata --format "{{ artist }} - {{ title }}")"

[ "$playing" = "" ] && echo "" || echo " ${playing} "
