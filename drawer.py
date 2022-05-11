from typing import Tuple, List, Union

Vector = Tuple[float]
Color = Tuple[float] | str
Polygon = List[Vector]

class BaseRenderer:

    scale: Vector
    centre: Vector
    dimensions: Vector
    
    def __init__(self) -> None:
        self.scale = (1,1)
        self.centre = (0,0)
        self.dimensions = (512,512)

    #helper that transforms a scaled point into image space
    def transformpoint(self, point: Vector)->Vector:
        res = (
            self.dimensions[0]*(0.5+(point[0]-self.centre[0])*self.scale[0]),
            self.dimensions[1]*(0.5+(point[1]-self.centre[1])*self.scale[1]),
        )
        return res

    #overridable function to draw a polygon
    def drawpoly(poly: Polygon, fill: Color | None, line: Color | None, width: float=1):
        raise NotImplementedError()

class SVGRenderer(BaseRenderer):
    def __init__(self) -> None:
        super().__init__(self)

class PixelRenderer(BaseRenderer):
    def __init__(self) -> None:
        super().__init__(self)

