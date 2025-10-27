from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGroupBox,
    QLineEdit, QSpinBox, QRadioButton, QButtonGroup
)
from PyQt6.QtCore import Qt
from widgets import add_shadow


class ControlPanel(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main = main_window
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title_layout = QHBoxLayout()

        self.title_label = QLabel(self.main.get_text('main_title'))
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFixedHeight(self.main.TITLE_BUTTON_HEIGHT)
        add_shadow(self.title_label)
        title_layout.addWidget(self.title_label)

        self.lang_btn = QPushButton(self.main.get_text('lang_btn'))
        self.lang_btn.setObjectName("langBtn")
        self.lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lang_btn.clicked.connect(self.main.switch_language)
        self.lang_btn.setFixedSize(80, self.main.TITLE_BUTTON_HEIGHT)
        add_shadow(self.lang_btn)
        title_layout.addWidget(self.lang_btn)

        layout.addLayout(title_layout)

        self.file_group = self._create_file_group()
        add_shadow(self.file_group)
        layout.addWidget(self.file_group)

        self.layout_group = self._create_layout_group()
        add_shadow(self.layout_group)
        layout.addWidget(self.layout_group)

        self.page_group = self._create_page_group()
        add_shadow(self.page_group)
        layout.addWidget(self.page_group)

        self.preview_btn = QPushButton(self.main.get_text('preview_btn'))
        self.preview_btn.setObjectName("previewBtn")
        self.preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.preview_btn.clicked.connect(self.main.generate_preview)
        self.preview_btn.setEnabled(False)
        self.preview_btn.setFixedHeight(self.main.BUTTON_HEIGHT)
        add_shadow(self.preview_btn)
        layout.addWidget(self.preview_btn)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.generate_btn = QPushButton(self.main.get_text('generate_btn'))
        self.generate_btn.setObjectName("generateBtn")
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_btn.clicked.connect(self.main.generate_pdf)
        self.generate_btn.setFixedHeight(self.main.BUTTON_HEIGHT)
        add_shadow(self.generate_btn)
        button_layout.addWidget(self.generate_btn)

        self.print_btn = QPushButton(self.main.get_text('print_btn'))
        self.print_btn.setObjectName("printBtn")
        self.print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.print_btn.clicked.connect(self.main.generate_and_print_pdf)
        self.print_btn.setFixedHeight(self.main.BUTTON_HEIGHT)
        add_shadow(self.print_btn)
        button_layout.addWidget(self.print_btn)

        layout.addLayout(button_layout)
        layout.addStretch()

        self._register_main_attributes()

    def _create_file_group(self):
        group = QGroupBox(self.main.get_text('file_group'))
        layout = QVBoxLayout()
        layout.setSpacing(10)

        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText(self.main.get_text('placeholder'))
        self.path_edit.setReadOnly(True)
        path_layout.addWidget(self.path_edit)

        self.browse_btn = QPushButton(self.main.get_text('browse_btn'))
        self.browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_btn.clicked.connect(self.main.browse_image)
        self.browse_btn.setFixedWidth(60)
        path_layout.addWidget(self.browse_btn)

        layout.addLayout(path_layout)
        group.setLayout(layout)
        return group

    def _create_layout_group(self):
        group = QGroupBox(self.main.get_text('layout_group'))
        layout = QVBoxLayout()
        layout.setSpacing(15)

        grid_layout = QHBoxLayout()

        self.rows_label = QLabel(self.main.get_text('rows'))
        grid_layout.addWidget(self.rows_label)
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 10)
        self.rows_spin.setValue(self.main.saved_rows)
        self.rows_spin.valueChanged.connect(self.main.update_label_count)
        self.rows_spin.valueChanged.connect(self.main.on_parameter_changed)
        self.rows_spin.valueChanged.connect(self.main.save_settings_debounce)
        grid_layout.addWidget(self.rows_spin)

        grid_layout.addSpacing(20)

        self.cols_label = QLabel(self.main.get_text('cols'))
        grid_layout.addWidget(self.cols_label)
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 10)
        self.cols_spin.setValue(self.main.saved_cols)
        self.cols_spin.valueChanged.connect(self.main.update_label_count)
        self.cols_spin.valueChanged.connect(self.main.on_parameter_changed)
        self.cols_spin.valueChanged.connect(self.main.save_settings_debounce)
        grid_layout.addWidget(self.cols_spin)

        grid_layout.addStretch()
        layout.addLayout(grid_layout)

        spacing_layout = QHBoxLayout()

        self.margin_label = QLabel(self.main.get_text('margin'))
        spacing_layout.addWidget(self.margin_label)
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(0, 30)
        self.margin_spin.setValue(self.main.saved_margin)
        self.margin_spin.setSuffix(" mm")
        self.margin_spin.valueChanged.connect(self.main.on_parameter_changed)
        self.margin_spin.valueChanged.connect(self.main.save_settings_debounce)
        spacing_layout.addWidget(self.margin_spin)

        spacing_layout.addSpacing(20)

        self.spacing_label = QLabel(self.main.get_text('spacing'))
        spacing_layout.addWidget(self.spacing_label)
        self.spacing_spin = QSpinBox()
        self.spacing_spin.setRange(0, 20)
        self.spacing_spin.setValue(self.main.saved_spacing)
        self.spacing_spin.setSuffix(" mm")
        self.spacing_spin.valueChanged.connect(self.main.on_parameter_changed)
        self.spacing_spin.valueChanged.connect(self.main.save_settings_debounce)
        spacing_layout.addWidget(self.spacing_spin)

        spacing_layout.addStretch()
        layout.addLayout(spacing_layout)

        group.setLayout(layout)
        return group

    def _create_page_group(self):
        group = QGroupBox(self.main.get_text('page_group'))
        layout = QVBoxLayout()
        layout.setSpacing(15)

        orientation_layout = QHBoxLayout()

        self.orientation_group = QButtonGroup()

        self.landscape_radio = QRadioButton(self.main.get_text('landscape'))
        self.landscape_radio.setChecked(self.main.saved_orientation == 'landscape')
        self.landscape_radio.toggled.connect(self.main.on_parameter_changed)
        self.landscape_radio.toggled.connect(self.main.save_settings_debounce)
        self.orientation_group.addButton(self.landscape_radio, 0)
        orientation_layout.addWidget(self.landscape_radio)

        self.portrait_radio = QRadioButton(self.main.get_text('portrait'))
        self.portrait_radio.setChecked(self.main.saved_orientation == 'portrait')
        self.portrait_radio.toggled.connect(self.main.on_parameter_changed)
        self.portrait_radio.toggled.connect(self.main.save_settings_debounce)
        self.orientation_group.addButton(self.portrait_radio, 1)
        orientation_layout.addWidget(self.portrait_radio)

        orientation_layout.addStretch()
        layout.addLayout(orientation_layout)

        count = self.rows_spin.value() * self.cols_spin.value()
        self.count_label = QLabel(self.main.get_text('count_label').format(count=count))
        self.count_label.setObjectName("countLabel")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.count_label)

        group.setLayout(layout)
        return group

    def _register_main_attributes(self):
        attrs = [
            'title_label', 'lang_btn', 'file_group', 'layout_group', 'page_group',
            'preview_btn', 'generate_btn', 'print_btn', 'path_edit', 'browse_btn',
            'rows_spin', 'cols_spin', 'margin_spin', 'spacing_spin', 'rows_label',
            'cols_label', 'margin_label', 'spacing_label', 'landscape_radio',
            'portrait_radio', 'orientation_group', 'count_label'
        ]
        for name in attrs:
            setattr(self.main, name, getattr(self, name))
