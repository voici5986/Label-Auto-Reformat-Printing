from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QSize


class AspectRatioLabel(QLabel):
    """保持固定宽高比的 QLabel."""

    def __init__(self, aspect_ratio=1.0, parent=None):
        super().__init__(parent)
        self._aspect_ratio = aspect_ratio

    def set_aspect_ratio(self, ratio: float) -> None:
        self._aspect_ratio = ratio
        self.updateGeometry()

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width: int) -> int:
        if self._aspect_ratio == 0:
            return super().heightForWidth(width)
        return int(width / self._aspect_ratio)

    def sizeHint(self) -> QSize:
        hint = super().sizeHint()
        return QSize(hint.width(), self.heightForWidth(hint.width()))

    def minimumSizeHint(self) -> QSize:
        hint = super().minimumSizeHint()
        return QSize(hint.width(), self.heightForWidth(hint.width()))
