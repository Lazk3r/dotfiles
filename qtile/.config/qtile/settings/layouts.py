# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles

from libqtile import layout
from settings.theme import colors
from libqtile.config import Match

# Layouts and layout rules


layout_conf = {
    'border_focus': colors['focus'][0],
    'border_width': 0,
    'margin': 10
}

layouts = [
    layout.MonadTall(**layout_conf),
    layout.Max(),
    layout.MonadWide(**layout_conf),
    layout.Bsp(**layout_conf),
    layout.Matrix(columns=3, **layout_conf),
    layout.RatioTile(**layout_conf),
    layout.Floating(**layout_conf),
    # layout.Columns(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="Steam"),
        Match(wm_class="epicgameslauncher.exe"),
    ],
    border_focus=colors["color4"][0],
    border_width=0
)
