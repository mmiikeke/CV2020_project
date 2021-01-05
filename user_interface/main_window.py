"""Mainwindow of the user interface, host and control the operation.
"""

import os, threading
from collections import OrderedDict

from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import Qt, QFile, QPropertyAnimation, QParallelAnimationGroup
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QFont, QIcon, QPixmap
from segmentation_program.merge import segment_image, merge_image

from user_interface.page_widget import page1, page2, page3, page4

__copyright__ = 'Copyright © 2020 mmiikeke - All Right Reserved.'

FORM = 'user_interface/form/ui_main.ui'

class MainWindow(QtCore.QObject):

    def __init__(self, main_app, parent=None):
        super(MainWindow, self).__init__(parent)
        """Main window, holding all user interface including.

        Args:
          parent: parent class of main window
        Returns:
          None
        Raises:
          None
        """
        self.app = main_app
        self._window = None
        self._pages = OrderedDict()
        self.setup_ui()

        if not os.path.isdir('tmp'):
            os.makedirs('tmp')

    @property
    def window(self):
        """The main window object"""
        return self._window

    def setup_ui(self):
        """Initialize user interface of main window."""
        loader = QUiLoader()
        file = QFile(FORM)
        file.open(QFile.ReadOnly)
        self._window = loader.load(file)
        file.close()

        self.set_pages()
        self.set_buttons()
        #self.test()
    
    def test(self):
        aa = GraphicView()
        # Add to frame
        g_layout = QtWidgets.QGridLayout(self._window.frame_content)
        g_layout.setSpacing(0)
        g_layout.setMargin(0)
        g_layout.addWidget(aa, 0, 0, 1, 1)

    def set_pages(self):
        """Setup pages"""
        self._pages['page1'] = page1()
        self._pages['page2'] = page2()
        self._pages['page3'] = page3()
        self._pages['page4'] = page4(self.app)

        # Add to frame
        g_layout = QtWidgets.QGridLayout(self._window.frame_content)
        g_layout.setSpacing(0)
        g_layout.setMargin(0)

        for index, name in enumerate(self._pages):
            g_layout.addWidget(self._pages[name].widget, 0, 0, 1, 1)

        self._pages['page2'].widget.stackUnder(self._pages['page1'].widget)
        self._pages['page2'].widget.setDisabled(True)
        self._pages['page2'].widget.hide()
        self._pages['page3'].widget.stackUnder(self._pages['page2'].widget)
        self._pages['page3'].widget.setDisabled(True)
        self._pages['page3'].widget.hide()
        self._pages['page4'].widget.stackUnder(self._pages['page3'].widget)
        self._pages['page4'].widget.setDisabled(True)
        self._pages['page4'].widget.hide()

    def set_buttons(self):
        """Setup buttons"""
        self._pages['page1'].widget.btn_start.clicked.connect(lambda: self.next_page(self._pages['page1'].widget, self._pages['page2'].widget))
        self._pages['page2'].widget.btn_start.clicked.connect(lambda: self.segment())
        self._pages['page3'].widget.btn_start.clicked.connect(lambda: self.initialize_merge())
        self._pages['page4'].widget.btn_start.clicked.connect(lambda: self.start_merge())

    def get_image(self, image_path):
        if os.path.isfile(image_path):
            for index, name in enumerate(self._pages):
                if self._pages[name].widget.isEnabled():
                    print(f'find {name}, path = {image_path}')
                    self._pages[name].get_image(image_path)
                        
    @QtCore.Slot()
    def next_page(self, a, b):
        a.setDisabled(True)
        b.setGeometry(a.geometry().translated(a.geometry().width() * 1.1, 0))
        b.show()

        # ANIMATION
        self.anim_a = QPropertyAnimation(a, b"geometry")
        self.anim_a.setDuration(2000)
        self.anim_a.setStartValue(a.geometry())
        self.anim_a.setEndValue(a.geometry().translated(-a.geometry().width() * 1.5, 0))
        self.anim_a.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        
        #print(b.geometry())
        self.anim_b = QPropertyAnimation(b, b"geometry")
        self.anim_b.setDuration(2200)
        self.anim_b.setKeyValueAt(0, a.geometry().translated(a.geometry().width() * 1.1, 0))
        self.anim_b.setKeyValueAt(0.2, a.geometry().translated(a.geometry().width() * 1.1, 0))
        self.anim_b.setKeyValueAt(1, a.geometry())
        self.anim_b.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.anim_a)
        self.group.addAnimation(self.anim_b)
        self.group.start()

        QtCore.QTimer.singleShot(2200, lambda: self.next_page_callback(a, b))
    
    @QtCore.Slot()
    def next_page_callback(self, a, b):
        b.setDisabled(False)
        a.stackUnder(b)
        a.hide()

    @QtCore.Slot()
    def segment(self):
        self._pages['page2'].widget.btn_start.setDisabled(True)
        self.image_path = self._pages['page2'].image_path

        result = segment_image(self.image_path)

        self.next_page(self._pages['page2'].widget, self._pages['page3'].widget)
        self._pages['page2'].widget.btn_start.setDisabled(False)
    
    @QtCore.Slot()
    def initialize_merge(self):
        self._pages['page3'].widget.btn_start.setDisabled(True)
        self.image_path = self._pages['page3'].image_path

        self._pages['page4'].initialize_merge(self.image_path)

        self.next_page(self._pages['page3'].widget, self._pages['page4'].widget)
        self._pages['page3'].widget.btn_start.setDisabled(False)

    @QtCore.Slot()
    def start_merge(self):
        self._pages['page4'].widget.btn_start.setDisabled(True)
        self.human_path = 'tmp/out0.png'
        self.bg_path = self._pages['page3'].image_path
        bgw, bgh = self._pages['page4'].aa.bgw, self._pages['page4'].aa.bgh
        imgw, imgh = self._pages['page4'].aa.imgw, self._pages['page4'].aa.imgh
        x, y = self._pages['page4'].aa.moveObject.pos().x(), self._pages['page4'].aa.moveObject.pos().y()
        print(f'bgw = {bgw}, bgh = {bgh}, imgw = {imgw}, imgh = {imgh}, pos = {x}, {y}')
        result = merge_image(self.human_path, self.bg_path, bgw, bgh, imgw, imgh, x, y)

        self.next_page(self._pages['page4'].widget, self._pages['page1'].widget)
        self._pages['page4'].widget.btn_start.setDisabled(False)
        