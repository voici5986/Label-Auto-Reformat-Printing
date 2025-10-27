#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
标签打印工具 - PyQt6版本
现代化Material Design界面，支持文件选择、参数调整、时间戳命名、多语言
"""

import sys
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter
from ui import LabelPrinterQt


def create_splash_screen():
    """创建启动画面"""
    splash_pix = QPixmap(400, 300)
    splash_pix.fill(QColor("#3498db"))

    painter = QPainter(splash_pix)
    painter.setPen(QColor("white"))

    title_font = QFont()
    title_font.setFamilies(["Leelawadee UI", "Microsoft YaHei UI", "sans-serif"])
    title_font.setPointSize(24)
    title_font.setBold(True)
    painter.setFont(title_font)
    painter.drawText(splash_pix.rect(), Qt.AlignmentFlag.AlignCenter, "🏷️\n标签打印工具\nLabel Printer")

    version_font = QFont()
    version_font.setFamilies(["Leelawadee UI", "Microsoft YaHei UI", "sans-serif"])
    version_font.setPointSize(12)
    painter.setFont(version_font)
    painter.drawText(20, 260, "正在โหลด... Loading...")

    painter.end()

    return QSplashScreen(splash_pix, Qt.WindowType.WindowStaysOnTopHint)


def main():
    """程序入口"""
    app = QApplication(sys.argv)

    font = QFont()
    font.setFamilies(["Leelawadee UI", "Microsoft YaHei UI", "sans-serif"])
    font.setPointSize(11)
    app.setFont(font)

    splash = create_splash_screen()
    splash.show()
    app.processEvents()

    window = LabelPrinterQt()

    QTimer.singleShot(800, lambda: splash.finish(window))
    QTimer.singleShot(850, window.show)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
