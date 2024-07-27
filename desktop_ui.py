from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from dataclasses import dataclass
from enum import Enum
from itertools import count

@dataclass
class GeometryWidget():
    x: int
    y: int
    size_x: int
    size_y: int

@dataclass
class ButtonType(str, Enum):
    PLAY = 'play'
    STOP = 'stop'

@dataclass
class GeometryGrid(int, Enum):
    LABEL_X = 10
    LABEL_WIDTH = 100
    PLAY_BUTTON_X = 120
    STOP_BUTTON_X = 150
    VOLUME_SLIDER_X = 180
    VOLUME_SLIDER_WIDTH = 80
    WIDGET_HIGHT = 30
    BUTTON_WIDTH = WIDGET_HIGHT
    
    ONE_ROW_Y = 10
    # SECOND_ROW_Y = 40
    # THIRD_ROW_y = 70

class Track():
    _ids = count(0)
    
    def __init__(self, parent: QWidget, object_prefix: str, label_text: str):
                
        self.id = next(self._ids)
        # print(self.id)
        # print(object_prefix)
        # print()
        row_y = GeometryGrid.ONE_ROW_Y + GeometryGrid.WIDGET_HIGHT*(self.id )

        self.label_bird = Label(
            parent,
            GeometryWidget(
                x = GeometryGrid.LABEL_X,
                y = row_y,
                size_x = GeometryGrid.LABEL_WIDTH,
                size_y = GeometryGrid.WIDGET_HIGHT),
            object_prefix,
            label_text)

        self.bird_play_button = PlayerButton(
            parent,
            GeometryWidget(
                x = GeometryGrid.PLAY_BUTTON_X,
                y = row_y,
                size_x = GeometryGrid.BUTTON_WIDTH,
                size_y = GeometryGrid.WIDGET_HIGHT),
            object_prefix + '_play_button',
            ButtonType.PLAY)

        self.bird_stop_button = PlayerButton(
            parent,
            GeometryWidget(
                x = GeometryGrid.STOP_BUTTON_X,
                y = row_y,
                size_x = GeometryGrid.BUTTON_WIDTH,
                size_y = GeometryGrid.WIDGET_HIGHT),
            object_prefix + '_stop_button',
            ButtonType.STOP)

        self.bird_volume_slider = VolumeSlider(
            parent,
            GeometryWidget(
                x = GeometryGrid.VOLUME_SLIDER_X,
                y = row_y,
                size_x = GeometryGrid.VOLUME_SLIDER_WIDTH,
                size_y = GeometryGrid.WIDGET_HIGHT),
            object_prefix + '_volume_slider')
    
    @classmethod
    def get_object_count(self):
        return next(self._ids)


class Label(QtWidgets.QLabel):
    def __init__(self, parent: QWidget, geometry: GeometryWidget, object_name: str, text: str):
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.size_x, geometry.size_y))
        self.setObjectName(object_name)
        self.setText(text)

class PlayerButton(QtWidgets.QPushButton):
    def __init__(self, parent: QWidget, geometry: GeometryWidget, object_name: str, button_type: ButtonType):
        
        # player_button = QtWidgets.QPushButton(parent)
        # player_button = super().__init__(parent)
        
        # super().__init__(parent)
        super().__init__(parent)
        # self(parent)
        self.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.size_x, geometry.size_y))
        button_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        button_size_policy.setHorizontalStretch(0)
        button_size_policy.setVerticalStretch(0)
        button_size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(button_size_policy)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setToolTipDuration(-1)
        self.setStyleSheet("border: none")
        self.setText("")
        
        button_icon = QtGui.QIcon()
        if button_type is ButtonType.PLAY:
            button_icon.addPixmap(QtGui.QPixmap("./assets/play_black_big.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        else:
            button_icon.addPixmap(QtGui.QPixmap("./assets/stop_black_big.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setIcon(button_icon)
        self.setObjectName(object_name)
        
        
        self.clicked.connect(lambda: print(self.objectName()))
        
        # return player_button

class VolumeSlider(QtWidgets.QSlider):
    def __init__(self, parent: QWidget, geometry: GeometryWidget, object_name: str):
        
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(geometry.x, geometry.y, geometry.size_x, geometry.size_y))
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setObjectName(object_name)
        
        self.valueChanged.connect(lambda: print(self.objectName()))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # MainWindow.resize(280, 100)

        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setToolTipDuration(9)
        self.central_widget.setObjectName("central_widget")

        self.grid_widget = QtWidgets.QWidget(self.central_widget)
        # self.grid_widget.setGeometry(QtCore.QRect(0, 0, 280, 100))

        grid_size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        grid_size_policy.setHorizontalStretch(0)
        grid_size_policy.setVerticalStretch(0)
        grid_size_policy.setHeightForWidth(self.grid_widget.sizePolicy().hasHeightForWidth())
        self.grid_widget.setSizePolicy(grid_size_policy)
        self.grid_widget.setObjectName("grid_widget")

        
        #self.label_city = Label(self.grid_widget, Geometry(10, 40, 100, 25), "City", 'City')
        #self.label_bird = Label(self.grid_widget, Geometry(10, 70, 100, 25), "Rain", 'Rain')

        self.track_1 = Track(self.grid_widget, 'bird', 'Bird')
        self.track_2 = Track(self.grid_widget, 'rain', 'Rain')
        self.track_3 = Track(self.grid_widget, 'city', 'City')
        
        #print(Track.get_object_count())
        row_count = Track.get_object_count()
        print(row_count)
        window_hight = GeometryGrid.ONE_ROW_Y*2 + GeometryGrid.WIDGET_HIGHT*row_count 
        #+ GeometryGrid.ONE_ROW_Y*(row_count - 1)
        
        MainWindow.resize(280, window_hight)
        print(window_hight)
        
        self.grid_widget.setGeometry(QtCore.QRect(0, 0, 280, window_hight))
        

        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
