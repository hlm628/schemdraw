""" Transformer element definitions """

from ..segments import Segment, SegmentArc
from .elements import Element
from .twoterm import cycloid
from ..types import XformTap


class Transformer(Element):
    """Transformer

    Add taps to the windings on either side using
    the `.taps` method.

    Args:
        t1: Turns on primary (left) side
        t2: Turns on secondary (right) side
        t2_list: List of turns on secondary side (overrides t2)
        core: Draw the core (parallel lines)
        loop: Use spiral/cycloid (loopy) style

    Anchors:
        * p1: primary side 1
        * p2: primary side 2
        * s1(_i): secondary side 1, for each winding
        * s2(_i): secondary side 2, for each winding
        * Other anchors defined by `taps` method
    """

    def __init__(
        self,
        *d,
        t1: int = 4,
        t2: int = 4,
        t2_list: list = None,
        core: bool = True,
        loop: bool = False,
        **kwargs,
    ):
        super().__init__(*d, **kwargs)
        ind_w = 0.4
        lbot = 0.0
        ltop = t1 * ind_w
        if t2_list is None:
            t2_list = [t2]
        else:
            t2 = sum(t2_list) + len(t2_list) - 1
        rtop = (ltop + lbot) / 2 + t2 * ind_w / 2
        rbot = (ltop + lbot) / 2 - t2 * ind_w / 2

        # Adjust for loops or core
        ind_gap = 0.75
        if loop:
            ind_gap = ind_gap + 0.4
        if core:
            ind_gap = ind_gap + 0.25

        ltapx = 0.0
        rtapx = ind_gap

        # Draw primary windings
        if loop:
            ltapx, ltop = self.draw_loops(t1, (0, 0))
        else:
            self.draw_coils(t1, (0, ltop), ind_w)

        # Draw secondary windings
        rtapx_list = []
        if loop:
            for j in range(len(t2_list)):
                rtapx, rtop = self.draw_loops(
                    t2_list[j],
                    (ind_gap, (ltop - lbot) / 2 - (sum(t2_list[:j]) + j) * ind_w / 2),
                    flip=True,
                )
                rtapx_list.append(rtapx)
        else:
            for j in range(len(t2_list)):
                self.draw_coils(
                    t2_list[j],
                    (ind_gap, rtop - (sum(t2_list[:j]) + j) * ind_w),
                    ind_w,
                    flip=True,
                )

        # Add the core
        if core:
            top = max(ltop, rtop)
            bot = min(lbot, rbot)
            center = ind_gap / 2
            core_w = ind_gap / 10
            self.segments.append(
                Segment([(center - core_w, top), (center - core_w, bot)])
            )
            self.segments.append(
                Segment([(center + core_w, top), (center + core_w, bot)])
            )

        self.anchors["p1"] = (0, ltop)
        self.anchors["p2"] = (0, lbot)
        if len(t2_list) == 1:
            self.anchors["s1"] = (ind_gap, rtop)
            self.anchors["s2"] = (ind_gap, rbot)
        else:
            for j in range(len(t2_list)):
                self.anchors[f"s1_{j+1}"] = (
                    ind_gap,
                    rtop - (sum(t2_list[:j]) + j) * ind_w,
                )
                self.anchors[f"s2_{j+1}"] = (
                    ind_gap,
                    rtop - (sum(t2_list[: j + 1]) + j) * ind_w,
                )

        self._ltapx = ltapx  # Save these for adding taps
        self._rtapx = rtapx
        self._ltop = ltop
        self._rtop = rtop
        self._ind_w = ind_w
        self._t2_list = t2_list

        if "ltaps" in kwargs:
            for name, pos in kwargs["ltaps"].items():
                self.tap(name, pos, "primary")
        if "rtaps" in kwargs:
            for name, pos in kwargs["rtaps"].items():
                if isinstance(pos, int):
                    self.tap(name, pos, "secondary")
                else:
                    winding, pos = pos
                    self.tap(name, pos, "secondary", winding)

    def draw_loops(self, n, ofst, flip=False):
        """Draw loops on one side of the transformer

        Args:
            n: Number of loops
            ofst: Offset position to center loop
            flip: Flip the loops (for secondary side)
        """
        c = cycloid(loops=n, ofst=ofst, flip=flip, norm=False, vertical=True)
        tapx = min([i[0] for i in c])
        top = c[-1][1]
        self.segments.append(Segment(c))
        return tapx, top

    def draw_coils(self, n, ofst, radius, flip=False):
        """Draw coils on one side of the transformer

        Args:
            n: Number of coils
            ofst: Offset position to center coil
            radius: Radius of coil
            flip: Flip the coils (for secondary side)
        """

        theta1, theta2 = 270, 90

        if flip:
            theta2, theta1 = theta1, theta2

        x, y = ofst

        for i in range(n):
            self.segments.append(
                SegmentArc(
                    (x, y - (i * radius + radius / 2)),
                    theta1=theta1,
                    theta2=theta2,
                    width=radius,
                    height=radius,
                )
            )

    def tap(self, name: str, pos: int, side: XformTap = "primary", winding: int = 0):
        """Add a tap

        A tap is simply a named anchor definition along one side
        of the transformer.

        Args:
            name: Name of the tap/anchor
            pos: Turn number from the top of the tap
            side: Primary (left) or Secondary (right) side
        """
        if side in ["left", "primary"]:
            self.anchors[name] = (self._ltapx, self._ltop - pos * self._ind_w)
        elif side in ["right", "secondary"]:
            self.anchors[name] = (
                self._rtapx,
                self._rtop
                - ((sum(self._t2_list[:winding]) + winding + pos) * self._ind_w),
            )
        else:
            raise ValueError(f"Undefined tap side {side}")
        return self
