''' Vacuum tube '''

import math
from .elements import Element, gap
from ..segments import Segment, SegmentArc, SegmentText

tr_back = 2.5
tr_xlen = tr_back * math.sqrt(3)/2
tr_leadlen = tr_back/4

class Triode(Element):
    ''' Triode Vacuum Tube.

        Args:
            leads: Draw short leads on input/output
            pin_nums: Show pin numbers at each anchor
            half: Draw only half of the tube. "left" for left half, "right" for right half.

        Anchors:
            * g (grid)
            * k (cathode)
            * a (anode)
    '''
    def __init__(self, *d, leads: bool = False, pin_nums: dict = None, half: str = None, **kwargs):
        super().__init__(*d, **kwargs)

        x = 0 if not leads else tr_leadlen

        # Decide whether to draw a full circle, left half, or right half based on 'half' argument
        theta1, theta2 = (0, 360)  # Default to full circle
        if half == 'left':
            theta1, theta2 = (90, 270)
        elif half == 'right':
            theta1, theta2 = (270, 90)
            
        # Draw the triode as a circular or semicircular shape using SegmentArc
        self.segments.append(SegmentArc(center=(x+tr_xlen/2, 0), radius=tr_xlen/2, theta1=theta1, theta2=theta2))

        if leads:
            # Grid lead as a dotted line
            for i in range(-tr_back//2, tr_back//2, 2):
                self.segments.append(Segment([(0, i), (tr_leadlen, i)]))
            # Cathode lead
            self.segments.append(Segment([(0, -tr_back/2), (tr_leadlen, -tr_back/2)]))
            # Anode lead
            self.segments.append(Segment([(tr_leadlen+tr_xlen, tr_back/2), (tr_xlen + 2*tr_leadlen, tr_back/2)]))

        # Defining the anchor points
        self.anchors['g'] = (0, 0)  # Grid
        self.anchors['k'] = (0, -tr_back/2)  # Cathode
        self.anchors['a'] = (tr_xlen + 2*x, tr_back/2)  # Anode
        self.params['drop'] = (2*x+tr_xlen, 0)
        
        # Add pin numbers if provided
        if pin_nums is not None:
            for anchor, pin_num in pin_nums.items():
                if anchor in self.anchors:
                    # Place the text slightly offset from the anchor
                    text_position = (self.anchors[anchor][0] - 0.1, self.anchors[anchor][1] - 0.1)
                    self.segments.append(SegmentText(text_position, str(pin_num)))

class Half12AX7(Triode):
    ''' Half of a 12AX7 Triode. 

    Inherits from the triode class above, but shows correct pin numbers. Can specify left or right.
    
    '''

    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)

        if self.half == 'left' and self.pin_nums is None:
            self.pin_nums = {'g': 2, 'k': 3, 'a': 1}
            
        elif self.half == 'right' and self.pin_nums is None:
            self.pin_nums = {'g': 7, 'k': 8, 'a': 6}