# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles

# Qtile keybindings

from libqtile.config import Key
from libqtile.command import lazy


mod = "mod4"

keys = [Key(key[0], key[1], *key[2:]) for key in [
    # ------------ Window Configs ------------

    # Controling windows
    ([mod], "j", lazy.layout.down()),
    ([mod], "k", lazy.layout.up()),
    ([mod], "h", lazy.layout.left()),
    ([mod], "l", lazy.layout.right()),
    ([mod, "shift"], "h", lazy.layout.swap_left()),
    ([mod, "shift"], "l", lazy.layout.swap_right()),
    ([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ([mod, "shift"], "k", lazy.layout.shuffle_up()),
    ([mod], "i", lazy.layout.grow()),
    ([mod], "u", lazy.layout.shrink()),
    ([mod], "n", lazy.layout.normalize()),
    ([mod], "o", lazy.layout.maximize()),
    ([mod, "shift"], "space", lazy.layout.flip()),

    # Toggle fullscreen
    ([mod], "f", lazy.window.toggle_fullscreen()),

    # Toggle floating
    ([mod, "shift"], "f", lazy.window.toggle_floating()),

    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),
    ([mod, "shift"], "Tab", lazy.prev_layout()),

    # Kill window
    ([mod], "w", lazy.window.kill()),

    # Switch focus of monitors
    ([mod], "period", lazy.next_screen()),
    ([mod], "comma", lazy.prev_screen()),

    # Restart Qtile
    ([mod, "control"], "r", lazy.restart()),

    ([mod, "control"], "q", lazy.shutdown()),
    ([mod], "r", lazy.spawncmd()),

    ([mod, "shift"], "x", lazy.hide_show_bar("all")),

    # ------------ App Configs ------------

    # Menu
    ([mod], "m", lazy.spawn("rofi -show drun")),

    # Window Nav
    #([mod, "shift"], "m", lazy.spawn("rofi -show")),

    # Power Menu
    ([mod], "p", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu")),

    # mpv youtube
    ([mod], "y", lazy.spawn("yt -g")),

    # Browser
    ([mod], "b", lazy.spawn("firefox")),
    ([mod, "shift"], "b", lazy.spawn("brave")),

    # File Explorer
    ([mod], "e", lazy.spawn("pcmanfm")),

    # Terminal
    ([mod], "Return", lazy.spawn("kitty")),

    # Screenshot
    ([mod], "s", lazy.spawn("flameshot gui")),  # Fullscreen
    # Fullscreen with mouse
    ([mod, "control"], "s", lazy.spawn("xfce4-screenshooter -fm")),
    ([mod, "shift"], "s", lazy.spawn("xfce4-screenshooter -r")),  # Region

    # Toggle picom
    ([mod, "shift"], "a", lazy.spawn("togglepicom")),

    # Lock Screen
    ([mod, "control"], "l", lazy.spawn("slock")),

    # ------------ Hardware Configs ------------

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),

    # Media
    ([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    ([], "XF86AudioNext", lazy.spawn("playerctl next")),
    ([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
]]
