# Program Name: Mp3 Music Player
# Created by: Bryant Liu
# Date Created: December 08 2021

try:
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import QIcon, QPixmap
    from songhandling import *
    from readwrite import *
    import getpass
    import os
    import math
    import random
    from pygame import mixer
    from time import sleep
    from threading import *
except:
    input("error")


class Ui_UnidentifiedPlayer(object):
    """window class"""
    def setupUi(self, UnidentifiedPlayer):
        """setup window inputs and other beginning processes"""
        mixer.init()
        self.t1 = Thread(target=self.play_pause)
        self.volume_level = 50
        self.shuffle = "off"
        self.repeat = "off"
        self.slider_pressed = False
        self.fname = None
        self.ready_to_play = False
        self.playing_state = False
        self.song_list = []
        (self.title, self.artist, self.duration, self.file,
         self.ftype, self.fsize, self.bitrate, self.directory,
         self.rawsecs) = get_song_data(self.fname)
        self.nulltime = 0
        # window settings
        UnidentifiedPlayer.setObjectName("UnidentifiedPlayer")
        UnidentifiedPlayer.setWindowTitle("Unidentified Player")
        UnidentifiedPlayer.resize(700, 340)
        UnidentifiedPlayer.setFixedSize(700, 340)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                           QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UnidentifiedPlayer.sizePolicy().
                                     hasHeightForWidth())
        UnidentifiedPlayer.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon("iconUP.png")
        UnidentifiedPlayer.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(UnidentifiedPlayer)
        self.centralwidget.setObjectName("centralwidget")
        # song slider
        self.songtimeslider = QtWidgets.QSlider(self.centralwidget)
        self.songtimeslider.setGeometry(QtCore.QRect(230, 140, 300, 22))
        self.songtimeslider.setMinimum(0)
        self.songtimeslider.setMaximum(100000)
        self.songtimeslider.setPageStep(0)
        self.songtimeslider.setOrientation(QtCore.Qt.Horizontal)
        self.songtimeslider.setObjectName("songtimeslider")
        self.songtimeslider.sliderPressed.connect(self.disableslider)
        self.songtimeslider.sliderReleased.connect(self.changetime)
        # play/pause button
        self.playpausebutton = QtWidgets.QPushButton(self.centralwidget)
        self.playpausebutton.setGeometry(QtCore.QRect(340, 170, 81, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.playpausebutton.setFont(font)
        self.playpausebutton.setIconSize(QtCore.QSize(16, 16))
        self.playpausebutton.setObjectName("playpausebutton")
        self.playpausebutton.clicked.connect(self.thread)
        # volume dial
        self.volumedial = QtWidgets.QDial(self.centralwidget)
        self.volumedial.setGeometry(QtCore.QRect(560, 20, 121, 121))
        self.volumedial.setMaximum(100)
        self.volumedial.setPageStep(1)
        self.volumedial.setProperty("value", 50)
        self.volumedial.setSliderPosition(50)
        self.volumedial.setTracking(True)
        self.volumedial.setOrientation(QtCore.Qt.Horizontal)
        self.volumedial.setInvertedAppearance(False)
        self.volumedial.setInvertedControls(True)
        self.volumedial.setWrapping(False)
        self.volumedial.setNotchTarget(7.7)
        self.volumedial.setNotchesVisible(True)
        self.volumedial.setObjectName("volumedial")
        self.volumedial.valueChanged.connect(lambda: self.vol_change())
        self.volumedial.sliderReleased.connect(self.update_config)
        # forwards button
        self.forwardsbutton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardsbutton.setGeometry(QtCore.QRect(420, 170, 111, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.forwardsbutton.setFont(font)
        self.forwardsbutton.setObjectName("forwardbutton")
        self.forwardsbutton.clicked.connect(self.forwards)
        # backwards button
        self.backwardsbutton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardsbutton.setGeometry(QtCore.QRect(230, 170, 111, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.backwardsbutton.setFont(font)
        self.backwardsbutton.setObjectName("backwardsbutton")
        self.backwardsbutton.clicked.connect(self.backwards)
        # shuffle button
        self.shufflebutton = QtWidgets.QPushButton(self.centralwidget)
        self.shufflebutton.setGeometry(QtCore.QRect(230, 250, 151, 41))
        self.shufflebutton.setObjectName("shufflebutton")
        self.shufflebutton.clicked.connect(self.shuffle_change)
        # repeat button
        self.repeatbutton = QtWidgets.QPushButton(self.centralwidget)
        self.repeatbutton.setGeometry(QtCore.QRect(380, 250, 151, 41))
        self.repeatbutton.setObjectName("repeatbutton")
        self.repeatbutton.clicked.connect(self.repeat_change)
        # stop button (eject)
        self.stopsongbutton = QtWidgets.QPushButton(self.centralwidget)
        self.stopsongbutton.setGeometry(QtCore.QRect(225, 0, 18, 120))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.stopsongbutton.setFont(font)
        self.stopsongbutton.setObjectName("stopsongbutton")
        self.stopsongbutton.clicked.connect(self.stop)
        # load song(s) button
        self.loadsongsbutton = QtWidgets.QPushButton(self.centralwidget)
        self.loadsongsbutton.setGeometry(QtCore.QRect(10, 0, 200, 21))
        self.loadsongsbutton.setObjectName("loadsongsbutton")
        self.loadsongsbutton.clicked.connect(self.add_songs)
        # remove selection button
        self.removeselectionbutton = QtWidgets.QPushButton(self.centralwidget)
        self.removeselectionbutton.setGeometry(QtCore.QRect(10, 300, 200, 21))
        self.removeselectionbutton.setObjectName("removeselection")
        self.removeselectionbutton.clicked.connect(self.remove)
        # songtime label
        self.songtimelabel = QtWidgets.QLabel(self.centralwidget)
        self.songtimelabel.setGeometry(QtCore.QRect(500, 120, 47, 13))
        self.songtimelabel.setObjectName("songtimelabel")
        # volume value label
        self.volumevaluelabel = QtWidgets.QLabel(self.centralwidget)
        self.volumevaluelabel.setGeometry(QtCore.QRect(610, 70, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.volumevaluelabel.setFont(font)
        self.volumevaluelabel.setObjectName("volumelabel")
        # volume label
        self.volumelabel = QtWidgets.QLabel(self.centralwidget)
        self.volumelabel.setGeometry(QtCore.QRect(600, 140, 47, 13))
        self.volumelabel.setObjectName("volumelabel")
        # plus sign label
        self.pluslabel = QtWidgets.QLabel(self.centralwidget)
        self.pluslabel.setGeometry(QtCore.QRect(660, 130, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pluslabel.setFont(font)
        self.pluslabel.setObjectName("pluslabel")
        # minus sign label
        self.minuslabel = QtWidgets.QLabel(self.centralwidget)
        self.minuslabel.setGeometry(QtCore.QRect(570, 130, 16, 16))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.minuslabel.setFont(font)
        self.minuslabel.setObjectName("minuslabel")
        # image
        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(550, 170, 130, 130))
        pixmap = QPixmap("iconUP.png")
        pixmap = pixmap.scaled(130, 130, QtCore.Qt.KeepAspectRatio)
        self.image.setPixmap(pixmap)
        self.image.setObjectName("imagelabel")
        # title label
        self.titlelabel = QtWidgets.QLabel(self.centralwidget)
        self.titlelabel.setGeometry(QtCore.QRect(250, 10, 47, 13))
        self.titlelabel.setObjectName("titlelabel")
        # artist label
        self.artistlabel = QtWidgets.QLabel(self.centralwidget)
        self.artistlabel.setGeometry(QtCore.QRect(250, 23, 47, 13))
        self.artistlabel.setObjectName("artistlabel")
        # duration label
        self.durationlabel = QtWidgets.QLabel(self.centralwidget)
        self.durationlabel.setGeometry(QtCore.QRect(250, 36, 47, 13))
        self.durationlabel.setObjectName("durationlabel")
        # filename label
        self.filenamelabel = QtWidgets.QLabel(self.centralwidget)
        self.filenamelabel.setGeometry(QtCore.QRect(250, 61, 47, 13))
        self.filenamelabel.setObjectName("filenamelabel")
        # type label
        self.typelabel = QtWidgets.QLabel(self.centralwidget)
        self.typelabel.setGeometry(QtCore.QRect(250, 74, 47, 13))
        self.typelabel.setObjectName("typelabel")
        # size label
        self.sizelabel = QtWidgets.QLabel(self.centralwidget)
        self.sizelabel.setGeometry(QtCore.QRect(250, 87, 47, 13))
        self.sizelabel.setObjectName("sizelabel")
        # bitrate label
        self.bitratelabel = QtWidgets.QLabel(self.centralwidget)
        self.bitratelabel.setGeometry(QtCore.QRect(250, 100, 47, 13))
        self.bitratelabel.setObjectName("bitratelabel")
        # seperator line
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(210, 6, 20, 334))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        # info label
        self.infolabel = QtWidgets.QLabel(self.centralwidget)
        self.infolabel.setGeometry(QtCore.QRect(230, 290, 301, 16))
        self.infolabel.setObjectName("infolabel")
        # list widget for songs
        self.list_widget = QListWidget(self.centralwidget)
        self.list_widget.setGeometry(5, 25, 210, 270)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        self.list_widget.itemActivated.connect(self.loader)
        self.scroll_bar = QScrollBar(self.centralwidget)
        self.list_widget.setVerticalScrollBar(self.scroll_bar)
        self.list_widget.itemPressed.connect(self.update_songs)
        # menubar and statusbar settings
        UnidentifiedPlayer.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(UnidentifiedPlayer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 700, 21))
        self.menubar.setObjectName("menubar")
        UnidentifiedPlayer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(UnidentifiedPlayer)
        self.statusbar.setObjectName("statusbar")
        UnidentifiedPlayer.setStatusBar(self.statusbar)
        # update labels
        self.retranslateUi(UnidentifiedPlayer)
        self.settings_inquire()
        self.song_inquire()
        # connecting events
        QtCore.QMetaObject.connectSlotsByName(UnidentifiedPlayer)

    ###########
    def retranslateUi(self, UnidentifiedPlayer):
        """label widgets"""
        _translate = QtCore.QCoreApplication.translate
        UnidentifiedPlayer.setWindowTitle(_translate("UnidentifiedPlayer",
                                                     "Unidentified Player"))
        self.playpausebutton.setText(_translate("UnidentifiedPlayer", "►"))
        self.forwardsbutton.setText(_translate("UnidentifiedPlayer", "►▌"))
        self.backwardsbutton.setText(_translate("UnidentifiedPlayer", "▐◄"))
        self.shufflebutton.setText(_translate("UnidentifiedPlayer",
                                              "Shuffle: Off"))
        self.repeatbutton.setText(_translate("UnidentifiedPlayer",
                                             "Repeat: Off"))
        self.stopsongbutton.setText(_translate("UnidentifiedPlayer", "■"))
        self.loadsongsbutton.setText(_translate("UnidentifiedPlayer",
                                                "Add Song(s)"))
        self.removeselectionbutton.setText(_translate("UnidentifiedPlayer",
                                                      "Remove Selection"))
        self.songtimelabel.setText(_translate("UnidentifiedPlayer", "00:00"))
        self.volumevaluelabel.setText(_translate("UnidentifiedPlayer",
                                                 str(self.volume_level)))
        self.artistlabel.setText(_translate("UnidentifiedPlayer", "Artist:"))
        self.titlelabel.setText(_translate("UnidentifiedPlayer", "Title:"))
        self.durationlabel.setText(_translate("UnidentifiedPlayer",
                                              "Duration:"))
        self.filenamelabel.setText(_translate("UnidentifiedPlayer", "File:"))
        self.typelabel.setText(_translate("UnidentifiedPlayer", "Type:"))
        self.sizelabel.setText(_translate("UnidentifiedPlayer", "Size:"))
        self.bitratelabel.setText(_translate("UnidentifiedPlayer", "Bitrate:"))
        self.pluslabel.setText(_translate("UnidentifiedPlayer", "+"))
        self.minuslabel.setText(_translate("UnidentifiedPlayer", "-"))
        self.volumelabel.setText(_translate("UnidentifiedPlayer", "VOLUME"))
        self.infolabel.setText(_translate("UnidentifiedPlayer",
                                          "(Note: Currently, only mp3s and" +
                                          "flacs are supported!)"))
        self.updatelabels()

    def updatelabels(self):
        """update labels"""
        self.titlelabel.setText(f"Title: {self.title}")
        self.titlelabel.adjustSize()
        self.artistlabel.setText(f"Artist: {self.artist}")
        self.artistlabel.adjustSize()
        self.durationlabel.setText(f"Duration: {self.duration}")
        self.durationlabel.adjustSize()
        self.filenamelabel.setText(f"File: {self.file}")
        self.filenamelabel.adjustSize()
        self.typelabel.setText(f"Type: {self.ftype}")
        self.typelabel.adjustSize()
        self.sizelabel.setText(f"Size : {self.fsize} MB")
        self.sizelabel.adjustSize()
        self.bitratelabel.setText(f"Bitrate: {self.bitrate} kbps")
        self.bitratelabel.adjustSize()

    def settings_inquire(self):
        """extract settings from config.txt"""
        self.volume_level, self.shuffle, self.repeat = get_settings()
        mixer.music.set_volume(self.volume_level/100)
        self.volumevaluelabel.setText(str(self.volume_level))
        self.volumedial.setProperty("value", self.volume_level)
        if self.shuffle == "off":
            self.shuffle = "off"
            self.shufflebutton.setText("Shuffle: Off")
        elif self.shuffle == "on":
            self.shuffle = "on"
            self.shufflebutton.setText("Shuffle: On")
        if self.repeat == "off":
            self.repeat = "off"
            self.repeatbutton.setText("Repeat: Off")
        elif self.repeat == "queue":
            self.repeat = "queue"
            self.repeatbutton.setText("Repeat: Queue")
        elif self.repeat == "track":
            self.repeat = "track"
            self.repeatbutton.setText("Repeat: Track")

    def song_inquire(self):
        """extract songs from queue.txt"""
        self.song_list = get_songs()
        for item in self.song_list:
            self.list_widget.addItem(item)

    ###########
    def add_songs(self):
        """add songs to queue"""
        try:
            self.fname = QFileDialog.getOpenFileNames(None,
                                                      'Add Song(s)',
                                                      'c:\\Users\\' +
                                                      getpass.getuser() +
                                                      '\\Music',
                                                      "Audio Files \
                                                      (*.mp3 *.flac)")
            if self.fname[0][0] not in ("", " ", None):
                for item in self.fname[0]:
                    self.list_widget.addItem(item)
                    self.song_list.append(item)
                self.update_songs()

        except:
            pass

    def loader(self):
        """load song into player"""
        try:
            self.stop()
        except:
            pass
        try:
            item = self.list_widget.currentItem()
            self.songd = item.text()
            (self.title, self.artist, self.duration, self.file,
             self.ftype, self.fsize, self.bitrate, self.directory,
             self.rawsecs) = get_song_data(self.songd)
            self.updatelabels()
            self.playing_state = False
            self.ready_to_play = True
            mixer.music.load(self.directory)
            mixer.music.play()
            mixer.music.pause()
        except:
            self.stop()
            self.remove()

    def thread(self):
        """thread for timebar"""
        self.t1 = Thread(target=self.play_pause)
        self.t1.start()

    def play_pause(self):
        """manages playing and puasing"""
        if self.ready_to_play is False:
            self.loader()
        if self.ready_to_play is True and self.playing_state is False:
            mixer.music.unpause()
            self.slider_pressed = False
            self.playing_state = True
            self.playpausebutton.setText("▌▌")

            totaltime = self.rawsecs
            x = 0
            while self.playing_state:
                x = mixer.music.get_pos()
                time = (x/1000) + self.nulltime
                self.songtimelabel.setText(time_convert(round(time)))
                decimal = (time/totaltime)*100000
                if self.slider_pressed is False:
                    self.songtimeslider.setValue(round(decimal))
                # check if song end
                if math.ceil(time) >= math.floor(totaltime):
                    self.song_end()
                sleep(0.5)
        elif self.ready_to_play is True and self.playing_state is True:
            mixer.music.pause()
            self.playing_state = False
            self.playpausebutton.setText("►")

    def disableslider(self):
        """disables slider"""
        self.slider_pressed = True

    def changetime(self):
        """allows user to adjust time duration with time bar"""
        try:
            if self.playing_state is True:
                position = self.songtimeslider.value()
                ratio = position/100000
                newtime = ratio*self.rawsecs
                self.nulltime = newtime
                mixer.music.stop()
                mixer.music.play(start=newtime)
                self.slider_pressed = False
            else:
                pass
        except:
            # fail proof
            self.stop()

    def song_end(self):
        """handles the actions taken after song ends"""
        self.playing_state = False
        # shuffle overrides repeat
        if self.shuffle == "on":
            self.song_list = [self.list_widget.item(i).text()
                              for i in range(self.list_widget.count())]
            x = len(self.song_list)
            ran_num = random.randint(1, x)
            ran_num -= 1
            self.list_widget.setCurrentRow(ran_num)
            self.loader()
            self.playpausebutton.setText("▌▌")
            self.playing_state = True
            self.ready_to_play = True
            mixer.music.unpause()
        # repeat
        else:
            if self.repeat == "queue":
                self.playing_state = True
                self.forwards()
            elif self.repeat == "track":
                mixer.music.stop()
                mixer.music.play()
                self.playing_state = True
            else:
                mixer.music.stop()
                mixer.music.play()
                mixer.music.pause()
                self.playing_state = False
                self.songtimeslider.setValue(0)
                self.playpausebutton.setText("►")
                self.songtimelabel.setText("00:00")
        self.nulltime = 0

    def stop(self):
        """completely stops the playing song"""
        mixer.music.stop()
        mixer.music.unload()
        (self.title, self.artist, self.duration, self.file,
         self.ftype, self.fsize, self.bitrate, self.directory,
         self.rawsecs) = get_song_data("")
        self.updatelabels()
        self.fname = None
        self.playing_state = False
        self.ready_to_play = False
        self.songtimeslider.setValue(0)
        self.playpausebutton.setText("►")
        self.songtimelabel.setText("00:00")
        self.nulltime = 0

    def vol_change(self):
        """adjusts volume"""
        self.volume_level = self.volumedial.value()
        self.volumevaluelabel.setText(str(self.volume_level))
        mixer.music.set_volume(self.volume_level/100)

    def shuffle_change(self):
        """changes state of shuffle"""
        if self.shuffle == "off":
            self.shuffle = "on"
            self.shufflebutton.setText("Shuffle: On")
        elif self.shuffle == "on":
            self.shuffle = "off"
            self.shufflebutton.setText("Shuffle: Off")
        self.update_config()

    def repeat_change(self):
        """changes state of repeat"""
        if self.repeat == "off":
            self.repeat = "queue"
            self.repeatbutton.setText("Repeat: Queue")
        elif self.repeat == "queue":
            self.repeat = "track"
            self.repeatbutton.setText("Repeat: Track")
        elif self.repeat == "track":
            self.repeat = "off"
            self.repeatbutton.setText("Repeat: Off")
        self.update_config()

    def update_config(self):
        """updates config.txt"""
        write_settings(self.volume_level, self.shuffle, self.repeat)

    def update_songs(self):
        """updates queue.txt"""
        self.song_list = [self.list_widget.item(i).text()
                          for i in range(self.list_widget.count())]
        write_songs(self.song_list)

    def backwards(self):
        """moves selection backwards in queue"""
        try:
            if self.shuffle == "on":
                self.song_list = [self.list_widget.item(i).text()
                                  for i in range(self.list_widget.count())]
                x = len(self.song_list)
                ran_num = random.randint(1, x)
                ran_num -= 1
                self.list_widget.setCurrentRow(ran_num)
                self.loader()
                self.playpausebutton.setText("▌▌")
                self.playing_state = True
                self.ready_to_play = True
                mixer.music.unpause()
                return
            self.song_list = [self.list_widget.item(i).text()
                              for i in range(self.list_widget.count())]
            row = self.list_widget.currentRow()-1
            if row <= -1:
                index = len(self.song_list) - 1
                row = index
            self.list_widget.setCurrentRow(row)
            if self.playing_state is True:
                self.stop()
                self.t1.join()
                self.thread()
            elif self.playing_state is False:
                self.stop()
                self.loader()
        except:
            pass

    def forwards(self):
        """moves selection forwards in queue"""
        try:
            if self.shuffle == "on":
                self.song_list = [self.list_widget.item(i).text()
                                  for i in range(self.list_widget.count())]
                x = len(self.song_list)
                ran_num = random.randint(1, x)
                ran_num -= 1
                self.list_widget.setCurrentRow(ran_num)
                self.loader()
                self.playpausebutton.setText("▌▌")
                self.playing_state = True
                self.ready_to_play = True
                mixer.music.unpause()
                return
            self.song_list = [self.list_widget.item(i).text()
                              for i in range(self.list_widget.count())]
            row = self.list_widget.currentRow()+1
            if row >= len(self.song_list):
                row = 0
            self.list_widget.setCurrentRow(row)
            if self.playing_state is True:
                self.stop()
                self.t1.join()
                self.thread()
            elif self.playing_state is False:
                self.stop()
                self.loader()
        except:
            pass

    def remove(self):
        """removes item from queue"""
        self.stop()
        row = self.list_widget.currentRow()
        self.list_widget.takeItem(row)
        self.update_songs()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UnidentifiedPlayer = QtWidgets.QMainWindow()
    ui = Ui_UnidentifiedPlayer()
    ui.setupUi(UnidentifiedPlayer)
    UnidentifiedPlayer.show()
    sys.exit(app.exec_())
