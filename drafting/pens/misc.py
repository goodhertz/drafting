from fontTools.pens.filterPen import ContourFilterPen
from fontTools.pens.recordingPen import RecordingPen


class ExplodingPen(ContourFilterPen):
    def __init__(self, outPen):
        self.pens = []
        super().__init__(outPen)

    def filterContour(self, contour):
        self.pens.append(contour)
        return contour