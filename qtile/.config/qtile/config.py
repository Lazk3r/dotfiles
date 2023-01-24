# Qtile Config File
# http://www.qtile.org/

# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles


from libqtile import hook

from settings.keys import mod, keys
from settings.groups import groups
from settings.layouts import layouts, floating_layout
from settings.widgets import widget_defaults, extension_defaults
from settings.screens import screens
from settings.mouse import mouse
from settings.path import qtile_path

from os import path
import subprocess


@hook.subscribe.startup_once
def autostart():
    subprocess.call([path.join(qtile_path, 'autostart.sh')])


@hook.subscribe.layout_change
def _(layout, group):
    if layout.name == "max":
        for i in group.windows:
            i.window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
        @hook.subscribe.client_new
        def _(win):
            win.window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
    elif layout.name == "monadtall":
        if len(group.windows) <= 1:
            group.windows[0].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
            group.windows[1].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
            @hook.subscribe.client_new
            def _(win):
                win.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
                for i in group.windows:
                    i.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            @hook.subscribe.client_killed
            def _(win):
                if len(group.windows) <= 2:
                    group.windows[0].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
                    group.windows[1].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
        else:
            for i in group.windows:
                i.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            @hook.subscribe.client_new
            def _(win):
                win.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
                for i in group.windows:
                    i.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            @hook.subscribe.client_killed
            def _(win):
                if len(group.windows) <= 2:
                    group.windows[0].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
                    group.windows[1].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
    else:
        for i in group.windows:
            i.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)


@hook.subscribe.startup_once
def _():
    @hook.subscribe.group_window_add
    def _(group, win):
        if len(group.windows) == 0:
            win.window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
        else:
            for i in group.windows:
                i.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            @hook.subscribe.client_killed
            def _(win):
                if len(group.windows) <= 2:
                    group.windows[0].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
                    group.windows[1].window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)


main = None
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
auto_fullscreen = True
focus_on_window_activation = 'urgent'
wmname = 'LG3D'
