"""The item widget page
"""

import os, math
from PySide2 import QtCore, QtWidgets, QtGui, QtUiTools
from PySide2.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsPixmapItem
from PySide2.QtCore import Qt, QPointF
from PIL import Image

__copyright__ = 'Copyright © 2020 mmiikeke - All Right Reserved.'

PAGE1 = 'user_interface/form/ui_page1.ui'
PAGE2 = 'user_interface/form/ui_page2.ui'
PAGE3 = 'user_interface/form/ui_page3.ui'
PAGE4 = 'user_interface/form/ui_page4.ui'

class MovingObject(QGraphicsPixmapItem):
    def __init__(self, scaled, x, y, r):
        super().__init__(scaled)
        self.setPos(x, y)
        #self.setPixmap(scaled)
        self.setAcceptHoverEvents(True)

    # mouse hover event
    def hoverEnterEvent(self, event):
        global app
        app.instance().setOverrideCursor(Qt.OpenHandCursor)
 
    def hoverLeaveEvent(self, event):
        global app
        app.instance().restoreOverrideCursor()
 
    # mouse click event
    def mousePressEvent(self, event):
        pass
 
    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()
 
        orig_position = self.scenePos()
 
        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
 
    def mouseReleaseEvent(self, event):
        print('x: {0}, y: {1}'.format(self.pos().x(), self.pos().y()))

class GraphicView(QGraphicsView):
    def __init__(self, image_path):
        super().__init__()

        # background
        pixmap = QtGui.QPixmap(image_path)
        #scaled = pixmap.scaled(QtCore.QSize(1000, 635), QtCore.Qt.KeepAspectRatio)
        scaled = pixmap
        self.bgh = scaled.height()
        self.bgw = scaled.width()
        bgpixItem = QGraphicsPixmapItem(scaled)

        # create scene
        self.scene = QGraphicsScene()
        self.setScene(self.scene)       
        self.setSceneRect(0, 0, self.bgw, self.bgh)

        self.scene.addItem(bgpixItem)


        pixmap = QtGui.QPixmap('tmp/out1.png')
        scaled = pixmap.scaled(QtCore.QSize(256, 256), QtCore.Qt.KeepAspectRatio)
        self.imgh = scaled.height()
        self.imgw = scaled.width()
        self.moveObject = MovingObject(scaled, 50, 50, 40)
        self.scene.addItem(self.moveObject)

class page1(QtCore.QObject):
    def __init__(self, parent=None):

        super(page1, self).__init__(parent)

        self._widget = None

        self.setup_ui()
        
    @property
    def widget(self):
        return self._widget
    
    def setup_ui(self):
        """Initialize user interface of widget."""
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(PAGE1)
        file.open(QtCore.QFile.ReadOnly)
        self._widget = loader.load(file)
        file.close()

        self.set_buttons()

    def set_buttons(self):
        """Setup buttons"""

class page2(QtCore.QObject):
    def __init__(self, parent=None):

        super(page2, self).__init__(parent)
        
        self._widget = None

        self.setup_ui()
        
    @property
    def widget(self):
        return self._widget
    
    def setup_ui(self):
        """Initialize user interface of widget."""
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(PAGE2)
        file.open(QtCore.QFile.ReadOnly)
        self._widget = loader.load(file)
        file.close()

        self.set_buttons()

    def set_buttons(self):
        """Setup buttons"""
        self._widget.btn_input.clicked.connect(self.select_input)

    def get_image(self, path):
        if not path.endswith('.png'):
            image = Image.open(path).convert('RGB')
            path = 'tmp/human.png'
            image.save('tmp/human.png')

        pixmap = QtGui.QPixmap(path)
        scaled = pixmap.scaled(QtCore.QSize(798, 469), QtCore.Qt.KeepAspectRatio)
        self._widget.label_input.setPixmap(scaled)
        self.image_path = path

    @QtCore.Slot()
    def select_input(self):
        file = str(QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "./", "Image File (*.jpg *.jpeg *.png *.jiff)")[0])
        self.get_image(file)

class page3(QtCore.QObject):
    def __init__(self, parent=None):

        super(page3, self).__init__(parent)
        
        self._widget = None

        self.setup_ui()
        
    @property
    def widget(self):
        return self._widget
    
    def setup_ui(self):
        """Initialize user interface of widget."""
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(PAGE3)
        file.open(QtCore.QFile.ReadOnly)
        self._widget = loader.load(file)
        file.close()

        self.set_buttons()

    def set_buttons(self):
        """Setup buttons"""
        self._widget.btn_input.clicked.connect(self.select_input)

    def get_image(self, path):
        if not path.endswith('.png'):
            image = Image.open(path).convert('RGB')
            path = 'tmp/bg.png'
            image.save('tmp/bg.png')

        pixmap = QtGui.QPixmap(path)
        scaled = pixmap.scaled(QtCore.QSize(798, 469), QtCore.Qt.KeepAspectRatio)
        self._widget.label_input.setPixmap(scaled)
        self.image_path = path

    @QtCore.Slot()
    def select_input(self):
        file = str(QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "./", "Image File (*.jpg *.jpeg *.png *.jiff)")[0])
        self.get_image(file)

class page4(QtCore.QObject):
    def __init__(self, main_app, parent=None):

        super(page4, self).__init__(parent)

        self._widget = None
        global app
        app = main_app
        self.setup_ui()
        self.aa = None
        
    @property
    def widget(self):
        return self._widget
    
    def setup_ui(self):
        """Initialize user interface of widget."""
        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(PAGE4)
        file.open(QtCore.QFile.ReadOnly)
        self._widget = loader.load(file)
        file.close()

    def initialize_merge(self, image_path):
        if self.aa != None:
            for i in reversed(range(self.g_layout.count())): 
                self.g_layout.removeWidget(self.aa)
            self.aa = GraphicView(image_path)
            self.g_layout.addWidget(self.aa, 0, 0, 1, 1)
        else:
            self.aa = GraphicView(image_path)
            # Add to frame
            self.g_layout = QtWidgets.QGridLayout(self._widget.frame_inputdata)
            self.g_layout.setSpacing(0)
            self.g_layout.setMargin(0)
            self.g_layout.addWidget(self.aa, 0, 0, 1, 1)