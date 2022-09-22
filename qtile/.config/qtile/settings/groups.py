# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles

# Qtile workspaces

from libqtile.config import Key, Group, Match
from libqtile.command import lazy
from settings.keys import mod, keys


# Get the icons at https://www.nerdfonts.com/cheat-sheet (you need a Nerd Font)

__groups = {
    1: Group(" ", matches=[Match(wm_class=["firefox", "LibreWolf"])]),
    2: Group(" "),
    3: Group(" "),
    4: Group(" ", layout="monadwide"),
    5: Group(" ", matches=[Match(wm_class=["libreoffice-startcenter", "DesktopEditors"])]),
    6: Group(" ", matches=[Match(wm_class=["Deadbeef"])]),
    7: Group(" "),
    8: Group(" ", matches=[Match(wm_class=["Zathura"])]),
    9: Group("", matches=[Match(wm_class=["JDownloader", "Transmission-gtk"])]),
}

groups = [__groups[i] for i in __groups]


def get_group_key(name):
    return [k for k, g in __groups.items() if g.name == name][0]


for i in groups:
    keys.extend([
        Key([mod], str(get_group_key(i.name)), lazy.group[i.name].toscreen()),
        Key([mod, "shift"], str(get_group_key(i.name)),
            lazy.window.togroup(i.name))
    ])
