""" Vacuum tube """

import math
from .elements import Element, gap
from ..segments import Segment, SegmentArc, SegmentText

tr_d = 2.5
tr_r = 0.5 * tr_d

grid_len = 0.5 * tr_d

anode_h = 0.5 * tr_r
anode_len = math.sqrt(tr_r**2 - anode_h**2)

cathode_h = anode_h
cathode_len = math.sqrt(tr_r**2 - cathode_h**2)
cathode_gap = math.sqrt(tr_r**2 - (cathode_len / 2) ** 2)
cathode_tail = 1 / 2 * (cathode_gap - cathode_h)

half_overhang = 12.5


class Triode(Element):
    """Triode Vacuum Tube.

    Args:
        pin_nums: Show pin numbers at each anchor
        half: Draw only half of the tube. "left" for left half, "right" for right half.

    Anchors:
        * g (grid)
        * k (cathode)
        * a (anode)
    """

    def __init__(
        self, *d, leads: bool = False, pin_nums: dict = None, half: str = None, **kwargs
    ):
        super().__init__(*d, **kwargs)

        # Decide whether to draw a full circle, left half, or right half based on 'half' argument
        theta1, theta2 = (0, 360)  # Default to full circle
        if half == "left":
            theta1, theta2 = (90 - half_overhang, 270 + half_overhang)
        elif half == "right":
            theta1, theta2 = (270 - half_overhang, 90 + half_overhang)

        # Draw the triode as a circular or semicircular shape using SegmentArc
        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=theta1,
                theta2=theta2,
            )
        )

        # Grid lead as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r),
                    ((tr_d - grid_len) / 2 + grid_len, tr_r),
                ],
                ls="--",
            )
        )
        self.segments.append(Segment([(0, tr_r), ((tr_d - grid_len) / 2 - 0.1, tr_r)]))

        # Anode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - anode_len / 2, tr_r + anode_h),
                    (tr_r + anode_len / 2, tr_r + anode_h),
                ]
            )
        )
        self.segments.append(Segment([(tr_r, tr_r + anode_h), (tr_r, tr_d)]))

        # Cathode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r + cathode_len / 2, tr_r - cathode_h),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r + cathode_len / 2, tr_r - cathode_h),
                    (tr_r + cathode_len / 2, tr_r - cathode_h - cathode_tail),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r - cathode_len / 2, tr_r - cathode_gap),
                ]
            )
        )

        # Defining the anchor points
        self.anchors["g"] = (0, tr_r)  # Grid
        self.anchors["k"] = (tr_r - cathode_len / 2, tr_r - cathode_gap)  # Cathode
        self.anchors["a"] = (tr_r, tr_d)  # Anode
        self.params["drop"] = (tr_d, 0)

        # Add pin numbers if provided
        if pin_nums is not None:
            self.segments.append(
                SegmentText(((tr_d + grid_len) / 2 + 0.2, tr_r), str(pin_nums["g"]))
            )
            self.segments.append(
                SegmentText((tr_r + 0.2, tr_r + anode_h + 0.3), str(pin_nums["a"]))
            )
            self.segments.append(
                SegmentText((tr_r, tr_r - cathode_h - 0.3), str(pin_nums["k"]))
            )


class Half12AX7(Triode):
    """Half of a 12AX7 Triode.

    Inherits from the triode class above, but shows correct pin numbers. Can specify left or right.

    """

    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)

        if self.half == "left" and self.pin_nums is None:
            self.pin_nums = {"g": 2, "k": 3, "a": 1}

        elif self.half == "right" and self.pin_nums is None:
            self.pin_nums = {"g": 7, "k": 8, "a": 6}
