#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签打印工具 - PyQt6版本
现代化Material Design界面，支持文件选择、参数调整、时间戳命名、多语言
"""

import sys
import os
import json
import io
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSpinBox, QRadioButton, QButtonGroup,
    QFileDialog, QMessageBox, QGroupBox, QLineEdit, QGraphicsDropShadowEffect,
    QSplashScreen
)
from PyQt6.QtCore import Qt, QTimer, QStandardPaths
from PyQt6.QtGui import QPixmap, QFont, QColor, QIcon, QPainter
from PyQt6.QtPrintSupport import QPrinterInfo
from PIL import Image
import fitz  # PyMuPDF - 用于PDF转图片和PDF转PNG

# reportlab 相关导入已移至 tile_label_image_to_pdf 函数内部（延迟导入优化）


# 语言字典
LANGUAGES = {
    'zh': {
        'window_title': '标签打印排版工具',
        'main_title': '🏷️  标签批量打印排版工具',
        'file_group': '📁 选择标签图片',
        'layout_group': '📐 排列设置',
        'page_group': '📄 页面设置',
        'preview_group': '👁️ PDF预览',
        'browse_btn': '浏览',
        'preview_btn': '🔄 生成预览',
        'generate_btn': '📄 生成 PDF',
        'print_btn': '🖨️ 生成并打印',
        'lang_btn': 'ภาษาไทย',  # 显示"泰语"让用户知道可以切换到泰语
        'placeholder': '请选择图片文件...',
        'preview_hint_no_image': '请选择标签图片',
        'preview_hint_click': '请点击"生成预览"查看PDF效果',
        'preview_hint_params_changed': '⚠️ 参数已改变，请重新生成预览',
        'preview_generating': '⏳ 正在生成预览...',
        'rows': '行数:',
        'cols': '列数:',
        'margin': '边距:',
        'spacing': '间距:',
        'landscape': '横向 (297×210mm)',
        'portrait': '竖向 (210×297mm)',
        'count_label': '预计生成: {count} 个标签',
        'dialog_title': '选择标签图片',
        'dialog_filter': '图片文件 (*.png *.jpg *.jpeg);;PNG文件 (*.png);;JPEG文件 (*.jpg *.jpeg);;所有文件 (*.*)',
        'warning_title': '提示',
        'warning_no_image': '请先选择标签图片！',
        'warning_no_preview': '请先生成预览再进行此操作！',
        'error_title': '错误',
        'error_not_exist': '选择的图片文件不存在！',
        'error_load_preview': '无法加载图片预览:\n{error}',
        'error_generate': '生成PDF时出错:\n{error}',
        'error_preview': '生成预览时出错:\n{error}',
        'error_invalid_params': '当前排版参数导致标签尺寸为负，请调整行数、列数、边距或间距设置！',
        'error_no_printer': '未检测到可用的打印机！\n\n请确保已安装打印机驱动程序。',
        'error_print_cancelled': '打印已取消',
        'error_print_failed': '打印失败:\n{error}',
        'preparing_print': '⏳ 正在准备打印...',
        'print_ready': '✅ 打印准备完成！\n\n请在打印对话框中选择打印机并确认打印。',
        'success_title': '成功',
        'success_message': 'PDF已生成！\n\n文件名: {filename}\n标签数: {count} 个\n\n是否打开文件所在位置？',
        'print_success': 'PDF已生成并发送到打印机！\n\n文件名: {filename}\n标签数: {count} 个',
        'print_not_supported': '当前系统暂不支持直接打印，请先导出 PDF 后手动打印。'
    },
    'th': {
        'window_title': 'เครื่องมือพิมพ์ฉลาก',
        'main_title': '🏷️  เครื่องมือพิมพ์ฉลากจำนวนมาก',
        'file_group': '📁 เลือกรูปภาพฉลาก',
        'layout_group': '📐 การตั้งค่าการจัดเรียง',
        'page_group': '📄 การตั้งค่าหน้ากระดาษ',
        'preview_group': '👁️ ดูตัวอย่าง PDF',
        'browse_btn': 'เรียกดู',
        'preview_btn': '🔄 สร้างตัวอย่าง',
        'generate_btn': '📄 สร้าง PDF',
        'print_btn': '🖨️ สร้างและพิมพ์',
        'lang_btn': '中文',  # 显示"中文"让用户知道可以切换到中文
        'placeholder': 'กรุณาเลือกไฟล์รูปภาพ...',
        'preview_hint_no_image': 'กรุณาเลือกรูปภาพฉลาก',
        'preview_hint_click': 'กรุณาคลิก สร้างตัวอย่าง เพื่อดูผล PDF',
        'preview_hint_params_changed': '⚠️ พารามิเตอร์เปลี่ยนแปลง กรุณาสร้างตัวอย่างใหม่',
        'preview_generating': '⏳ กำลังสร้างตัวอย่าง...',
        'rows': 'แถว:',
        'cols': 'คอลัมน์:',
        'margin': 'ระยะขอบ:',
        'spacing': 'ระยะห่าง:',
        'landscape': 'แนวนอน (297×210mm)',
        'portrait': 'แนวตั้ง (210×297mm)',
        'count_label': 'คาดว่าจะสร้าง: {count} ฉลาก',
        'dialog_title': 'เลือกรูปภาพฉลาก',
        'dialog_filter': 'ไฟล์รูปภาพ (*.png *.jpg *.jpeg);;ไฟล์ PNG (*.png);;ไฟล์ JPEG (*.jpg *.jpeg);;ไฟล์ทั้งหมด (*.*)',
        'warning_title': 'แจ้งเตือน',
        'warning_no_image': 'กรุณาเลือกรูปภาพฉลากก่อน！',
        'warning_no_preview': 'กรุณาสร้างตัวอย่างก่อนดำเนินการนี้！',
        'error_title': 'ข้อผิดพลาด',
        'error_not_exist': 'ไฟล์รูปภาพที่เลือกไม่มีอยู่！',
        'error_load_preview': 'ไม่สามารถโหลดตัวอย่างรูปภาพ:\n{error}',
        'error_generate': 'เกิดข้อผิดพลาดในการสร้าง PDF:\n{error}',
        'error_preview': 'เกิดข้อผิดพลาดในการสร้างตัวอย่าง:\n{error}',
        'error_invalid_params': 'การตั้งค่าปัจจุบันทำให้ขนาดฉลากติดลบ โปรดปรับแถว คอลัมน์ ระยะขอบ หรือระยะห่าง',
        'error_no_printer': 'ไม่พบเครื่องพิมพ์ที่ใช้งานได้！\n\nกรุณาตรวจสอบว่าได้ติดตั้งไดรเวอร์เครื่องพิมพ์แล้ว',
        'error_print_cancelled': 'ยกเลิกการพิมพ์',
        'error_print_failed': 'การพิมพ์ล้มเหลว:\n{error}',
        'preparing_print': '⏳ กำลังเตรียมการพิมพ์...',
        'print_ready': '✅ เตรียมการพิมพ์เรียบร้อยแล้ว！\n\nกรุณาเลือกเครื่องพิมพ์และยืนยันการพิมพ์ในกล่องโต้ตอบ',
        'success_title': 'สำเร็จ',
        'success_message': 'สร้าง PDF เรียบร้อยแล้ว！\n\nชื่อไฟล์: {filename}\nจำนวนฉลาก: {count} ฉลาก\n\nต้องการเปิดตำแหน่งไฟล์หรือไม่？',
        'print_success': 'สร้าง PDF และส่งไปยังเครื่องพิมพ์เรียบร้อยแล้ว！\n\nชื่อไฟล์: {filename}\nจำนวนฉลาก: {count} ฉลาก',
        'print_not_supported': 'ระบบปัจจุบันไม่รองรับการพิมพ์โดยตรง โปรดส่งออก PDF แล้วพิมพ์ด้วยตนเอง'
    }
}


class LabelPrinterQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_path = ""
        self.preview_pixmap = None
        self.preview_generated = False  # 预览生成状态标志
        self.is_windows = sys.platform.startswith('win')
        self.status_label = None
        self._status_message_key = None
        
        # 加载所有设置
        settings = self.load_settings()
        self.current_lang = settings['language']
        self.saved_rows = settings['rows']
        self.saved_cols = settings['cols']
        self.saved_margin = settings['margin']
        self.saved_spacing = settings['spacing']
        self.saved_orientation = settings['orientation']
        
        self.init_ui()
        self.update_button_states()
        
    def get_resource_path(self, relative_path):
        """获取资源文件的绝对路径(支持PyInstaller打包)"""
        try:
            # PyInstaller创建临时文件夹,将路径存储在_MEIPASS中
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)
    
    def ensure_outputs_folder(self):
        """确保输出目录存在,如果不可写则回退到当前目录"""
        documents_path = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
        preferred_dir = None
        if documents_path:
            preferred_dir = os.path.join(documents_path, "LabelPrinterOutputs")
        outputs_dir = preferred_dir or os.path.join(os.path.abspath("."), "outputs")
        try:
            os.makedirs(outputs_dir, exist_ok=True)
        except OSError:
            fallback_dir = os.path.join(os.path.abspath("."), "outputs")
            if outputs_dir != fallback_dir:
                outputs_dir = fallback_dir
                os.makedirs(outputs_dir, exist_ok=True)
            else:
                raise
        return outputs_dir
    
    def load_settings(self):
        """加载所有保存的设置"""
        config_file = 'settings.json'
        default_settings = {
            'language': 'th',
            'rows': 3,
            'cols': 3,
            'margin': 6,
            'spacing': 8,
            'orientation': 'landscape'
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    saved_settings = json.load(f)
                    # 合并默认设置和保存的设置,确保所有键都存在
                    return {**default_settings, **saved_settings}
        except:
            pass
        
        return default_settings
    
    def save_settings(self):
        """保存所有设置"""
        config_file = 'settings.json'
        
        # 获取当前方向设置
        orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'
        
        settings = {
            'language': self.current_lang,
            'rows': self.rows_spin.value(),
            'cols': self.cols_spin.value(),
            'margin': self.margin_spin.value(),
            'spacing': self.spacing_spin.value(),
            'orientation': orientation
        }
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except:
            pass
    
    def get_text(self, key):
        """获取当前语言的文本"""
        return LANGUAGES[self.current_lang].get(key, key)
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle(self.get_text('window_title'))
        self.setFixedSize(900, 600)
        
        # 设置窗口图标
        icon_path = self.get_resource_path('label.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            icon_path = self.get_resource_path('label.png')
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
        
        # 设置应用样式
        self.set_stylesheet()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 左侧控制面板
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, stretch=3)
        
        # 右侧预览面板
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, stretch=2)
        
        # 居中显示窗口
        self.center_window()
        
    def set_stylesheet(self):
        """设置现代化样式表"""
        self.setStyleSheet("""
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
            #statusLabel {
                color: #7f8c8d;
                font-size: 14px;
                padding: 4px;
            }
        """)
        
    def create_left_panel(self):
        """创建左侧控制面板"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        
        # 标题栏（包含标题和语言切换按钮）
        title_layout = QHBoxLayout()
        
        # 标题
        self.title_label = QLabel(self.get_text('main_title'))
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setFixedHeight(45)
        self.add_shadow(self.title_label)
        title_layout.addWidget(self.title_label)
        
        # 语言切换按钮
        self.lang_btn = QPushButton(self.get_text('lang_btn'))
        self.lang_btn.setObjectName("langBtn")
        self.lang_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.lang_btn.clicked.connect(self.switch_language)
        self.lang_btn.setFixedSize(80, 45)
        self.add_shadow(self.lang_btn)
        title_layout.addWidget(self.lang_btn)
        
        layout.addLayout(title_layout)
        
        # 文件选择组
        self.file_group = self.create_file_selection_group()
        self.add_shadow(self.file_group)
        layout.addWidget(self.file_group)
        
        # 排列设置组
        self.layout_group = self.create_layout_settings_group()
        self.add_shadow(self.layout_group)
        layout.addWidget(self.layout_group)
        
        # 页面设置组
        self.page_group = self.create_page_settings_group()
        self.add_shadow(self.page_group)
        layout.addWidget(self.page_group)
        
        # 生成预览按钮（单独一行）
        self.preview_btn = QPushButton(self.get_text('preview_btn'))
        self.preview_btn.setObjectName("previewBtn")
        self.preview_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.preview_btn.clicked.connect(self.generate_preview)
        self.preview_btn.setEnabled(False)  # 初始禁用
        self.preview_btn.setFixedHeight(40)
        self.add_shadow(self.preview_btn)
        layout.addWidget(self.preview_btn)
        
        # 按钮布局（生成PDF和打印按钮并排）
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # 生成PDF按钮
        self.generate_btn = QPushButton(self.get_text('generate_btn'))
        self.generate_btn.setObjectName("generateBtn")
        self.generate_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.generate_btn.clicked.connect(self.generate_pdf)
        self.generate_btn.setFixedHeight(40)
        self.add_shadow(self.generate_btn)
        button_layout.addWidget(self.generate_btn)
        
        # 生成并打印按钮
        self.print_btn = QPushButton(self.get_text('print_btn'))
        self.print_btn.setObjectName("printBtn")
        self.print_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.print_btn.clicked.connect(self.generate_and_print_pdf)
        self.print_btn.setFixedHeight(40)
        self.add_shadow(self.print_btn)
        button_layout.addWidget(self.print_btn)
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        return panel
        
    def create_file_selection_group(self):
        """创建文件选择组"""
        group = QGroupBox(self.get_text('file_group'))
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 文件路径显示
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText(self.get_text('placeholder'))
        self.path_edit.setReadOnly(True)
        path_layout.addWidget(self.path_edit)
        
        # 浏览按钮
        self.browse_btn = QPushButton(self.get_text('browse_btn'))
        self.browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.browse_btn.clicked.connect(self.browse_image)
        self.browse_btn.setFixedWidth(60)
        path_layout.addWidget(self.browse_btn)
        
        layout.addLayout(path_layout)
        group.setLayout(layout)
        return group
        
    def create_layout_settings_group(self):
        """创建排列设置组"""
        group = QGroupBox(self.get_text('layout_group'))
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 行列数设置
        grid_layout = QHBoxLayout()
        
        # 行数
        self.rows_label = QLabel(self.get_text('rows'))
        grid_layout.addWidget(self.rows_label)
        self.rows_spin = QSpinBox()
        self.rows_spin.setRange(1, 10)
        self.rows_spin.setValue(self.saved_rows)  # 使用保存的值
        self.rows_spin.valueChanged.connect(self.update_label_count)
        self.rows_spin.valueChanged.connect(self.on_parameter_changed)
        self.rows_spin.valueChanged.connect(self.save_settings)  # 自动保存
        grid_layout.addWidget(self.rows_spin)
        
        grid_layout.addSpacing(20)
        
        # 列数
        self.cols_label = QLabel(self.get_text('cols'))
        grid_layout.addWidget(self.cols_label)
        self.cols_spin = QSpinBox()
        self.cols_spin.setRange(1, 10)
        self.cols_spin.setValue(self.saved_cols)  # 使用保存的值
        self.cols_spin.valueChanged.connect(self.update_label_count)
        self.cols_spin.valueChanged.connect(self.on_parameter_changed)
        self.cols_spin.valueChanged.connect(self.save_settings)  # 自动保存
        grid_layout.addWidget(self.cols_spin)
        
        grid_layout.addStretch()
        layout.addLayout(grid_layout)
        
        # 边距和间距设置
        spacing_layout = QHBoxLayout()
        
        # 边距
        self.margin_label = QLabel(self.get_text('margin'))
        spacing_layout.addWidget(self.margin_label)
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(0, 30)
        self.margin_spin.setValue(self.saved_margin)  # 使用保存的值
        self.margin_spin.setSuffix(" mm")
        self.margin_spin.valueChanged.connect(self.on_parameter_changed)
        self.margin_spin.valueChanged.connect(self.save_settings)  # 自动保存
        spacing_layout.addWidget(self.margin_spin)
        
        spacing_layout.addSpacing(20)
        
        # 间距
        self.spacing_label = QLabel(self.get_text('spacing'))
        spacing_layout.addWidget(self.spacing_label)
        self.spacing_spin = QSpinBox()
        self.spacing_spin.setRange(0, 20)
        self.spacing_spin.setValue(self.saved_spacing)  # 使用保存的值
        self.spacing_spin.setSuffix(" mm")
        self.spacing_spin.valueChanged.connect(self.on_parameter_changed)
        self.spacing_spin.valueChanged.connect(self.save_settings)  # 自动保存
        spacing_layout.addWidget(self.spacing_spin)
        
        spacing_layout.addStretch()
        layout.addLayout(spacing_layout)
        
        group.setLayout(layout)
        return group
        
    def create_page_settings_group(self):
        """创建页面设置组"""
        group = QGroupBox(self.get_text('page_group'))
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 页面方向
        orientation_layout = QHBoxLayout()
        
        self.orientation_group = QButtonGroup()
        
        self.landscape_radio = QRadioButton(self.get_text('landscape'))
        self.landscape_radio.setChecked(self.saved_orientation == 'landscape')  # 使用保存的值
        self.landscape_radio.toggled.connect(self.on_parameter_changed)
        self.landscape_radio.toggled.connect(self.save_settings)  # 自动保存
        self.orientation_group.addButton(self.landscape_radio, 0)
        orientation_layout.addWidget(self.landscape_radio)
        
        self.portrait_radio = QRadioButton(self.get_text('portrait'))
        self.portrait_radio.setChecked(self.saved_orientation == 'portrait')  # 使用保存的值
        self.portrait_radio.toggled.connect(self.on_parameter_changed)
        self.portrait_radio.toggled.connect(self.save_settings)  # 自动保存
        self.orientation_group.addButton(self.portrait_radio, 1)
        orientation_layout.addWidget(self.portrait_radio)
        
        orientation_layout.addStretch()
        layout.addLayout(orientation_layout)
        
        # 标签数量显示
        count = self.rows_spin.value() * self.cols_spin.value() if hasattr(self, 'rows_spin') else 12
        self.count_label = QLabel(self.get_text('count_label').format(count=count))
        self.count_label.setObjectName("countLabel")
        self.count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.count_label)
        
        group.setLayout(layout)
        return group
        
    def create_right_panel(self):
        """创建右侧预览面板"""
        self.preview_group = QGroupBox(self.get_text('preview_group'))
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # 预览标签
        self.preview_label = QLabel()
        self.preview_label.setObjectName("previewLabel")
        self.preview_label.setFixedSize(400, 505)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setText(self.get_text('preview_hint_no_image'))
        self.preview_label.setStyleSheet("""
            QLabel {
                color: #95a5a6;
                font-size: 16px;
            }
        """)
        
        layout.addWidget(self.preview_label)
        self.status_label = QLabel()
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        self.set_status_message(None)
        layout.addStretch()  # 添加弹性空间,让预览区域居中
        
        self.preview_group.setLayout(layout)
        self.add_shadow(self.preview_group)
        return self.preview_group
        
    def add_shadow(self, widget):
        """为控件添加阴影效果"""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        widget.setGraphicsEffect(shadow)
    
    def switch_language(self):
        """切换语言"""
        # 切换到另一种语言
        self.current_lang = 'th' if self.current_lang == 'zh' else 'zh'
        
        # 保存所有设置(包括语言)
        self.save_settings()
        
        # 更新所有界面文本
        self.update_ui_texts()
    
    def update_ui_texts(self):
        """更新所有界面文本"""
        # 更新窗口标题
        self.setWindowTitle(self.get_text('window_title'))
        
        # 更新主标题
        self.title_label.setText(self.get_text('main_title'))
        
        # 更新语言按钮
        self.lang_btn.setText(self.get_text('lang_btn'))
        
        # 更新GroupBox标题
        self.file_group.setTitle(self.get_text('file_group'))
        self.layout_group.setTitle(self.get_text('layout_group'))
        self.page_group.setTitle(self.get_text('page_group'))
        self.preview_group.setTitle(self.get_text('preview_group'))
        
        # 更新按钮文本
        self.browse_btn.setText(self.get_text('browse_btn'))
        self.preview_btn.setText(self.get_text('preview_btn'))
        self.generate_btn.setText(self.get_text('generate_btn'))
        self.print_btn.setText(self.get_text('print_btn'))
        if not self.is_windows:
            self.print_btn.setToolTip(self.get_text('print_not_supported'))
        else:
            self.print_btn.setToolTip("")
        
        # 更新占位符
        self.path_edit.setPlaceholderText(self.get_text('placeholder'))
        
        # 更新标签文本
        self.rows_label.setText(self.get_text('rows'))
        self.cols_label.setText(self.get_text('cols'))
        self.margin_label.setText(self.get_text('margin'))
        self.spacing_label.setText(self.get_text('spacing'))
        
        # 更新单选按钮
        self.landscape_radio.setText(self.get_text('landscape'))
        self.portrait_radio.setText(self.get_text('portrait'))
        
        # 更新标签数量
        self.update_label_count()
        
        # 更新预览文本
        if not self.image_path:
            self.preview_label.setText(self.get_text('preview_hint_no_image'))
        elif not self.preview_generated:
            self.preview_label.setText(self.get_text('preview_hint_click'))
        
        self.set_status_message(self._status_message_key)
        self.update_button_states()
        
    def browse_image(self):
        """浏览并选择图片文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            self.get_text('dialog_title'),
            "",
            self.get_text('dialog_filter')
        )
        
        if file_path:
            self.image_path = file_path
            self.path_edit.setText(file_path)
            # 重置预览状态
            self.preview_generated = False
            # 启用预览按钮,禁用生成和打印按钮
            self.update_button_states()
            # 显示提示文本
            self.preview_label.clear()
            self.preview_label.setText(self.get_text('preview_hint_click'))
            self.set_status_message(None)
            
    def on_parameter_changed(self):
        """参数改变时的处理"""
        if self.preview_generated:
            # 如果已经生成过预览,则禁用生成和打印按钮
            self.preview_generated = False
            self.update_button_states()
            # 显示参数改变提示
            self.preview_label.setText(self.get_text('preview_hint_params_changed'))
            self.set_status_message('preview_hint_params_changed')
    
    def update_button_states(self):
        """更新按钮状态"""
        has_image = bool(self.image_path)
        
        # 预览按钮:有图片时启用
        self.preview_btn.setEnabled(has_image)
        
        # 生成和打印按钮:有图片且已生成预览时启用
        self.generate_btn.setEnabled(has_image and self.preview_generated)
        allow_print = self.is_windows and has_image and self.preview_generated
        self.print_btn.setEnabled(allow_print)
        if not self.is_windows:
            self.print_btn.setToolTip(self.get_text('print_not_supported'))
        elif not allow_print:
            self.print_btn.setToolTip("")
    
    def set_status_message(self, key=None):
        """根据字典键更新状态标签, None 表示清除"""
        if self.status_label is None:
            return
        if key is None:
            self._status_message_key = None
            self.status_label.setText("")
        else:
            self._status_message_key = key
            self.status_label.setText(self.get_text(key))
    
    def validate_layout_parameters(self):
        """验证当前排版参数是否会生成有效的标签尺寸"""
        rows = self.rows_spin.value()
        cols = self.cols_spin.value()
        
        if rows <= 0 or cols <= 0:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('error_invalid_params')
            )
            return False
        
        orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'
        if orientation == 'landscape':
            page_width_mm, page_height_mm = 297.0, 210.0
        else:
            page_width_mm, page_height_mm = 210.0, 297.0
        
        margin = float(self.margin_spin.value())
        spacing = float(self.spacing_spin.value())
        
        usable_width = page_width_mm - 2 * margin
        usable_height = page_height_mm - 2 * margin
        
        label_width = (usable_width - (cols - 1) * spacing) / cols
        label_height = (usable_height - (rows - 1) * spacing) / rows
        
        if label_width <= 0 or label_height <= 0:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('error_invalid_params')
            )
            return False
        
        return True
    
    def generate_preview(self):
        """生成PDF预览"""
        if not self.image_path:
            return
        
        if not self.validate_layout_parameters():
            return
        
        pdf_document = None
        try:
            # 显示生成中提示
            self.preview_label.clear()
            self.preview_label.setText(self.get_text('preview_generating'))
            self.set_status_message('preview_generating')
            QApplication.processEvents()  # 强制更新UI
            
            # 获取页面方向
            orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'
            
            # 调用PDF生成函数(使用真实参数生成精确预览)
            pdf_bytes = self.tile_label_image_to_pdf(
                image_path=self.image_path,
                output_pdf=None,
                rows=self.rows_spin.value(),
                cols=self.cols_spin.value(),
                margin_mm=self.margin_spin.value(),
                spacing_mm=self.spacing_spin.value(),
                orientation=orientation,
                return_pdf_bytes=True
            )
            
            # 使用PyMuPDF将PDF转换为图片
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            page = pdf_document[0]  # 获取第一页
            
            # 设置缩放比例以获得高质量预览
            zoom = 3
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # 将pixmap转换为QPixmap
            img_data = pix.tobytes("png")
            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            
            # 缩放到预览区域大小
            scaled_pixmap = pixmap.scaled(
                400, 505,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # 显示预览
            self.preview_label.setPixmap(scaled_pixmap)
            self.set_status_message(None)
            
            # 标记预览已生成
            self.preview_generated = True
            self.update_button_states()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_preview').format(error=str(e))
            )
            # 恢复提示文本
            self.preview_label.setText(self.get_text('preview_hint_click'))
            self.set_status_message(None)
        finally:
            if pdf_document is not None:
                pdf_document.close()
            
    def update_label_count(self):
        """更新标签数量显示"""
        count = self.rows_spin.value() * self.cols_spin.value()
        self.count_label.setText(self.get_text('count_label').format(count=count))
        
    def generate_pdf(self):
        """生成PDF文件"""
        # 验证是否选择了图片
        if not self.image_path:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('warning_no_image')
            )
            return
        
        # 验证是否已生成预览
        if not self.preview_generated:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('warning_no_preview')
            )
            return
        
        # 验证图片文件是否存在
        if not os.path.exists(self.image_path):
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_not_exist')
            )
            return
        
        if not self.validate_layout_parameters():
            return
            
        try:
            # 确保outputs文件夹存在
            outputs_dir = self.ensure_outputs_folder()
            
            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_pdf = os.path.join(outputs_dir, f"label{timestamp}.pdf")
            
            # 获取页面方向
            orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'
            
            # 调用PDF生成函数
            self.tile_label_image_to_pdf(
                image_path=self.image_path,
                output_pdf=output_pdf,
                rows=self.rows_spin.value(),
                cols=self.cols_spin.value(),
                margin_mm=self.margin_spin.value(),
                spacing_mm=self.spacing_spin.value(),
                orientation=orientation
            )
            
            # 成功提示
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
                # 打开outputs文件夹
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
        """生成PDF并转换为PNG打印"""
        # 验证是否选择了图片
        if not self.image_path:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('warning_no_image')
            )
            return

        # 验证是否已生成预览
        if not self.preview_generated:
            QMessageBox.warning(
                self,
                self.get_text('warning_title'),
                self.get_text('warning_no_preview')
            )
            return

        # 验证图片文件是否存在
        if not os.path.exists(self.image_path):
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_not_exist')
            )
            return

        if not self.validate_layout_parameters():
            return

        if not self.is_windows:
            QMessageBox.information(
                self,
                self.get_text('warning_title'),
                self.get_text('print_not_supported')
            )
            self.set_status_message('print_not_supported')
            return

        if not QPrinterInfo.availablePrinters():
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_no_printer')
            )
            self.set_status_message('error_no_printer')
            return

        pdf_document = None
        try:
            # 确保outputs文件夹存在
            outputs_dir = self.ensure_outputs_folder()

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            output_pdf = os.path.join(outputs_dir, f"label{timestamp}.pdf")
            output_png = os.path.join(outputs_dir, f"label{timestamp}.png")
            
            # 获取页面方向
            orientation = 'landscape' if self.landscape_radio.isChecked() else 'portrait'
            
            self.set_status_message('preparing_print')
            QApplication.processEvents()
            
            # 1. 生成PDF文件
            self.tile_label_image_to_pdf(
                image_path=self.image_path,
                output_pdf=output_pdf,
                rows=self.rows_spin.value(),
                cols=self.cols_spin.value(),
                margin_mm=self.margin_spin.value(),
                spacing_mm=self.spacing_spin.value(),
                orientation=orientation
            )
            
            # 2. 使用PyMuPDF将PDF转换为PNG(300 DPI)
            pdf_document = fitz.open(output_pdf)
            page = pdf_document[0]  # 获取第一页
            
            # 设置300 DPI的缩放比例
            zoom = 300 / 72
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # 3. 保存PNG文件
            pix.save(output_png)
            
            self.set_status_message('print_ready')
            QApplication.processEvents()
            
            # 4. 使用os.startfile调用Windows打印对话框
            os.startfile(output_png, "print")
            
            # 显示成功消息
            QMessageBox.information(
                self,
                self.get_text('success_title'),
                self.get_text('print_success').format(
                    filename=output_pdf,
                    count=self.rows_spin.value() * self.cols_spin.value()
                )
            )
                    
        except Exception as e:
            self.set_status_message(None)
            QMessageBox.critical(
                self,
                self.get_text('error_title'),
                self.get_text('error_print_failed').format(error=str(e))
            )
        finally:
            if pdf_document is not None:
                pdf_document.close()
    

    def tile_label_image_to_pdf(self, image_path, output_pdf=None, rows=3, cols=4,
                                margin_mm=8, spacing_mm=3, orientation='landscape',
                                return_pdf_bytes=False):
        """
        将标签图片重复排列到一页A4纸上，并可选地返回 PDF 字节内容。
        """
        if output_pdf is None and not return_pdf_bytes:
            raise ValueError("output_pdf must be provided when return_pdf_bytes is False")
        
        # 延迟导入 reportlab（优化启动速度）
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.units import mm
        from reportlab.lib.utils import ImageReader
        
        # A4尺寸（横向或竖向）
        if orientation == 'landscape':
            page_size = landscape(A4)
        else:
            page_size = A4
        
        page_width, page_height = page_size
        margin = margin_mm * mm
        spacing = spacing_mm * mm
        
        # 计算可用空间
        usable_width = page_width - 2 * margin
        usable_height = page_height - 2 * margin
        
        # 计算单个标签区域大小
        label_width = (usable_width - (cols - 1) * spacing) / cols
        label_height = (usable_height - (rows - 1) * spacing) / rows
        
        # 读取图片验证
        try:
            img = Image.open(image_path)
            image_reader = ImageReader(img)
        except Exception as e:
            raise Exception(f"无法读取图片: {e}")
        
        buffer = io.BytesIO() if return_pdf_bytes else None
        target = buffer if buffer is not None else output_pdf
        try:
            # 创建PDF
            c = canvas.Canvas(target, pagesize=page_size)
            
            # 绘制标签网格
            for row in range(rows):
                for col in range(cols):
                    # 计算每个标签的位置
                    x = margin + col * (label_width + spacing)
                    y = page_height - margin - (row + 1) * label_height - row * spacing
                    
                    # 绘制图片
                    c.drawImage(
                        image_reader,
                        x, y,
                        width=label_width,
                        height=label_height,
                        preserveAspectRatio=True
                    )
            
            c.save()
        finally:
            img.close()
        
        if buffer is not None:
            pdf_bytes = buffer.getvalue()
            buffer.close()
            if output_pdf:
                with open(output_pdf, 'wb') as f:
                    f.write(pdf_bytes)
            return pdf_bytes
        
        return None
        
    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)


def create_splash_screen():
    """创建启动画面"""
    # 创建一个简单的启动画面
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(QColor("#3498db"))
    
    # 在启动画面上绘制文字
    painter = QPainter(splash_pix)
    painter.setPen(QColor("white"))
    
    # 设置字体
    title_font = QFont()
    title_font.setFamilies(["Leelawadee UI", "Microsoft YaHei UI", "sans-serif"])
    title_font.setPointSize(24)
    title_font.setBold(True)
    painter.setFont(title_font)
    
    # 绘制标题
    painter.drawText(splash_pix.rect(), Qt.AlignmentFlag.AlignCenter, "🏷️\n标签打印工具\nLabel Printer")
    
    # 绘制版本信息
    version_font = QFont()
    version_font.setFamilies(["Leelawadee UI", "Microsoft YaHei UI", "sans-serif"])
    version_font.setPointSize(12)
    painter.setFont(version_font)
    painter.drawText(20, 260, "正在加载... Loading...")
    
    painter.end()
    
    return QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用字体（支持中文和泰语，带回退机制）
    font = QFont()
    # 字体回退列表：泰语优先，中文次之，最后回退到系统默认
    # Leelawadee UI - Windows自带泰语字体
    # Microsoft YaHei UI - Windows自带中文字体
    # sans-serif - 系统默认无衬线字体
    font.setFamilies(["Leelawadee UI", "Microsoft YaHei UI", "sans-serif"])
    font.setPointSize(11)
    app.setFont(font)
    
    # 显示启动画面
    splash = create_splash_screen()
    splash.show()
    app.processEvents()
    
    # 创建主窗口（这里会加载所有组件）
    window = LabelPrinterQt()
    
    # 使用定时器延迟关闭启动画面，确保主窗口完全加载
    QTimer.singleShot(800, lambda: splash.finish(window))
    QTimer.singleShot(850, window.show)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()