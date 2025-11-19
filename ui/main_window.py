import os
import sys
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QFileDialog, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
from config import CONFIG_FILE, DEFAULT_SETTINGS
from config.settings_service import SettingsService
from i18n import LANGUAGES
from services import PDFService
from .control_panel import ControlPanel
from .preview_panel import PreviewPanel
from .styles import AppStyle, AppConstants


class LabelPrinterQt(QMainWindow):

    def __init__(self):
        super().__init__()
        self.image_path = ""
        self.preview_pixmap = None
        self.preview_generated = False
        self.pdf_service = PDFService()
        self.settings_service = SettingsService(CONFIG_FILE, DEFAULT_SETTINGS)
        
        # 设置保存防抖定时器
        self.settings_timer = QTimer()
        self.settings_timer.setSingleShot(True)
        self.settings_timer.timeout.connect(self.save_settings)
        
        # resize 防抖定时器
        self.resize_timer = QTimer()
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self._handle_resize)

        settings = self.load_settings()
        self.current_lang = settings['language']
        self.saved_rows = settings['rows']
        self.saved_cols = settings['cols']
        self.saved_margin = settings['margin']
        self.saved_spacing = settings['spacing']
        self.saved_orientation = settings['orientation']

        self.init_ui()

    def get_resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS  # type: ignore[attr-defined]
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def ensure_outputs_folder(self):
        outputs_dir = "outputs"
        if not os.path.exists(outputs_dir):
            os.makedirs(outputs_dir)
        return outputs_dir

    def load_settings(self):
        return self.settings_service.load()

    def save_settings(self):
        orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'
        settings = {
            'language': self.current_lang,
            'rows': self.rows_spin.value(),
            'cols': self.cols_spin.value(),
            'margin': self.margin_spin.value(),
            'spacing': self.spacing_spin.value(),
            'orientation': orientation
        }
        self.settings_service.save(settings)

    def save_settings_debounce(self):
        self.settings_timer.start(500)

    def validate_image_file(self):
        if not self.image_path:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('warning_no_image')
            )
            return False

        if not os.path.exists(self.image_path):
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_not_exist')
            )
            return False

        return True

    def generate_filename(self, extension):
        outputs_dir = self.ensure_outputs_folder()
        timestamp = datetime.now().strftime("%m%d%H%M")
        return os.path.join(outputs_dir, f"label{timestamp}.{extension}")

    def get_text(self, key):
        return LANGUAGES[self.current_lang].get(key, key)

    def init_ui(self):
        self.setWindowTitle(self.get_text('window_title'))
        self.setMinimumSize(1000, 538)
        self.resize(AppConstants.WINDOW_WIDTH, AppConstants.WINDOW_HEIGHT)

        icon_path = self.get_resource_path('label.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            fallback = self.get_resource_path('label.png')
            if os.path.exists(fallback):
                self.setWindowIcon(QIcon(fallback))

        AppStyle.apply(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.control_panel = ControlPanel(self)
        self.control_panel.setMaximumWidth(AppConstants.LEFT_PANEL_MAX_WIDTH)
        main_layout.addWidget(self.control_panel, stretch=2)

        self.preview_panel = PreviewPanel(self)
        main_layout.addWidget(self.preview_panel, stretch=3)

        self.center_window()

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def switch_language(self):
        self.current_lang = 'th' if self.current_lang == 'zh' else 'zh'
        self.save_settings()
        self.update_ui_texts()

    def update_ui_texts(self):
        self.setWindowTitle(self.get_text('window_title'))
        self.title_label.setText(self.get_text('main_title'))
        self.lang_btn.setText(self.get_text('lang_btn'))
        self.file_group.setTitle(self.get_text('file_group'))
        self.layout_group.setTitle(self.get_text('layout_group'))
        self.page_group.setTitle(self.get_text('page_group'))
        self.preview_group.setTitle(self.get_text('preview_group'))
        self.browse_btn.setText(self.get_text('browse_btn'))
        self.preview_btn.setText(self.get_text('preview_btn'))
        self.generate_btn.setText(self.get_text('generate_btn'))
        self.print_btn.setText(self.get_text('print_btn'))
        self.path_edit.setPlaceholderText(self.get_text('placeholder'))
        self.rows_label.setText(self.get_text('rows'))
        self.cols_label.setText(self.get_text('cols'))
        self.margin_label.setText(self.get_text('margin'))
        self.spacing_label.setText(self.get_text('spacing'))
        self.landscape_radio.setText(self.get_text('landscape'))
        self.portrait_radio.setText(self.get_text('portrait'))
        self.update_label_count()

        if not self.image_path:
            self.preview_label.setText(self.get_text('preview_hint_no_image'))
        elif not self.preview_generated:
            self.preview_label.setText(self.get_text('preview_hint_click'))

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.get_text('dialog_title'),
            "",
            self.get_text('dialog_filter')
        )

        if file_path:
            self.image_path = file_path
            self.path_edit.setText(file_path)
            self.preview_generated = False
            self.update_button_states()
            self.preview_label.clear()
            self.preview_label.setText(self.get_text('preview_hint_click'))

    def on_parameter_changed(self):
        if self.preview_generated:
            self.preview_generated = False
            self.update_button_states()
            self.preview_label.setText(self.get_text('preview_hint_params_changed'))

    def update_button_states(self):
        has_image = bool(self.image_path)
        self.preview_btn.setEnabled(has_image)
        self.generate_btn.setEnabled(has_image and self.preview_generated)
        self.print_btn.setEnabled(has_image and self.preview_generated)

    def generate_preview(self):
        if not self.image_path:
            return

        temp_pdf = "temp_preview.pdf"
        try:
            # 显示加载动画
            self.loading_overlay.set_message(self.get_text('preview_generating'))
            self.loading_overlay.show_loading()
            QApplication.processEvents()

            orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'

            self.pdf_service.tile_label_image_to_pdf(
                image_path=self.image_path,
                output_pdf=temp_pdf,
                rows=self.rows_spin.value(),
                cols=self.cols_spin.value(),
                margin_mm=self.margin_spin.value(),
                spacing_mm=self.spacing_spin.value(),
                orientation=orientation,
                error_label_size_msg=self.get_text('error_label_size')
            )

            pixmap = self.pdf_service.pdf_to_pixmap(temp_pdf, zoom=3)
            self.show_preview_image(pixmap)

            self.preview_generated = True
            self.update_button_states()

        except Exception as e:
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_preview').format(error=str(e))
            )
            self.preview_label.setText(self.get_text('preview_hint_click'))
        finally:
            # 隐藏加载动画
            self.loading_overlay.hide_loading()
            # 确保临时文件总是被清理
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)

    def resizeEvent(self, event):
        """窗口缩放事件，使用防抖优化性能"""
        super().resizeEvent(event)
        if self.preview_generated and self.preview_pixmap and not self.preview_pixmap.isNull():
            # 防抖：100ms后执行
            self.resize_timer.start(100)

    def _handle_resize(self):
        """处理窗口缩放后的预览图更新"""
        if self.preview_generated and self.preview_pixmap and not self.preview_pixmap.isNull():
            self.show_preview_image()

    def show_preview_image(self, pixmap=None):
        if pixmap and not pixmap.isNull():
            self.preview_pixmap = pixmap
        if self.preview_pixmap and not self.preview_pixmap.isNull():
            target_rect = self.preview_label.contentsRect()
            target_width = max(1, target_rect.width() - 20)
            target_height = max(1, target_rect.height() - 20)
            scaled_pixmap = self.preview_pixmap.scaled(
                target_width,
                target_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.preview_label.setPixmap(scaled_pixmap)
            self.preview_label.setText("")

    def update_label_count(self):
        count = self.rows_spin.value() * self.cols_spin.value()
        self.count_label.setText(self.get_text('count_label').format(count=count))

    def _generate_pdf_internal(self):
        """内部 PDF 生成逻辑，由 generate_pdf 和 generate_and_print_pdf 共用"""
        output_pdf = self.generate_filename("pdf")
        orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'

        self.pdf_service.tile_label_image_to_pdf(
            image_path=self.image_path,
            output_pdf=output_pdf,
            rows=self.rows_spin.value(),
            cols=self.cols_spin.value(),
            margin_mm=self.margin_spin.value(),
            spacing_mm=self.spacing_spin.value(),
            orientation=orientation,
            error_label_size_msg=self.get_text('error_label_size')
        )
        return output_pdf

    def generate_pdf(self):
        if not self.validate_image_file():
            return

        if not self.preview_generated:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('warning_no_preview')
            )
            return

        try:
            output_pdf = self._generate_pdf_internal()

            reply = QMessageBox.question(
                self,
                self.get_text('success_title'),
                self.get_text('success_message').format(
                    filename=output_pdf,
                    count=self.rows_spin.value() * self.cols_spin.value()
                ),
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                outputs_dir = self.ensure_outputs_folder()
                if sys.platform == 'win32':
                    os.startfile(os.path.abspath(outputs_dir))
                elif sys.platform == 'darwin':
                    os.system(f'open "{os.path.abspath(outputs_dir)}"')
                else:
                    os.system(f'xdg-open "{os.path.abspath(outputs_dir)}"')

        except Exception as e:
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_generate').format(error=str(e))
            )

    def generate_and_print_pdf(self):
        if not self.validate_image_file():
            return

        if not self.preview_generated:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('warning_no_preview')
            )
            return

        try:
            output_pdf = self._generate_pdf_internal()
            output_png = self.generate_filename("png")

            self.pdf_service.pdf_to_png(output_pdf, output_png, dpi=300)

            if sys.platform == 'win32':
                os.startfile(output_png, "print")
                QMessageBox.information(
                    self,
                    self.get_text('success_title'),
                    self.get_text('print_success').format(
                        filename=output_pdf,
                        count=self.rows_spin.value() * self.cols_spin.value()
                    )
                )
            else:
                QMessageBox.information(
                    self,
                    self.get_text('success_title'),
                    self.get_text('print_success').format(
                        filename=output_pdf,
                        count=self.rows_spin.value() * self.cols_spin.value()
                    )
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_print_failed').format(error=str(e))
            )
