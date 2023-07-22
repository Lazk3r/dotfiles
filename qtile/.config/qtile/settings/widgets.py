# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles

from libqtile import widget
from settings.theme import colors
import subprocess

# Get the icons at https://www.nerdfonts.com/cheat-sheet (you need a Nerd Font)

base = lambda fg='text', bg='dark': {
    'foreground': colors[fg],
    'background': colors[bg]
}


def separator(): return widget.Sep(**base(), linewidth=0, padding=5)


icon = lambda fg='text', bg='dark', fontsize=16, text="?": widget.TextBox(
    **base(fg, bg),
    fontsize=fontsize,
    text=text,
    padding=3
)

powerlineLeft = lambda fg="light", bg="dark": widget.TextBox(
    **base(fg, bg),
    text="",
    fontsize=37,
    padding=-3
)

powerlineRight = lambda fg="light", bg="dark": widget.TextBox(
    **base(fg, bg),
    text="",
    fontsize=37,
    padding=-3
)


def workspaces(): return [
    #separator(),
    widget.GroupBox(
        **base(fg='light', bg='focus'),
        font='FantasqueSansMono Nerd Font',
        fontsize=19,
        margin_y=3,
        margin_x=0,
        padding_y=8,
        padding_x=5,
        borderwidth=3,
        active=colors['active'],
        inactive=colors['inactive'],
        rounded = False,
        highlight_color=colors['focus'],
        highlight_method = "line",
        this_current_screen_border=colors['light'],
        this_screen_border=colors['inactive'],
        other_current_screen_border=colors['focus'],
        other_screen_border=colors['focus'],
    ),
    powerlineRight('focus', 'dark'),
    separator(),
    widget.WindowName(**base(fg='focus'), fontsize=14, padding=5),
    separator(),
]


primary_widgets = [
    separator(),

    icon(text=' ', fg='distro'),

    powerlineRight('dark', 'focus'),

    *workspaces(),

    separator(),

    widget.Systray(background=colors['dark'], padding=5),

    powerlineLeft('color6', 'dark'),

    widget.PulseVolume(**base(bg='color6'), emoji = True),

    widget.PulseVolume(**base(bg='color6')),

    powerlineLeft('color5', 'color6'),

    icon(bg="color5", text='📥'),

    widget.GenPollText(**base(bg='color5'), update_interval=1800, fmt='{}', func=lambda: subprocess.check_output(
        "/home/lazk3r/.config/qtile/qtileupdates.sh").decode("utf-8").replace('\n', '')),

    powerlineLeft('color4', 'color5'),

    icon(bg="color4", text='🧠'),

    widget.Memory(**base(bg='color4'), format = '{MemUsed: .2f}{mm}/{MemTotal: .2f}{mm}', measure_mem = 'G'),

    powerlineLeft('color3', 'color4'),

    icon(bg="color3", text='💻 '),

    widget.CPU(**base(bg='color3'), format = '{freq_current}GHz {load_percent}%'),

    powerlineLeft('color2', 'color3'),

    widget.CurrentLayoutIcon(**base(bg='color2'), scale=0.65),

    widget.CurrentLayout(**base(bg='color2'), padding=5),

    powerlineLeft('color1', 'color2'),

    icon(bg="color1", fontsize=17, text='🗓️ '),

    widget.Clock(**base(bg='color1'), format='%d/%m/%Y - %r '),

]

bottom_widgets = [
    widget.Net(**base(bg='color5'), format = ' {down} ↓↑ {up}'),

    powerlineRight('color5', 'color6'),

    widget.ThermalSensor(**base(bg='color6'), tag_sensor = 'Package id 0'),

    icon(bg="color6", text='🌡️'),

    powerlineRight('color6', 'dark'),

    widget.Spacer(**base(bg='dark')),

    widget.GenPollText(**base(bg='dark', fg='focus'), update_interval=2, fmt='{}', func=lambda: subprocess.check_output(
        "/home/lazk3r/.config/qtile/playing.sh").decode("utf-8").replace('\n', '')),

    widget.Spacer(**base(bg='dark')),

    powerlineLeft('color4', 'dark'),

    widget.DF(**base(bg='color4'), partition = '/home/lazk3r/Datos', visible_on_warn = False, format = '💾 {uf}{m}/{s}{m} ({r:.0f}%)', update_interval = 300),

    powerlineLeft('color5', 'color4'),

    widget.DF(**base(bg='color5'), partition = '/home', visible_on_warn = False, format = '🏠 {uf}{m}/{s}{m} ({r:.0f}%)', update_interval = 300),

    powerlineLeft('color2', 'color5'),
    
    widget.DF(**base(bg='color2'), visible_on_warn = False, format = '🔒 {uf}{m}/{s}{m} ({r:.0f}%) ', update_interval = 300),
]

secondary_widgets = [
    *workspaces(),

    separator(),

    powerlineLeft('color2', 'dark'),

    widget.CurrentLayoutIcon(**base(bg='color2'), scale=0.65),

    widget.CurrentLayout(**base(bg='color2'), padding=5),
]

widget_defaults = {
    'font': 'FantasqueSansMono Nerd Font Bold',
    'fontsize': 14,
    'padding': 1,
}
extension_defaults = widget_defaults.copy()
