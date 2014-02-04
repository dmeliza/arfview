from PySide import QtGui, QtCore
import pyqtgraph.dockarea as pgd
import pyqtgraph as pg

class settingsPanel(QtGui.QWidget):
    def __init__(self):
        super(settingsPanel, self).__init__()
        self.initUI()

    def initUI(self):
        
        layout = QtGui.QVBoxLayout()
        self.oscillogram_check=QtGui.QCheckBox("Oscillogram")
        self.oscillogram_check.setCheckState(QtCore.Qt.CheckState.Checked)
        self.raster_check=QtGui.QCheckBox("Raster")
        self.raster_check.setCheckState(QtCore.Qt.CheckState.Checked)
        self.label_check=QtGui.QCheckBox("Label")
        self.label_check.setCheckState(QtCore.Qt.CheckState.Checked)
        self.psth_check=QtGui.QCheckBox("PSTH")
        self.psth_bin_size = QtGui.QLineEdit('10')
        self.isi_check=QtGui.QCheckBox("ISI")
        self.isi_bin_size = QtGui.QLineEdit('10')
        self.spectrogram_check=QtGui.QCheckBox("Spectrogram")
        self.spectrogram_box = self.create_spectrogram_box()

        psth_settings_layout = QtGui.QHBoxLayout()
        psth_settings_layout.addWidget(self.psth_check)
        psth_settings_layout.addWidget(QtGui.QLabel("Bin Size: "))
        self.psth_bin_size.setMaximumWidth(50)
        psth_settings_layout.addWidget(self.psth_bin_size)
        psth_settings_layout.addWidget(QtGui.QLabel('ms'))
        psth_settings_layout.addStretch()
        psth_settings_layout.setContentsMargins(0,0,0,0)
        
        isi_settings_layout = QtGui.QHBoxLayout()
        isi_settings_layout.addWidget(self.isi_check)
        isi_settings_layout.addSpacing(18)
        isi_settings_layout.addWidget(QtGui.QLabel("Bin Size: "))
        self.isi_bin_size.setMaximumWidth(50)
        isi_settings_layout.addWidget(self.isi_bin_size)
        isi_settings_layout.addWidget(QtGui.QLabel('ms'))
        isi_settings_layout.addStretch()
        isi_settings_layout.setContentsMargins(0,0,0,0)
        
        layout.addWidget(self.oscillogram_check)
        layout.addWidget(self.raster_check)
        layout.addWidget(self.label_check)
        layout.addLayout(psth_settings_layout)
        layout.addLayout(isi_settings_layout)
        layout.addWidget(self.spectrogram_check)
        layout.addWidget(self.spectrogram_box)
        layout.addStretch()

        self.setLayout(layout)
        

    def create_spectrogram_box(self):
        self.spectrogram_check.setCheckState(QtCore.Qt.CheckState.Checked)
        self.win_size = QtGui.QLineEdit("256")
        self.step = QtGui.QLineEdit("1")
        self.window = QtGui.QComboBox()
        self.window.addItem("Hann")
        self.window.addItem("Bartlett")
        self.window.addItem("Blackman")
        self.window.addItem("Boxcar")
        self.window.addItem("Hamming")
        self.window.addItem("Parzen")
        group_box = QtGui.QGroupBox("Spectrogram Settings")
        layout = QtGui.QGridLayout()
        ledge = 0
        uedge = 0
        layout.addWidget(QtGui.QLabel("Window Size:"), uedge, ledge)
        layout.addWidget(self.win_size, uedge, ledge+1)
        layout.addWidget(QtGui.QLabel("samples"), uedge, ledge+2)
        layout.addWidget(QtGui.QLabel("Time Step:"), uedge+1, ledge)
        layout.addWidget(self.step, uedge+1, ledge+1)
        layout.addWidget(QtGui.QLabel("ms"), uedge+1, ledge+2)
        layout.addWidget(QtGui.QLabel("Window"), uedge+2, ledge)
        layout.addWidget(self.window, uedge+2, ledge+1)
        #layout.setContentsMargins(0,0,50,0)
        layout.setColumnStretch(1,30)
        group_box.setLayout(layout)
    
        return group_box
