from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPainter, QPen, QColor


class LoadingSpinner(QWidget):
    """加载动画组件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._rotate)
        self.setFixedSize(40, 40)
    
    def _rotate(self):
        """旋转动画"""
        self.angle = (self.angle + 30) % 360
        self.update()
    
    def start(self):
        """启动动画"""
        self.timer.start(100)  # 每100ms旋转一次
    
    def stop(self):
        """停止动画"""
        self.timer.stop()
    
    def paintEvent(self, event):
        """绘制旋转的加载指示器"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # 设置画笔
        pen = QPen(QColor("#3498db"))
        pen.setWidth(4)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        # 绘制圆弧
        painter.translate(20, 20)
        painter.rotate(self.angle)
        painter.drawArc(-15, -15, 30, 30, 0, 270 * 16)


class LoadingOverlay(QWidget):
    """加载遮罩层组件"""
    
    def __init__(self, parent=None, message="正在加载..."):
        super().__init__(parent)
        self._message = message
        self._init_ui()
        self.hide()
    
    def _init_ui(self):
        """初始化UI"""
        # 设置半透明背景
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(236, 240, 241, 230);
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 加载动画
        self.spinner = LoadingSpinner(self)
        layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 加载文字
        self.label = QLabel(self._message, self)
        self.label.setStyleSheet("""
            QLabel {
                color: #2c3e50;
                font-size: 16px;
                font-weight: bold;
                background: transparent;
            }
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
    
    def set_message(self, message: str):
        """设置加载文字"""
        self._message = message
        self.label.setText(message)
    
    def show_loading(self):
        """显示加载动画"""
        self.show()
        self.raise_()  # 确保在最上层
        self.spinner.start()
    
    def hide_loading(self):
        """隐藏加载动画"""
        self.spinner.stop()
        self.hide()
