# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles

# Multimonitor support

from libqtile.config import Screen
from libqtile import bar
from settings.widgets import primary_widgets, secondary_widgets, bottom_widgets
import subprocess


def status_bar(widgets): return bar.Bar(widgets, 24, opacity=0.9)


screens = [Screen(top=status_bar(primary_widgets), bottom=status_bar(bottom_widgets))]

connected_monitors = subprocess.run(
    "xrandr | grep 'connected' | cut -d ' ' -f 2",
    shell=True,
    stdout=subprocess.PIPE
).stdout.decode("UTF-8").split("\n")[:-1].count("connected")

if connected_monitors > 1:
    for i in range(1, connected_monitors):
        screens.append(Screen(top=status_bar(secondary_widgets)))
