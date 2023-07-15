""" Other elements """

from .elements import Element, Element2Term, gap
from .twoterm import resheight
from ..segments import Segment, SegmentPoly, SegmentArc, SegmentCircle


class Speaker(Element):
    """Speaker element with two inputs.

    Anchors:
        * in1
        * in2
    """

    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        sph = 0.5
        self.segments.append(Segment([(0, 0), (resheight, 0)]))
        self.segments.append(Segment([(0, -sph), (resheight, -sph)]))
        self.segments.append(
            SegmentPoly(
                [
                    (resheight, sph / 2),
                    (resheight, -sph * 1.5),
                    (resheight * 2, -sph * 1.5),
                    (resheight * 2, sph / 2),
                ]
            )
        )
        self.segments.append(
            SegmentPoly(
                [
                    (resheight * 2, sph / 2),
                    (resheight * 3.5, sph * 1.25),
                    (resheight * 3.5, -sph * 2.25),
                    (resheight * 2, -sph * 1.5),
                ],
                closed=False,
            )
        )
        self.anchors["in1"] = (0, 0)
        self.anchors["in2"] = (0, -sph)
        self.params["drop"] = (0, -sph)


class Mic(Element):
    """Microphone element with two inputs.

    Anchors:
        * in1
        * in2
    """

    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        sph = 0.5
        self.segments.append(Segment([(0, 0), (resheight, 0)]))  # Upper lead
        self.segments.append(Segment([(0, -sph), (resheight, -sph)]))  # Lower lead
        self.segments.append(
            Segment(  # Vertical flat
                [(-resheight * 2, resheight), (-resheight * 2, -resheight * 3)]
            )
        )
        self.segments.append(
            SegmentArc(
                (-resheight * 2, -resheight),
                theta1=270,
                theta2=90,
                width=resheight * 4,
                height=resheight * 4,
            )
        )
        self.anchors["in1"] = (resheight, 0)
        self.anchors["in2"] = (resheight, -sph)
        self.params["drop"] = (0, -sph)


class Motor(Element2Term):
    """Motor"""

    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        mw = 0.22
        self.segments.append(
            Segment([(-mw, 0), (-mw, 0), gap, (1 + mw, 0), (1 + mw, 0)])
        )
        self.segments.append(Segment([(0, -mw), (0 - mw, -mw), (0 - mw, mw), (0, mw)]))
        self.segments.append(Segment([(1, -mw), (1 + mw, -mw), (1 + mw, mw), (1, mw)]))
        self.segments.append(SegmentCircle((0.5, 0), 0.5))


class AudioJack(Element):
    """Audio Jack with 2 or 3 connectors and optional switches.

    Args:
        ring: Show ring (third conductor) contact
        switch: Show switch on tip contact
        ringswitch: Show switch on ring contact
        dots: Show connector dots
        radius: Radius of connector dots
        extend_sleeve: Extend sleeve to right

    Anchors:
        * tip
        * sleeve
        * ring
        * ringswitch
        * tipswitch
    """

    def __init__(
        self,
        *d,
        radius: float = 0.075,
        ring: bool = False,
        ringswitch: bool = False,
        dots: bool = True,
        switch: bool = False,
        open: bool = True,
        extend_sleeve: bool = True,
        **kwargs
    ):
        super().__init__(*d, **kwargs)
        fill = "bg" if open else None

        length = 2.0
        ringlen = 0.75
        tiplen = 0.55
        swidth = 0.2
        sleeveheight = 1.0
        tipy = 1.0
        ringy = 0.1
        sleevey = 0.35
        swdy = 0.4
        swlen = 0.5

        if switch:
            tipy += 0.2

        if ring and ringswitch:
            sleevey += 0.2
            ringy -= 0.2

        sanchorx = 0 if extend_sleeve else -length - swidth

        if ring:
            if dots:
                if extend_sleeve:
                    self.segments.append(
                        SegmentCircle((0, -sleevey), radius, fill=fill, zorder=4)
                    )
                else:
                    self.segments.append(
                        SegmentCircle(
                            (-length - swidth, -sleevey), radius, fill=fill, zorder=4
                        )
                    )

            if extend_sleeve:
                self.segments.append(Segment([(0, -sleevey), (-length, -sleevey)]))

            self.segments.append(
                Segment(
                    [
                        (-length, 0),
                        (-length, sleeveheight),
                        (-length - swidth, sleeveheight),
                        (-length - swidth, 0),
                        (-length, 0),
                    ]
                )
            )
            self.anchors["sleeve"] = (sanchorx, -sleevey)

            if dots:
                self.segments.append(
                    SegmentCircle((0, ringy), radius, fill=fill, zorder=4)
                )
            self.segments.append(
                Segment(
                    [
                        (-radius, ringy),
                        (-length * 0.75, ringy),
                        (-length * ringlen - 2 * radius, ringy + 2 * radius),
                        (-length * ringlen - radius * 4, ringy),
                    ]
                )
            )
            self.anchors["ring"] = (0, ringy)

        else:
            if dots and extend_sleeve:
                self.segments.append(SegmentCircle((0, 0), radius, fill=fill, zorder=4))
            if extend_sleeve:
                self.segments.append(Segment([(-radius, 0), (-length + swidth, 0)]))
            self.segments.append(
                Segment(
                    [
                        (-length + swidth, 0),
                        (-length, 0),
                        (-length, sleeveheight),
                        (-length + swidth, sleeveheight),
                        (-length + swidth, 0),
                    ]
                )
            )
            self.anchors["sleeve"] = (sanchorx, 0)

        if dots:
            self.segments.append(SegmentCircle((0, tipy), radius, fill=fill, zorder=4))
        self.segments.append(
            Segment(
                [
                    (-radius, tipy),
                    (-length * 0.55, tipy),
                    (-length * tiplen - 2 * radius, tipy - 2 * radius),
                    (-length * tiplen - radius * 4, tipy),
                ]
            )
        )
        self.anchors["tip"] = (0, tipy)

        if switch:
            if dots:
                self.segments.append(
                    SegmentCircle((0, tipy - swdy), radius, fill=fill, zorder=4)
                )
            self.segments.append(Segment([(0, tipy - swdy), (-swlen, tipy - swdy)]))
            self.segments.append(
                Segment([(-swlen, tipy - swdy), (-swlen, tipy)], arrow="->")
            )
            self.anchors["tipswitch"] = (0, tipy - swdy)

        if ring and ringswitch:
            if dots:
                self.segments.append(
                    SegmentCircle((0, ringy + swdy), radius, fill=fill, zorder=4)
                )
            self.segments.append(Segment([(0, ringy + swdy), (-swlen, ringy + swdy)]))
            self.segments.append(
                Segment([(-swlen, ringy + swdy), (-swlen, ringy)], arrow="->")
            )
            self.anchors["ringswitch"] = (0, ringy + swdy)
