from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from widgets import AspectRatioLabel, add_shadow, LoadingOverlay
from .styles import AppConstants


class PreviewPanel(QGroupBox):
    def __init__(self, main_window):
        super().__init__(main_window.get_text('preview_group'))
        self.main = main_window
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.preview_label = AspectRatioLabel(AppConstants.PREVIEW_ASPECT_RATIO)
        self.preview_label.setObjectName("previewLabel")
        self.preview_label.setMinimumWidth(400)
        self.preview_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setText(self.main.get_text('preview_hint_no_image'))
        self.preview_label.setStyleSheet("""
            QLabel {
                color: #95a5a6;
                font-size: 16px;
            }
        """)

        layout.addWidget(self.preview_label)
        layout.addStretch()

        self.setLayout(layout)
        add_shadow(self)
        
        # 添加加载遮罩层
        self.loading_overlay = LoadingOverlay(self.preview_label)
        
        self.main.preview_group = self
        self.main.preview_label = self.preview_label
        self.main.loading_overlay = self.loading_overlay
    
    def resizeEvent(self, event):
        """调整遮罩层大小以覆盖预览区域"""
        super().resizeEvent(event)
        if hasattr(self, 'loading_overlay'):
            self.loading_overlay.setGeometry(self.preview_label.geometry())
