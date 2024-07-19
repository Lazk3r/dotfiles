#!/bin/bash

entries="⏻ Shutdown\n⭮ Reboot\n⏾ Suspend\n⇠ Logout\n"

selected=$(echo -e $entries|wofi --width 250 --height 210 --dmenu --cache-file /dev/null | awk '{print tolower($2)}')

case $selected in
  shutdown)
    exec systemctl poweroff -i;;
  reboot)
    exec systemctl reboot;;
  suspend)
    exec systemctl suspend;;
  logout)
    swaymsg exit;;
esac
