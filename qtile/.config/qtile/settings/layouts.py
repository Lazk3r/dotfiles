# Julian Gallego
# https://gitlab.com/lazk3r/dotfiles

import math
from collections import namedtuple
from libqtile.layout.base import _SimpleLayoutBase
from libqtile import layout
from settings.theme import colors
from libqtile.config import Match
from libqtile.backend.base import Window
from libqtile.layout.base import Layout


# Modifine the default Max layouts
# A modifide version of Max layout from the source code of qtile
class Max(_SimpleLayoutBase):
    defaults = [
        ("margin", 0, "Margin of the layout (int or list of ints [N E S W])"),
        ("border_focus", "#0000ff", "Border colour(s) for the window when focused"),
        ("border_normal", "#000000", "Border colour(s) for the window when not focused"),
        ("border_width", 0, "Border width."),
    ]

    def __init__(self, **config):
        _SimpleLayoutBase.__init__(self, **config)
        self.add_defaults(Max.defaults)

    def add(self, client):
        return super().add(client, 1)

    def configure(self, client, screen_rect):
        if self.clients and client is self.clients.current_client:
            client.window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
            client.place(
                screen_rect.x,
                screen_rect.y,
                screen_rect.width - self.border_width * 2,
                screen_rect.height - self.border_width * 2,
                self.border_width,
                self.border_focus if client.has_focus else self.border_normal,
                margin=self.margin,
            )
            client.unhide()
        else:
            client.hide()

    cmd_previous = _SimpleLayoutBase.previous
    cmd_next = _SimpleLayoutBase.next

    cmd_up = cmd_previous
    cmd_down = cmd_next
# End Modifine the default Max layouts

# Modifine the default Monadtall layouts
# A modifide version of Monadtall layout from the source code of qtile
class MonadTall(_SimpleLayoutBase):
    _left = 0
    _right = 1

    defaults = [
        ("border_focus", "#ff0000", "Border colour(s) for the focused window."),
        ("border_normal", "#000000", "Border colour(s) for un-focused windows."),
        ("border_width", 2, "Border width."),
        ("single_border_width", None, "Border width for single window"),
        ("single_margin", None, "Margin size for single window"),
        ("margin", 0, "Margin of the layout"),
        (
            "ratio",
            0.5,
            "The percent of the screen-space the master pane should occupy " "by default.",
        ),
        (
            "min_ratio",
            0.25,
            "The percent of the screen-space the master pane should occupy " "at minimum.",
        ),
        (
            "max_ratio",
            0.75,
            "The percent of the screen-space the master pane should occupy " "at maximum.",
        ),
        ("min_secondary_size", 85, "minimum size in pixel for a secondary pane window "),
        (
            "align",
            _left,
            "Which side master plane will be placed "
            "(one of ``MonadTall._left`` or ``MonadTall._right``)",
        ),
        ("change_ratio", 0.05, "Resize ratio"),
        ("change_size", 20, "Resize change in pixels"),
        (
            "new_client_position",
            "after_current",
            "Place new windows: "
            " after_current - after the active window."
            " before_current - before the active window,"
            " top - at the top of the stack,"
            " bottom - at the bottom of the stack,",
        ),
    ]

    def __init__(self, **config):
        _SimpleLayoutBase.__init__(self, **config)
        self.add_defaults(MonadTall.defaults)
        if self.single_border_width is None:
            self.single_border_width = self.border_width
        if self.single_margin is None:
            self.single_margin = self.margin
        self.relative_sizes = []
        self.screen_rect = None
        self.default_ratio = self.ratio

    @property
    def focused(self):
        return self.clients.current_index

    def _get_relative_size_from_absolute(self, absolute_size):
        return absolute_size / self.screen_rect.height

    def _get_absolute_size_from_relative(self, relative_size):
        return int(relative_size * self.screen_rect.height)

    def clone(self, group):
        "Clone layout for other groups"
        c = _SimpleLayoutBase.clone(self, group)
        c.sizes = []
        c.relative_sizes = []
        c.screen_rect = group.screen.get_rect() if group.screen else None
        c.ratio = self.ratio
        c.align = self.align
        return c

    def add(self, client):
        "Add client to layout"
        self.clients.add(client, client_position=self.new_client_position)
        self.do_normalize = True

    def remove(self, client):
        "Remove client from layout"
        self.do_normalize = True
        return self.clients.remove(client)

    def cmd_set_ratio(self, ratio):
        "Directly set the main pane ratio"
        ratio = min(self.max_ratio, ratio)
        self.ratio = max(self.min_ratio, ratio)
        self.group.layout_all()

    def cmd_normalize(self, redraw=True):
        "Evenly distribute screen-space among secondary clients"
        n = len(self.clients) - 1  # exclude main client, 0
        # if secondary clients exist
        if n > 0 and self.screen_rect is not None:
            self.relative_sizes = [1.0 / n] * n
        # reset main pane ratio
        if redraw:
            self.group.layout_all()
        self.do_normalize = False

    def cmd_reset(self, ratio=None, redraw=True):
        "Reset Layout."
        self.ratio = ratio or self.default_ratio
        if self.align == self._right:
            self.align = self._left
        self.cmd_normalize(redraw)

    def _maximize_main(self):
        "Toggle the main pane between min and max size"
        if self.ratio <= 0.5 * (self.max_ratio + self.min_ratio):
            self.ratio = self.max_ratio
        else:
            self.ratio = self.min_ratio
        self.group.layout_all()

    def _maximize_secondary(self):
        "Toggle the focused secondary pane between min and max size"
        n = len(self.clients) - 2  # total shrinking clients
        # total size of collapsed secondaries
        collapsed_size = self.min_secondary_size * n
        nidx = self.focused - 1  # focused size index
        # total height of maximized secondary
        maxed_size = self.group.screen.dheight - collapsed_size
        # if maximized or nearly maximized
        if (
            abs(self._get_absolute_size_from_relative(self.relative_sizes[nidx]) - maxed_size)
            < self.change_size
        ):
            # minimize
            self._shrink_secondary(
                self._get_absolute_size_from_relative(self.relative_sizes[nidx])
                - self.min_secondary_size
            )
        # otherwise maximize
        else:
            self._grow_secondary(maxed_size)

    def cmd_maximize(self):
        "Grow the currently focused client to the max size"
        # if we have 1 or 2 panes or main pane is focused
        if len(self.clients) < 3 or self.focused == 0:
            self._maximize_main()
        # secondary is focused
        else:
            self._maximize_secondary()
        self.group.layout_all()

    def configure(self, client, screen_rect):
        "Position client based on order and sizes"
        self.screen_rect = screen_rect

        # if no sizes or normalize flag is set, normalize
        if not self.relative_sizes or self.do_normalize:
            self.cmd_normalize(False)

        # if client not in this layout
        if not self.clients or client not in self.clients:
            client.hide()
            return

        # determine focus border-color
        if client.has_focus:
            px = self.border_focus
        else:
            px = self.border_normal

        # single client - fullscreen
        if len(self.clients) == 1:
            client.window.set_property("ROUND_CORNERS", 1, "CARDINAL", 32)
            client.place(
                self.screen_rect.x,
                self.screen_rect.y,
                self.screen_rect.width - 2 * self.single_border_width,
                self.screen_rect.height - 2 * self.single_border_width,
                self.single_border_width,
                px,
                margin=self.single_margin,
            )
            client.unhide()
            return
        cidx = self.clients.index(client)
        self._configure_specific(client, screen_rect, px, cidx)
        client.unhide()

    def _configure_specific(self, client, screen_rect, px, cidx):
        """Specific configuration for xmonad tall."""
        self.screen_rect = screen_rect

        # calculate main/secondary pane size
        width_main = int(self.screen_rect.width * self.ratio)
        width_shared = self.screen_rect.width - width_main

        # calculate client's x offset
        if self.align == self._left:  # left or up orientation
            if cidx == 0:
                # main client
                xpos = self.screen_rect.x
            else:
                # secondary client
                xpos = self.screen_rect.x + width_main
        else:  # right or down orientation
            if cidx == 0:
                # main client
                xpos = self.screen_rect.x + width_shared - self.margin
            else:
                # secondary client
                xpos = self.screen_rect.x

        # calculate client height and place
        if cidx > 0:
            # secondary client
            width = width_shared - 2 * self.border_width
            # ypos is the sum of all clients above it
            ypos = self.screen_rect.y + self._get_absolute_size_from_relative(
                sum(self.relative_sizes[: cidx - 1])
            )
            # get height from precalculated height list
            height = self._get_absolute_size_from_relative(self.relative_sizes[cidx - 1])
            # fix double margin
            if cidx > 1:
                ypos -= self.margin
                height += self.margin
            # place client based on calculated dimensions
            client.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            client.place(
                xpos,
                ypos,
                width,
                height - 2 * self.border_width,
                self.border_width,
                px,
                margin=self.margin,
            )
        else:
            # main client
            client.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            client.place(
                xpos,
                self.screen_rect.y,
                width_main,
                self.screen_rect.height,
                self.border_width,
                px,
                margin=[
                    self.margin,
                    2 * self.border_width,
                    self.margin + 2 * self.border_width,
                    self.margin,
                ],
            )

    def info(self):
        d = _SimpleLayoutBase.info(self)
        d.update(
            dict(
                main=d["clients"][0] if self.clients else None,
                secondary=d["clients"][1::] if self.clients else [],
            )
        )
        return d

    def get_shrink_margin(self, cidx):
        "Return how many remaining pixels a client can shrink"
        return max(
            0,
            self._get_absolute_size_from_relative(self.relative_sizes[cidx])
            - self.min_secondary_size,
        )

    def shrink(self, cidx, amt):
        """Reduce the size of a client

        Will only shrink the client until it reaches the configured minimum
        size. Any amount that was prevented in the resize is returned.
        """
        # get max resizable amount
        margin = self.get_shrink_margin(cidx)
        if amt > margin:  # too much
            self.relative_sizes[cidx] -= self._get_relative_size_from_absolute(margin)
            return amt - margin
        else:
            self.relative_sizes[cidx] -= self._get_relative_size_from_absolute(amt)
            return 0

    def shrink_up(self, cidx, amt):
        """Shrink the window up

        Will shrink all secondary clients above the specified index in order.
        Each client will attempt to shrink as much as it is able before the
        next client is resized.

        Any amount that was unable to be applied to the clients is returned.
        """
        left = amt  # track unused shrink amount
        # for each client before specified index
        for idx in range(0, cidx):
            # shrink by whatever is left-over of original amount
            left -= left - self.shrink(idx, left)
        # return unused shrink amount
        return left

    def shrink_up_shared(self, cidx, amt):
        """Shrink the shared space

        Will shrink all secondary clients above the specified index by an equal
        share of the provided amount. After applying the shared amount to all
        affected clients, any amount left over will be applied in a non-equal
        manner with ``shrink_up``.

        Any amount that was unable to be applied to the clients is returned.
        """
        # split shrink amount among number of clients
        per_amt = amt / cidx
        left = amt  # track unused shrink amount
        # for each client before specified index
        for idx in range(0, cidx):
            # shrink by equal amount and track left-over
            left -= per_amt - self.shrink(idx, per_amt)
        # apply non-equal shrinkage secondary pass
        # in order to use up any left over shrink amounts
        left = self.shrink_up(cidx, left)
        # return whatever could not be applied
        return left

    def shrink_down(self, cidx, amt):
        """Shrink current window down

        Will shrink all secondary clients below the specified index in order.
        Each client will attempt to shrink as much as it is able before the
        next client is resized.

        Any amount that was unable to be applied to the clients is returned.
        """
        left = amt  # track unused shrink amount
        # for each client after specified index
        for idx in range(cidx + 1, len(self.relative_sizes)):
            # shrink by current total left-over amount
            left -= left - self.shrink(idx, left)
        # return unused shrink amount
        return left

    def shrink_down_shared(self, cidx, amt):
        """Shrink secondary clients

        Will shrink all secondary clients below the specified index by an equal
        share of the provided amount. After applying the shared amount to all
        affected clients, any amount left over will be applied in a non-equal
        manner with ``shrink_down``.

        Any amount that was unable to be applied to the clients is returned.
        """
        # split shrink amount among number of clients
        per_amt = amt / (len(self.relative_sizes) - 1 - cidx)
        left = amt  # track unused shrink amount
        # for each client after specified index
        for idx in range(cidx + 1, len(self.relative_sizes)):
            # shrink by equal amount and track left-over
            left -= per_amt - self.shrink(idx, per_amt)
        # apply non-equal shrinkage secondary pass
        # in order to use up any left over shrink amounts
        left = self.shrink_down(cidx, left)
        # return whatever could not be applied
        return left

    def _grow_main(self, amt):
        """Will grow the client that is currently in the main pane"""
        self.ratio += amt
        self.ratio = min(self.max_ratio, self.ratio)

    def _grow_solo_secondary(self, amt):
        """Will grow the solitary client in the secondary pane"""
        self.ratio -= amt
        self.ratio = max(self.min_ratio, self.ratio)

    def _grow_secondary(self, amt):
        """Will grow the focused client in the secondary pane"""
        half_change_size = amt / 2
        # track unshrinkable amounts
        left = amt
        # first secondary (top)
        if self.focused == 1:
            # only shrink downwards
            left -= amt - self.shrink_down_shared(0, amt)
        # last secondary (bottom)
        elif self.focused == len(self.clients) - 1:
            # only shrink upwards
            left -= amt - self.shrink_up(len(self.relative_sizes) - 1, amt)
        # middle secondary
        else:
            # get size index
            idx = self.focused - 1
            # shrink up and down
            left -= half_change_size - self.shrink_up_shared(idx, half_change_size)
            left -= half_change_size - self.shrink_down_shared(idx, half_change_size)
            left -= half_change_size - self.shrink_up_shared(idx, half_change_size)
            left -= half_change_size - self.shrink_down_shared(idx, half_change_size)
        # calculate how much shrinkage took place
        diff = amt - left
        # grow client by diff amount
        self.relative_sizes[self.focused - 1] += self._get_relative_size_from_absolute(diff)

    def cmd_grow(self):
        """Grow current window

        Will grow the currently focused client reducing the size of those
        around it. Growing will stop when no other secondary clients can reduce
        their size any further.
        """
        if self.focused == 0:
            self._grow_main(self.change_ratio)
        elif len(self.clients) == 2:
            self._grow_solo_secondary(self.change_ratio)
        else:
            self._grow_secondary(self.change_size)
        self.group.layout_all()

    def cmd_grow_main(self):
        """Grow main pane

        Will grow the main pane, reducing the size of clients in the secondary
        pane.
        """
        self._grow_main(self.change_ratio)
        self.group.layout_all()

    def cmd_shrink_main(self):
        """Shrink main pane

        Will shrink the main pane, increasing the size of clients in the
        secondary pane.
        """
        self._shrink_main(self.change_ratio)
        self.group.layout_all()

    def grow(self, cidx, amt):
        "Grow secondary client by specified amount"
        self.relative_sizes[cidx] += self._get_relative_size_from_absolute(amt)

    def grow_up_shared(self, cidx, amt):
        """Grow higher secondary clients

        Will grow all secondary clients above the specified index by an equal
        share of the provided amount.
        """
        # split grow amount among number of clients
        per_amt = amt / cidx
        for idx in range(0, cidx):
            self.grow(idx, per_amt)

    def grow_down_shared(self, cidx, amt):
        """Grow lower secondary clients

        Will grow all secondary clients below the specified index by an equal
        share of the provided amount.
        """
        # split grow amount among number of clients
        per_amt = amt / (len(self.relative_sizes) - 1 - cidx)
        for idx in range(cidx + 1, len(self.relative_sizes)):
            self.grow(idx, per_amt)

    def _shrink_main(self, amt):
        """Will shrink the client that currently in the main pane"""
        self.ratio -= amt
        self.ratio = max(self.min_ratio, self.ratio)

    def _shrink_solo_secondary(self, amt):
        """Will shrink the solitary client in the secondary pane"""
        self.ratio += amt
        self.ratio = min(self.max_ratio, self.ratio)

    def _shrink_secondary(self, amt):
        """Will shrink the focused client in the secondary pane"""
        # get focused client
        client = self.clients[self.focused]

        # get default change size
        change = amt

        # get left-over height after change
        left = client.height - amt
        # if change would violate min_secondary_size
        if left < self.min_secondary_size:
            # just reduce to min_secondary_size
            change = client.height - self.min_secondary_size

        # calculate half of that change
        half_change = change / 2

        # first secondary (top)
        if self.focused == 1:
            # only grow downwards
            self.grow_down_shared(0, change)
        # last secondary (bottom)
        elif self.focused == len(self.clients) - 1:
            # only grow upwards
            self.grow_up_shared(len(self.relative_sizes) - 1, change)
        # middle secondary
        else:
            idx = self.focused - 1
            # grow up and down
            self.grow_up_shared(idx, half_change)
            self.grow_down_shared(idx, half_change)
        # shrink client by total change
        self.relative_sizes[self.focused - 1] -= self._get_relative_size_from_absolute(change)

    cmd_next = _SimpleLayoutBase.next
    cmd_previous = _SimpleLayoutBase.previous

    def cmd_shrink(self):
        """Shrink current window

        Will shrink the currently focused client reducing the size of those
        around it. Shrinking will stop when the client has reached the minimum
        size.
        """
        if self.focused == 0:
            self._shrink_main(self.change_ratio)
        elif len(self.clients) == 2:
            self._shrink_solo_secondary(self.change_ratio)
        else:
            self._shrink_secondary(self.change_size)
        self.group.layout_all()

    cmd_up = cmd_previous
    cmd_down = cmd_next

    def cmd_shuffle_up(self):
        """Shuffle the client up the stack"""
        self.clients.shuffle_up()
        self.group.layout_all()
        self.group.focus(self.clients.current_client)

    def cmd_shuffle_down(self):
        """Shuffle the client down the stack"""
        self.clients.shuffle_down()
        self.group.layout_all()
        self.group.focus(self.clients[self.focused])

    def cmd_flip(self):
        """Flip the layout horizontally"""
        self.align = self._left if self.align == self._right else self._right
        self.group.layout_all()

    def _get_closest(self, x, y, clients):
        """Get closest window to a point x,y"""
        target = min(
            clients,
            key=lambda c: math.hypot(c.x - x, c.y - y),
            default=self.clients.current_client,
        )
        return target

    def cmd_swap(self, window1, window2):
        """Swap two windows"""
        self.clients.swap(window1, window2, 1)
        self.group.layout_all()
        self.group.focus(window1)

    def cmd_swap_left(self):
        """Swap current window with closest window to the left"""
        win = self.clients.current_client
        x, y = win.x, win.y
        candidates = [c for c in self.clients if c.info()["x"] < x]
        target = self._get_closest(x, y, candidates)
        self.cmd_swap(win, target)

    def cmd_swap_right(self):
        """Swap current window with closest window to the right"""
        win = self.clients.current_client
        x, y = win.x, win.y
        candidates = [c for c in self.clients if c.info()["x"] > x]
        target = self._get_closest(x, y, candidates)
        self.cmd_swap(win, target)

    def cmd_swap_main(self):
        """Swap current window to main pane"""
        if self.align == self._left:
            self.cmd_swap_left()
        elif self.align == self._right:
            self.cmd_swap_right()

    def cmd_left(self):
        """Focus on the closest window to the left of the current window"""
        win = self.clients.current_client
        x, y = win.x, win.y
        candidates = [c for c in self.clients if c.info()["x"] < x]
        self.clients.current_client = self._get_closest(x, y, candidates)
        self.group.focus(self.clients.current_client)

    def cmd_right(self):
        """Focus on the closest window to the right of the current window"""
        win = self.clients.current_client
        x, y = win.x, win.y
        candidates = [c for c in self.clients if c.info()["x"] > x]
        self.clients.current_client = self._get_closest(x, y, candidates)
        self.group.focus(self.clients.current_client)

    cmd_shuffle_left = cmd_swap_left
    cmd_shuffle_right = cmd_swap_right
# End Modifine the default Monadtall layouts

# Modifine the default MonadWide layouts
# A modifide version of MonadWide layout from the source code of qtile
class MonadWide(MonadTall):
    _up = 0
    _down = 1

    def _get_relative_size_from_absolute(self, absolute_size):
        return absolute_size / self.screen_rect.width

    def _get_absolute_size_from_relative(self, relative_size):
        return int(relative_size * self.screen_rect.width)

    def _maximize_secondary(self):
        """Toggle the focused secondary pane between min and max size."""
        n = len(self.clients) - 2  # total shrinking clients
        # total size of collapsed secondaries
        collapsed_size = self.min_secondary_size * n
        nidx = self.focused - 1  # focused size index
        # total width of maximized secondary
        maxed_size = self.screen_rect.width - collapsed_size
        # if maximized or nearly maximized
        if (
            abs(self._get_absolute_size_from_relative(self.relative_sizes[nidx]) - maxed_size)
            < self.change_size
        ):
            # minimize
            self._shrink_secondary(
                self._get_absolute_size_from_relative(self.relative_sizes[nidx])
                - self.min_secondary_size
            )
        # otherwise maximize
        else:
            self._grow_secondary(maxed_size)

    def _configure_specific(self, client, screen_rect, px, cidx):
        """Specific configuration for xmonad wide."""
        self.screen_rect = screen_rect

        # calculate main/secondary column widths
        height_main = int(self.screen_rect.height * self.ratio)
        height_shared = self.screen_rect.height - height_main

        # calculate client's x offset
        if self.align == self._up:  # up orientation
            if cidx == 0:
                # main client
                ypos = self.screen_rect.y
            else:
                # secondary client
                ypos = self.screen_rect.y + height_main
        else:  # right or down orientation
            if cidx == 0:
                # main client
                ypos = self.screen_rect.y + height_shared - self.margin
            else:
                # secondary client
                ypos = self.screen_rect.y

        # calculate client height and place
        if cidx > 0:
            # secondary client
            height = height_shared - 2 * self.border_width
            # xpos is the sum of all clients left of it
            xpos = self.screen_rect.x + self._get_absolute_size_from_relative(
                sum(self.relative_sizes[: cidx - 1])
            )
            # get width from precalculated width list
            width = self._get_absolute_size_from_relative(self.relative_sizes[cidx - 1])
            # fix double margin
            if cidx > 1:
                xpos -= self.margin
                width += self.margin
            # place client based on calculated dimensions
            client.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            client.place(
                xpos,
                ypos,
                width - 2 * self.border_width,
                height,
                self.border_width,
                px,
                margin=self.margin,
            )
        else:
            # main client
            client.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            client.place(
                self.screen_rect.x,
                ypos,
                self.screen_rect.width,
                height_main,
                self.border_width,
                px,
                margin=[
                    self.margin,
                    self.margin + 2 * self.border_width,
                    2 * self.border_width,
                    self.margin,
                ],
            )

    def _shrink_secondary(self, amt):
        """Will shrink the focused client in the secondary pane"""
        # get focused client
        client = self.clients[self.focused]

        # get default change size
        change = amt

        # get left-over height after change
        left = client.width - amt
        # if change would violate min_secondary_size
        if left < self.min_secondary_size:
            # just reduce to min_secondary_size
            change = client.width - self.min_secondary_size

        # calculate half of that change
        half_change = change / 2

        # first secondary (top)
        if self.focused == 1:
            # only grow downwards
            self.grow_down_shared(0, change)
        # last secondary (bottom)
        elif self.focused == len(self.clients) - 1:
            # only grow upwards
            self.grow_up_shared(len(self.relative_sizes) - 1, change)
        # middle secondary
        else:
            idx = self.focused - 1
            # grow up and down
            self.grow_up_shared(idx, half_change)
            self.grow_down_shared(idx, half_change)
        # shrink client by total change
        self.relative_sizes[self.focused - 1] -= self._get_relative_size_from_absolute(change)

    def cmd_swap_left(self):
        """Swap current window with closest window to the down"""
        win = self.clients.current_client
        x, y = win.x, win.y
        candidates = [c for c in self.clients.clients if c.info()["y"] > y]
        target = self._get_closest(x, y, candidates)
        self.cmd_swap(win, target)

    def cmd_swap_right(self):
        """Swap current window with closest window to the up"""
        win = self.clients.current_client
        x, y = win.x, win.y
        candidates = [c for c in self.clients if c.info()["y"] < y]
        target = self._get_closest(x, y, candidates)
        self.cmd_swap(win, target)

    def cmd_swap_main(self):
        """Swap current window to main pane"""
        if self.align == self._up:
            self.cmd_swap_right()
        elif self.align == self._down:
            self.cmd_swap_left()
# End Modifine the default MonadWide layouts

# Modifine the default Floating layouts
# A modifide version of Floating layout from the source code of qtile

class Floating(Layout):
    """
    Floating layout, which does nothing with windows but handles focus order
    """

    default_float_rules = [
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_type="toolbar"),
        Match(wm_type="splash"),
        Match(wm_type="dialog"),
        Match(wm_class="file_progress"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(func=lambda c: c.has_fixed_size()),
        Match(func=lambda c: c.has_fixed_ratio()),
    ]

    defaults = [
        ("border_focus", "#0000ff", "Border colour(s) for the focused window."),
        ("border_normal", "#000000", "Border colour(s) for un-focused windows."),
        ("border_width", 1, "Border width."),
        ("max_border_width", 0, "Border width for maximize."),
        ("fullscreen_border_width", 0, "Border width for fullscreen."),
    ]

    def __init__(
        self, float_rules: list[Match] | None = None, no_reposition_rules=None, **config
    ):
        """
        If you have certain apps that you always want to float you can provide
        ``float_rules`` to do so. ``float_rules`` are a list of
        Match objects::

            from libqtile.config import Match
            Match(title=WM_NAME, wm_class=WM_CLASS, role=WM_WINDOW_ROLE)

        When a new window is opened its ``match`` method is called with each of
        these rules.  If one matches, the window will float.  The following
        will float GIMP and Skype::

            from libqtile.config import Match
            float_rules=[Match(wm_class="skype"), Match(wm_class="gimp")]

        The following ``Match`` will float all windows that are transient windows for a
        parent window:

            Match(func=lambda c: bool(c.is_transient_for()))

        Specify these in the ``floating_layout`` in your config.

        Floating layout will try to center most of floating windows by default,
        but if you don't want this to happen for certain windows that are
        centered by mistake, you can use ``no_reposition_rules`` option to
        specify them and layout will rely on windows to position themselves in
        correct location on the screen.
        """
        Layout.__init__(self, **config)
        self.clients: list[Window] = []
        self.focused = None
        self.group = None

        if float_rules is None:
            float_rules = self.default_float_rules

        self.float_rules = float_rules
        self.no_reposition_rules = no_reposition_rules or []
        self.add_defaults(Floating.defaults)

    def match(self, win):
        """Used to default float some windows"""
        return any(win.match(rule) for rule in self.float_rules)

    def find_clients(self, group):
        """Find all clients belonging to a given group"""
        return [c for c in self.clients if c.group is group]

    def to_screen(self, group, new_screen):
        """Adjust offsets of clients within current screen"""
        for win in self.find_clients(group):
            if win.maximized:
                win.maximized = True
            elif win.fullscreen:
                win.fullscreen = True
            else:
                # If the window hasn't been floated before, it will be configured in
                # .configure()
                if win.float_x is not None and win.float_y is not None:
                    # By default, place window at same offset from top corner
                    new_x = new_screen.x + win.float_x
                    new_y = new_screen.y + win.float_y
                    # make sure window isn't off screen left/right...
                    new_x = min(new_x, new_screen.x + new_screen.width - win.width)
                    new_x = max(new_x, new_screen.x)
                    # and up/down
                    new_y = min(new_y, new_screen.y + new_screen.height - win.height)
                    new_y = max(new_y, new_screen.y)

                    win.x = new_x
                    win.y = new_y
            win.group = new_screen.group

    def focus_first(self, group=None):
        if group is None:
            clients = self.clients
        else:
            clients = self.find_clients(group)

        if clients:
            return clients[0]

    def focus_next(self, win):
        if win not in self.clients or win.group is None:
            return

        clients = self.find_clients(win.group)
        idx = clients.index(win)
        if len(clients) > idx + 1:
            return clients[idx + 1]

    def focus_last(self, group=None):
        if group is None:
            clients = self.clients
        else:
            clients = self.find_clients(group)

        if clients:
            return clients[-1]

    def focus_previous(self, win):
        if win not in self.clients or win.group is None:
            return

        clients = self.find_clients(win.group)
        idx = clients.index(win)
        if idx > 0:
            return clients[idx - 1]

    def focus(self, client):
        self.focused = client

    def blur(self):
        self.focused = None

    def on_screen(self, client, screen_rect):
        if client.x < screen_rect.x:  # client's left edge
            return False
        if screen_rect.x + screen_rect.width < client.x + client.width:  # right
            return False
        if client.y < screen_rect.y:  # top
            return False
        if screen_rect.y + screen_rect.width < client.y + client.height:  # bottom
            return False
        return True

    def compute_client_position(self, client, screen_rect):
        """recompute client.x and client.y, returning whether or not to place
        this client above other windows or not"""
        above = True

        if client.has_user_set_position() and not self.on_screen(client, screen_rect):
            # move to screen
            client.x = screen_rect.x + client.x
            client.y = screen_rect.y + client.y
        if not client.has_user_set_position() or not self.on_screen(client, screen_rect):
            # client has not been properly placed before or it is off screen
            transient_for = client.is_transient_for()
            if transient_for is not None:
                # if transient for a window, place in the center of the window
                center_x = transient_for.x + transient_for.width / 2
                center_y = transient_for.y + transient_for.height / 2
                above = False
            else:
                center_x = screen_rect.x + screen_rect.width / 2
                center_y = screen_rect.y + screen_rect.height / 2

            x = center_x - client.width / 2
            y = center_y - client.height / 2

            # don't go off the right...
            x = min(x, screen_rect.x + screen_rect.width - client.width)
            # or left...
            x = max(x, screen_rect.x)
            # or bottom...
            y = min(y, screen_rect.y + screen_rect.height - client.height)
            # or top
            y = max(y, screen_rect.y)

            client.x = int(round(x))
            client.y = int(round(y))
        return above

    def configure(self, client, screen_rect):
        if client.has_focus:
            bc = self.border_focus
        else:
            bc = self.border_normal

        if client.maximized:
            bw = self.max_border_width
        elif client.fullscreen:
            bw = self.fullscreen_border_width
        else:
            bw = self.border_width

        # 'sun-awt-X11-XWindowPeer' is a dropdown used in Java application,
        # don't reposition it anywhere, let Java app to control it
        cls = client.get_wm_class() or ""
        is_java_dropdown = "sun-awt-X11-XWindowPeer" in cls
        if is_java_dropdown:
            client.paint_borders(bc, bw)
            client.cmd_bring_to_front()

        # alternatively, users may have asked us explicitly to leave the client alone
        elif any(m.compare(client) for m in self.no_reposition_rules):
            client.paint_borders(bc, bw)
            client.cmd_bring_to_front()

        else:
            above = False

            # We definitely have a screen here, so let's be sure we'll float on screen
            if client.float_x is None or client.float_y is None:
                # this window hasn't been placed before, let's put it in a sensible spot
                above = self.compute_client_position(client, screen_rect)

            client.window.set_property("ROUND_CORNERS", 0, "CARDINAL", 32)
            client.place(
                client.x,
                client.y,
                client.width,
                client.height,
                bw,
                bc,
                above,
                respect_hints=True,
            )
        client.unhide()

    def add(self, client):
        self.clients.append(client)
        self.focused = client

    def remove(self, client):
        if client not in self.clients:
            return

        next_focus = self.focus_next(client)
        if client is self.focused:
            self.blur()
        self.clients.remove(client)
        return next_focus

    def get_windows(self):
        return self.clients

    def info(self):
        d = Layout.info(self)
        d["clients"] = [c.name for c in self.clients]
        return d

    def cmd_next(self):
        # This can't ever be called, but implement the abstract method
        pass

    def cmd_previous(self):
        # This can't ever be called, but implement the abstract method
        pass
# End Modifine the default Floating layouts

# Layouts and layout rules


layout_conf = {
    'border_focus': colors['focus'][0],
    'border_width': 0,
    'margin': 10
}

layouts = [
    MonadTall(**layout_conf, single_margin=0),
    Max(),
    MonadWide(**layout_conf, single_margin=0),
    # layout.Bsp(**layout_conf),
    # layout.Matrix(columns=3, **layout_conf),
    # layout.RatioTile(**layout_conf),
    # layout.Floating(**layout_conf),
    # layout.Columns(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="Steam"),
        Match(wm_class="epicgameslauncher.exe"),
    ],
    border_focus=colors["color4"][0],
    border_width=0
)
