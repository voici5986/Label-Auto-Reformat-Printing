from PyQt6.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from widgets import AspectRatioLabel, add_shadow
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
        self.main.preview_group = self
        self.main.preview_label = self.preview_label
