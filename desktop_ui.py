""" Desktop GUI. """
import os
import sys

from dataclasses import dataclass
from enum import Enum
from itertools import count
from pathlib import Path

from PyQt5.QtCore import (
    QUrl,
    QFileInfo,
    QRect,
    QMetaObject,
    #QCoreApplication,
    Qt)
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QPixmap

@dataclass
class GeometryWidget():
    """ Geometry settings for one widget. """

    x: int
    y: int
    size_x: int
    size_y: int

@dataclass
class ButtonType(str, Enum):
    """ Button types. """

    PLAY = 'play'
    STOP = 'stop'

@dataclass
class GeometryGrid(int, Enum):
    """ Geometry characteristics for grid. """

    LABEL_X = 10
    LABEL_WIDTH = 100
    PLAY_BUTTON_X = 120
    STOP_BUTTON_X = 150
    VOLUME_SLIDER_X = 180
    VOLUME_SLIDER_WIDTH = 80
    WIDGET_HIGHT = 30
    BUTTON_WIDTH = WIDGET_HIGHT
    ONE_ROW_Y = 10

def current_folder(folder_name: str):
    """ Defining current work folder. """

    if getattr(sys, "frozen", False):
        base_directory = sys._MEIPASS
    else:
        base_directory = os.path.dirname(os.path.realpath("__file__"))

    return os.path.join(base_directory, folder_name)

class Track():
    """ Track entity. """

    _ids = count(0)

    def __init__(self, parent: QWidget, object_prefix: str, label_text: str):

        self.base_directory = os.path.dirname(os.path.realpath("__file__"))
        self.id = next(self._ids)
        self.media_player = QMediaPlayer()
        self.media_player.setMedia(
            QMediaContent(
                QUrl.fromLocalFile(
                    QFileInfo(
                        os.path.join(
                            'background_sounds', f'{object_prefix}.mp3')).absoluteFilePath())))

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

        self.bird_play_button.clicked.connect(self.play_track)
        self.bird_stop_button.clicked.connect(self.stop_track)

        self.bird_volume_slider.valueChanged.connect(
            lambda: self.set_volume_track(self.bird_volume_slider.value()))

        self.media_player.mediaStatusChanged.connect(self.play_track_again)

    @classmethod
    def get_object_count(cls) -> int:
        """ Return Tracks count. """

        return next(cls._ids)

    def play_track(self):
        """ Press button start action. """

        self.media_player.play()

    def play_track_again(self, status):
        """ Restarting track. """

        if status == 7:
            self.media_player.play()

    def stop_track(self):
        """ Press button stop action. """

        self.media_player.stop()

    def set_volume_track(self, value):
        """ Changing volume. """

        self.media_player.setVolume(value)

class Label(QLabel):
    """ Label for track. """

    def __init__(self, parent: QWidget, geometry: GeometryWidget, object_name: str, text: str):

        super().__init__(parent)

        self.setGeometry(QRect(geometry.x, geometry.y, geometry.size_x, geometry.size_y))
        self.setObjectName(object_name)
        self.setText(text)

class PlayerButton(QPushButton):
    """ Play button. """

    def __init__(
        self,
        parent: QWidget,
        geometry: GeometryWidget,
        object_name: str,
        button_type: ButtonType):

        super().__init__(parent)

        self.setGeometry(QRect(geometry.x, geometry.y, geometry.size_x, geometry.size_y))

        button_size_policy = QSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Maximum)
        button_size_policy.setHorizontalStretch(0)
        button_size_policy.setVerticalStretch(0)
        button_size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(button_size_policy)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setToolTipDuration(-1)
        self.setStyleSheet("border: none")
        self.setText("")

        button_icon = QIcon()
        if button_type is ButtonType.PLAY:
            button_icon.addPixmap(
                QPixmap(os.path.join(current_folder('assets'), 'play_black_big.png')),
                QIcon.Normal,
                QIcon.Off)
        else:
            button_icon.addPixmap(
                QPixmap(os.path.join(current_folder('assets'), 'stop_black_big.png')),
                QIcon.Normal,
                QIcon.Off)

        self.setIcon(button_icon)
        self.setObjectName(object_name)

class VolumeSlider(QSlider):
    """ Volume change slinder. """

    def __init__(self, parent: QWidget, geometry: GeometryWidget, object_name: str):

        super().__init__(parent)

        self.setGeometry(QRect(geometry.x, geometry.y, geometry.size_x, geometry.size_y))

        size_policy = QSizePolicy(
            QSizePolicy.Ignored,
            QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(size_policy)
        self.setOrientation(Qt.Horizontal)
        self.setObjectName(object_name)

class UiMainWindow(object):
    """ Desktop window. """

    def setup_ui(self, main_window):
        """ Set window settings. """

        main_window.setObjectName("MainWindow")

        self.central_widget = QWidget(main_window)
        self.central_widget.setToolTipDuration(9)
        self.central_widget.setObjectName("central_widget")

        self.grid_widget = QWidget(self.central_widget)

        grid_size_policy = QSizePolicy(
            QSizePolicy.Maximum,
            QSizePolicy.Maximum)
        grid_size_policy.setHorizontalStretch(0)
        grid_size_policy.setVerticalStretch(0)
        grid_size_policy.setHeightForWidth(self.grid_widget.sizePolicy().hasHeightForWidth())
        self.grid_widget.setSizePolicy(grid_size_policy)
        self.grid_widget.setObjectName("grid_widget")

        for track in os.listdir('./background_sounds'):
            track_name = Path(track).stem
            print(track_name)
            Track(self.grid_widget, track_name, track_name)

        row_count = Track.get_object_count()
        window_hight = GeometryGrid.ONE_ROW_Y*2 + GeometryGrid.WIDGET_HIGHT*row_count

        self.grid_widget.setGeometry(QRect(0, 0, 280, window_hight))

        main_window.resize(280, window_hight)
        main_window.setCentralWidget(self.central_widget)
        main_window.setWindowTitle("MainWindow")

        QMetaObject.connectSlotsByName(main_window)
