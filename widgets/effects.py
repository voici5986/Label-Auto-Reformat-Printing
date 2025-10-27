from PyQt6.QtWidgets import QWidget, QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor


def add_shadow(widget: QWidget, blur_radius: int = 15, alpha: int = 30) -> None:
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(blur_radius)
    shadow.setColor(QColor(0, 0, 0, alpha))
    shadow.setOffset(0, 2)
    widget.setGraphicsEffect(shadow)
