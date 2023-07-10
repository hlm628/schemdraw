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

dual_tr_gap = 0.5 * tr_r
dual_tr_grid_offset = 0.25

pent_gap = dual_tr_gap


class VacuumTube(Element):
    """
    Parent class for all the tubes defined below.

    Args:
        pin_nums: Show pin numbers at each anchor
        draw_heaters: Whether to draw heater filaments
    """

    def __init__(self, *d, pin_nums: dict = None, draw_heaters: bool = False, **kwargs):
        super().__init__(*d, **kwargs)

        self.pin_nums = pin_nums
        self.draw_heaters = draw_heaters

    def draw_heaters(self):
        """Draw heater filaments"""
        x_extent, _ = self.anchors["drop"]

        self.segments.append(Segment([(x_extent / 2 - 0.2, 0), (x_extent, 0.2)]))

        self.segments.append(Segment([(x_extent / 2 + 0.2, 0), (x_extent, 0.2)]))

    def draw_pin_num(self, location, num):
        self.segments.append(
            SegmentText(
                location, str(num)
            )
        )


class Triode(VacuumTube):
    """Triode Vacuum Tube.

    Args:
        pin_nums: Show pin numbers at each anchor
        half: Draw only half of the tube. "left" for left half, "right" for right half.

    Anchors:
        * g (grid)
        * k (cathode)
        * a (anode)
    """

    def __init__(self, *d, pin_nums: dict = None, half: str = None, **kwargs):
        super().__init__(*d, **kwargs)

        self.pin_nums = pin_nums
        self.half = half

        half_sign = 1 if self.half == "right" else -1

        # Decide whether to draw a full circle, left half, or right half based on 'half' argument
        theta1, theta2 = (0, 360)  # Default to full circle
        if self.half == "left":
            theta1, theta2 = (90 - half_overhang, 270 + half_overhang)
        elif self.half == "right":
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
        self.segments.append(
            Segment(
                [
                    (tr_r + half_sign * tr_r, tr_r),
                    ((tr_d + half_sign * grid_len) / 2 + half_sign * 0.1, tr_r),
                ]
            )
        )

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
                    (tr_r - half_sign * cathode_len / 2, tr_r - cathode_h),
                    (
                        tr_r - half_sign * cathode_len / 2,
                        tr_r - cathode_h - cathode_tail,
                    ),
                ]
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_r + half_sign * cathode_len / 2, tr_r - cathode_h),
                    (tr_r + half_sign * cathode_len / 2, tr_r - cathode_gap),
                ]
            )
        )

        # Defining the anchor points
        self.anchors["g"] = (tr_r + half_sign * tr_r, tr_r)  # Grid
        self.anchors["k"] = (
            tr_r + half_sign * cathode_len / 2,
            tr_r - cathode_gap,
        )  # Cathode
        self.anchors["a"] = (tr_r, tr_d)  # Anode
        self.params["drop"] = (tr_d, 0)

        # Add pin numbers if provided
        if self.pin_nums is not None:
            self.segments.append(
                SegmentText(
                    ((tr_d - half_sign * grid_len) / 2 - half_sign * 0.2, tr_r),
                    str(self.pin_nums["g"]),
                )
            )
            self.segments.append(
                SegmentText(
                    (tr_r - half_sign * 0.2, tr_r + anode_h + 0.3),
                    str(self.pin_nums["a"]),
                )
            )
            self.segments.append(
                SegmentText((tr_r, tr_r - cathode_h - 0.3), str(self.pin_nums["k"]))
            )


class DualTriode(VacuumTube):
    """Dual Triode Vacuum Tube.

    Args:
        pin_nums: Show pin numbers at each anchor

    Anchors:
        * g1 (grid of first triode)
        * g2 (grid of second triode)
        * k1 (cathode of first triode)
        * k2 (cathode of second triode)
        * a1 (anode of first triode)
        * a2 (anode of second triode)
    """

    def __init__(self, *d, pin_nums: dict = None, **kwargs):
        super().__init__(*d, **kwargs)

        self.pin_nums = pin_nums

        # Draw the triode outline
        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=90,
                theta2=270,
            )
        )

        self.segments.append(Segment([(tr_r, 0), (tr_r + dual_tr_gap, 0)]))

        self.segments.append(Segment([(tr_r, tr_d), (tr_r + dual_tr_gap, tr_d)]))

        self.segments.append(
            SegmentArc(
                center=(tr_r + dual_tr_gap, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=270,
                theta2=90,
            )
        )

        # Grid lead as dotted lines
        self.segments.append(
            Segment(
                [
                    (dual_tr_grid_offset + (tr_d - grid_len) / 2, tr_r),
                    (
                        dual_tr_grid_offset + (tr_d - grid_len) / 2 + 0.5 * grid_len,
                        tr_r,
                    ),
                ],
                ls="--",
            )
        )

        self.segments.append(
            Segment(
                [
                    (
                        (tr_d + dual_tr_gap)
                        - (dual_tr_grid_offset + (tr_d - grid_len) / 2),
                        tr_r,
                    ),
                    (
                        (tr_d + dual_tr_gap)
                        - (
                            dual_tr_grid_offset + (tr_d - grid_len) / 2 + 0.5 * grid_len
                        ),
                        tr_r,
                    ),
                ],
                ls="--",
            )
        )

        self.segments.append(
            Segment(
                [
                    (
                        tr_d + dual_tr_gap - (grid_len / 2) + 0.1 - dual_tr_grid_offset,
                        tr_r,
                    ),
                    (tr_d + dual_tr_gap, tr_r),
                ]
            )
        )

        self.segments.append(
            Segment(
                [
                    (0, tr_r),
                    ((tr_d - grid_len) / 2 - 0.1 + dual_tr_grid_offset, tr_r),
                ]
            )
        )

        # Anode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - anode_len / 2, tr_r + anode_h),
                    (tr_r + anode_len / 2 + dual_tr_gap, tr_r + anode_h),
                ]
            )
        )
        self.segments.append(Segment([(tr_r, tr_r + anode_h), (tr_r, tr_d)]))
        self.segments.append(
            Segment([(tr_r + dual_tr_gap, tr_r + anode_h), (tr_r + dual_tr_gap, tr_d)])
        )

        # Cathode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - cathode_len / 2, tr_r - cathode_h),
                    (tr_r + cathode_len / 2 + dual_tr_gap, tr_r - cathode_h),
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
        self.segments.append(
            Segment(
                [
                    (tr_r + cathode_len / 2 + dual_tr_gap, tr_r - cathode_h),
                    (tr_r + cathode_len / 2 + dual_tr_gap, tr_r - cathode_gap),
                ]
            )
        )

        ## Defining the anchor points
        # Grids
        self.anchors["g1"] = (0, tr_r)  # Grids
        self.anchors["g2"] = (tr_d + dual_tr_gap, tr_r)

        # Cathodes
        self.anchors["k1"] = (
            tr_r - cathode_len / 2,
            tr_r - cathode_gap,
        )
        self.anchors["k2"] = (
            tr_r + cathode_len / 2 + dual_tr_gap,
            tr_r - cathode_gap,
        )

        # Anodes
        self.anchors["a1"] = (tr_r - anode_len / 2, tr_d)
        self.anchors["a2"] = (tr_r + anode_len / 2 + dual_tr_gap, tr_d)

        self.params["drop"] = (tr_d + dual_tr_gap, 0)

        # Add pin numbers if provided
        if self.pin_nums is not None:
            # Grids
            self.segments.append(
                SegmentText(
                    (0.3, tr_r + 0.2),
                    str(self.pin_nums["g1"]),
                )
            )
            self.segments.append(
                SegmentText(
                    (tr_d + dual_tr_gap - 0.3, tr_r + 0.2),
                    str(self.pin_nums["g2"]),
                )
            )

            # Anodes
            self.segments.append(
                SegmentText(
                    (tr_r - 0.2, tr_r + anode_h + 0.3),
                    str(self.pin_nums["a1"]),
                )
            )
            self.segments.append(
                SegmentText(
                    (tr_r + dual_tr_gap + 0.2, tr_r + anode_h + 0.3),
                    str(self.pin_nums["a2"]),
                )
            )

            # Cathodes
            self.segments.append(
                SegmentText(
                    (tr_r - cathode_gap / 2 + 0.3, tr_r - cathode_h - 0.3),
                    str(self.pin_nums["k1"]),
                )
            )
            self.segments.append(
                SegmentText(
                    (
                        tr_r + cathode_gap / 2 + dual_tr_gap - 0.3,
                        tr_r - cathode_h - 0.3,
                    ),
                    str(self.pin_nums["k2"]),
                )
            )


def Half12AX7(half="left", **kwargs):
    """Half of a 12AX7 Triode.

    Uses the Triode class above, but shows correct pin numbers. Can specify left or right.

    Args:
        half: "left" or "right" half of the tube

    """

    if half == "left":
        pin_nums = {"g": 2, "k": 3, "a": 1}

    elif half == "right":
        pin_nums = {"g": 7, "k": 8, "a": 6}

    return Triode(half=half, pin_nums=pin_nums, **kwargs)


def _12AX7(**kwargs):
    """Full 12AX7 Triode.

    Uses the DualTriode class above, but shows correct pin numbers.
    """

    return DualTriode(
        pin_nums={"g1": 2, "k1": 3, "a1": 1, "g2": 7, "k2": 8, "a2": 6}, **kwargs
    )


ECC83 = _12AX7
HalfECC83 = Half12AX7


class Pentode(VacuumTube):
    """Pentode Vacuum Tube.

    Args:
        pin_nums: Show pin numbers at each anchor

    Anchors:
        * g1 (grid)
        * g2 (screen grid)
        * g3 (suppressor grid)
        * k (cathode)
        * a (anode)
    """

    def __init__(self, *d, pin_nums: dict = None, **kwargs):
        super().__init__(*d, **kwargs)

        self.pin_nums = pin_nums

        # Draw the pentode outline
        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r),
                width=tr_d,
                height=tr_d,
                theta1=180,
                theta2=0,
            )
        )

        self.segments.append(
            Segment(
                [
                    (0, tr_r),
                    (0, tr_r + pent_gap),
                ]
            )
        )

        self.segments.append(
            Segment(
                [
                    (tr_d, tr_r),
                    (tr_d, tr_r + pent_gap),
                ]
            )
        )

        self.segments.append(
            SegmentArc(
                center=(tr_r, tr_r + pent_gap),
                width=tr_d,
                height=tr_d,
                theta1=0,
                theta2=180,
            )
        )

        # Grid lead as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r),
                    ((tr_d + grid_len) / 2, tr_r),
                ],
                ls="--",
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_d, tr_r),
                    ((tr_d + grid_len) / 2 + 0.1, tr_r),
                ]
            )
        )

        # Screen grid as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r + pent_gap / 2),
                    ((tr_d + grid_len) / 2, tr_r + pent_gap / 2),
                ],
                ls="--",
            )
        )
        self.segments.append(
            Segment(
                [
                    (0, tr_r + pent_gap / 2),
                    (grid_len / 2 - 0.1, tr_r + pent_gap / 2),
                ]
            )
        )

        # Suppressor grid as a dotted line
        self.segments.append(
            Segment(
                [
                    ((tr_d - grid_len) / 2, tr_r + pent_gap),
                    ((tr_d + grid_len) / 2, tr_r + pent_gap),
                ],
                ls="--",
            )
        )
        self.segments.append(
            Segment(
                [
                    (tr_d, tr_r + pent_gap),
                    ((tr_d + grid_len) / 2 + 0.1, tr_r + pent_gap),
                ]
            )
        )

        # Anode leads
        self.segments.append(
            Segment(
                [
                    (tr_r - anode_len / 2, tr_r + pent_gap + anode_h),
                    (tr_r + anode_len / 2, tr_r + pent_gap + anode_h),
                ]
            )
        )
        self.segments.append(
            Segment([(tr_r, tr_r + pent_gap + anode_h), (tr_r, tr_d + pent_gap)])
        )

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
                    (
                        tr_r + cathode_len / 2,
                        tr_r - cathode_h - cathode_tail,
                    ),
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
        self.anchors["g1"] = (tr_d, tr_r)  # Grid
        self.anchors["g2"] = (0, tr_r + pent_gap / 2)  # Screen
        self.anchors["g3"] = (tr_d, tr_r + pent_gap)  # Suppressor
        self.anchors["k"] = (
            tr_r - cathode_len / 2,
            tr_r - cathode_gap,
        )  # Cathode
        self.anchors["a"] = (tr_r, tr_d + pent_gap)  # Anode
        self.params["drop"] = (tr_d, 0)

        # Add pin numbers if provided
        if self.pin_nums is not None:
            self.segments.append(
                SegmentText(
                    (tr_r - grid_len / 2 - 0.2, tr_r),
                    str(self.pin_nums["g1"]),
                )
            )
            self.segments.append(
                SegmentText(
                    (tr_d - grid_len / 2 + 0.2, tr_r + pent_gap / 2),
                    str(self.pin_nums["g2"]),
                )
            )

            self.segments.append(
                SegmentText(
                    (tr_r - grid_len / 2 - 0.2, tr_r + pent_gap),
                    str(self.pin_nums["g3"]),
                )
            )

            self.segments.append(
                SegmentText(
                    (tr_r + 0.2, tr_r + pent_gap + anode_h + 0.2),
                    str(self.pin_nums["a"]),
                )
            )
            self.segments.append(
                SegmentText((tr_r, tr_r - cathode_h - 0.3), str(self.pin_nums["k"]))
            )


def KT66(**kwargs):
    """KT66 Pentode.

    Uses the Pentode class above, but shows correct pin numbers.
    """

    return Pentode(pin_nums={"g1": 5, "g2": 4, "g3": "", "a": 3, "k": 8}, **kwargs)


def EL34(**kwargs):
    """EL34 Pentode.

    Uses the Pentode class above, but shows correct pin numbers.
    """

    return Pentode(pin_nums={"g1": 5, "g2": 4, "g3": 1, "a": 3, "k": 8}, **kwargs)
