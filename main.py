# Add system path

import os, sys
sys.path.append(os.path.join(os.path.abspath(os.getcwd()), 'segmentation_program'))

import PySide2
from PySide2.QtWidgets import QApplication
from PySide2 import QtWidgets, QtCore, QtGui
from user_interface.main_window import MainWindow

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.setWindowTitle('human part segmentation')
        self.setAcceptDrops(True)

    def set_child(self, child):
        v_layout = QtWidgets.QVBoxLayout()
        v_layout.setSpacing(0)
        v_layout.setMargin(0)
        v_layout.addWidget(child)
        self.setLayout(v_layout)
        child.setParent(self)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            #event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            get_image(file_path)
 
            event.accept()
        else:
            event.ignore()

def get_image(image_path):
    sub.get_image(image_path)

if '__main__' == __name__:
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QtWidgets.QApplication(sys.argv)
    parent = MyWidget()
    sub = MainWindow(app, parent)
    parent.set_child(sub.window)

    parent.show()
    ret = app.exec_()
    sys.exit(ret)
