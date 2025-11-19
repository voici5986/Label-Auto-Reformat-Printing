class AppConstants:
    """UI 布局常量"""
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600

    PREVIEW_WIDTH = 480
    PREVIEW_HEIGHT = 480
    PREVIEW_ASPECT_RATIO = 1 / 1

    BUTTON_HEIGHT = 40
    TITLE_BUTTON_HEIGHT = 45

    LEFT_PANEL_MAX_WIDTH = 420

    FONT_SIZE_NORMAL = 16
    FONT_SIZE_TITLE = 20


class AppStyle:
    STYLE_SHEET = """
        QMainWindow {
            background-color: #f5f6fa;
        }

        QGroupBox {
            background-color: white;
            border: none;
            border-radius: 5px;
            margin-top: 0px;
            padding-top: 25px;
            padding-left: 15px;
            padding-right: 10px;
            padding-bottom: 10px;
            font-size: 16px;
            font-weight: bold;
            color: #2c3e50;
        }

        QGroupBox::title {
            subcontrol-origin: padding;
            subcontrol-position: top left;
            left: 10px;
            top: 8px;
            padding: 0 5px;
        }

        QLabel {
            color: #2c3e50;
            font-size: 16px;
        }

        QLineEdit {
            background-color: #ecf0f1;
            border: none;
            border-radius: 5px;
            padding: 5px 5px;
            font-size: 16px;
            color: #2c3e50;
        }

        QLineEdit:focus {
            background-color: #e3e8eb;
        }

        QSpinBox {
            background-color: #ecf0f1;
            border: none;
            border-radius: 5px;
            padding: 3px 3px;
            font-size: 16px;
            color: #2c3e50;
            min-width: 80px;
        }

        QSpinBox:focus {
            background-color: #e3e8eb;
        }

        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #3498db;
            border: none;
            border-radius: 5px;
            width: 20px;
        }

        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #2980b9;
        }

        QSpinBox::up-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-bottom: 6px solid white;
            width: 0;
            height: 0;
        }

        QSpinBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid white;
            width: 0;
            height: 0;
        }

        QRadioButton {
            color: #2c3e50;
            font-size: 16px;
            spacing: 8px;
        }

        QRadioButton::indicator {
            width: 5px;
            height: 5px;
        }

        QRadioButton::indicator:unchecked {
            background-color: #ecf0f1;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
        }

        QRadioButton::indicator:checked {
            background-color: #3498db;
            border: 2px solid #3498db;
            border-radius: 5px;
        }

        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 5px 5px;
            font-size: 16px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #2980b9;
        }

        QPushButton:pressed {
            background-color: #21618c;
        }

        QPushButton#generateBtn {
            background-color: #27ae60;
            font-size: 16px;
            padding: 5px 5px;
        }

        QPushButton#generateBtn:hover {
            background-color: #229954;
        }

        QPushButton#generateBtn:pressed {
            background-color: #1e8449;
        }

        QPushButton#printBtn {
            background-color: #3498db;
            font-size: 16px;
            padding: 5px 5px;
        }

        QPushButton#printBtn:hover {
            background-color: #2980b9;
        }

        QPushButton#printBtn:pressed {
            background-color: #21618c;
        }

        QPushButton#previewBtn {
            background-color: #9b59b6;
            font-size: 16px;
            padding: 5px 5px;
        }

        QPushButton#previewBtn:hover {
            background-color: #8e44ad;
        }

        QPushButton#previewBtn:pressed {
            background-color: #7d3c98;
        }

        QPushButton#previewBtn:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }

        QPushButton#langBtn {
            background-color: #e67e22;
            font-size: 16px;
            padding: 5px 5px;
            min-width: 60px;
        }

        QPushButton#langBtn:hover {
            background-color: #d35400;
        }

        QPushButton#langBtn:pressed {
            background-color: #ba4a00;
        }

        #titleLabel {
            background-color: #3498db;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 0px;
            border-radius: 5px;
        }

        #countLabel {
            color: #3498db;
            font-size: 16px;
            font-weight: bold;
            padding: 2px;
        }

        #previewLabel {
            background-color: #ecf0f1;
            border: 2px dashed #bdc3c7;
            border-radius: 5px;
        }
    """

    @classmethod
    def apply(cls, widget) -> None:
        widget.setStyleSheet(cls.STYLE_SHEET)
