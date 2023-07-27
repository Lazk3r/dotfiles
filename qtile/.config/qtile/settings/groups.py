# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles

# Qtile workspaces

from libqtile.config import Key, Group, Match
from libqtile.command import lazy
from settings.keys import mod, keys


# Get the icons at https://www.nerdfonts.com/cheat-sheet (you need a Nerd Font)

groups = [
    Group("1", label="󰖟 ", matches=[Match(wm_class=["firefox", "LibreWolf"])]),
    Group("2", label="󰉋 "),
    Group("3", label=" "),
    Group("4", label="󰌠 "),
    Group("5", label="󰛿 ", matches=[Match(wm_class=["libreoffice-startcenter", "DesktopEditors"])]),
    Group("6", label="󰎆 ", matches=[Match(wm_class=["Deadbeef"])]),
    Group("7", label="󰢚 "),
    Group("8", label=" ", matches=[Match(wm_class=["Zathura"])]),
    Group("9", label=" ", matches=[Match(wm_class=["JDownloader", "Transmission-gtk"])]),
]

for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen()),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        ]
    )
