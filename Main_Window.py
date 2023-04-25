import json
import sys

import requests
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, QDateTime
from art_source.ai_voltage import AI_Acquisition
from art_source.Di_Art import DI_Acquisition
from uisource.MainUi1 import Ui_mainWindow
import pyqtgraph as pg
import pandas as pd
import numpy as np

class MainWindow(QtWidgets.QMainWindow,Ui_mainWindow):
    def __init__(self):
        #初始化
        super( MainWindow, self ).__init__()
        self.headers = {'content-type': 'application/json'}
        url = "49.234.121.115"
        self.url = f"http://{url}:5000/add_data"
        self.send_data={}
        self.filename = QDateTime.currentDateTime().toString( "yyyy年MM月dd日hh时mm分ss秒zzz毫秒" )

        self.savedata=[]
        self.savedata_mean = []
        self.art_Ai=AI_Acquisition()
        self.art_Di=DI_Acquisition()
        self.timer = QTimer()
        self.timer.timeout.connect(self.start_measure)
        self.timer1 = QTimer()
        self.timer1.timeout.connect( self.start_listening )
        self.unit=''
        self.k = '1'
        self.b = '0'
        self.channel=[0]
        self.equipment='挖掘机'
        self.sensor1='压力传感器'
        self.channel_data=[]
        self.setupUi(self)
        self.plot_init()
        self.radioButton_Analog.setChecked(True)
        self.config_ana()
        self.radioButton_Analog.toggled.connect(self.config_ana)
        self.radioButton_Digital.toggled.connect( self.config_digital )
        self.sensor.textChanged.connect(self.config_unit)
        self.lineEdit_k.textChanged.connect( self.config_k )
        self.lineEdit_b.textChanged.connect( self.config_b )
        self.lineEdit_IP.textChanged.connect(self.config_Ip)
        self.lineEdit_frequency.textChanged.connect(self.config_speed)
        # self.comboBox.currentIndexChanged.connect(self.config_channel)
        self.comboBox.activated.connect( self.config_channel )
        self.comboBox_jixing.activated.connect( self.choose_equipment )
        self.comboBox_sensor.activated.connect( self.chooes_sensor )
        self.pushButton_start.clicked.connect(self.start)
        self.pushButton_stop.clicked.connect( self.stop_measure )
        self.pushButton_clear.clicked.connect( self.clear_measure )
        self.pushButton_save.clicked.connect( self.save_data )
        self.pushButton_listening.clicked.connect( self.start_send )
    def plot_init(self):
        self.plot_plt = pg.PlotWidget()  # 实例化一个绘图部件

        self.plot_plt.showGrid( x=True, y=True )  # 显示图形网格
        # self.plot_plt.setYRange( max=6, min=-6 )
        # self.plot_plt.plot(  )
        self.verticalLayout_4.addWidget(self.plot_plt)
    def config_ana(self):
        self.comboBox.setEnabled(True)
        self.sensor.setEnabled(True)
        self.lineEdit_k.setEnabled(True)
        self.lineEdit_b.setEnabled(True)
        self.textBrowser_port0.setEnabled(False)
        self.textBrowser_port1.setEnabled(False)
    def config_digital(self):
        self.comboBox.setEnabled(False)
        self.sensor.setEnabled(False)
        self.lineEdit_k.setEnabled(False)
        self.lineEdit_b.setEnabled(False)
        self.textBrowser_port0.setEnabled(True)
        self.textBrowser_port1.setEnabled(True)
    def config_unit(self):
        self.unit=self.sensor.text()
        print( self.unit )
        self.label_11.setText('y('+self.unit+')='+self.k+'x'+'+'+self.b)
    def config_k(self):
        self.k1=self.lineEdit_k.text()
        self.k=self.k1
        print( self.k )
        self.label_11.setText( 'y(' + self.unit + ')=' + self.k +'x' + '+'+self.b )
    def config_b(self):
        self.b=self.lineEdit_b.text()
        print( self.b )
        self.label_11.setText( 'y(' + self.unit + ')=' + self.k +'x' +'+'+ self.b )
    def config_channel(self):
        # print(self.comboBox.currentText())
        self.channel=list(self.comboBox.currentText())
        print(self.channel)
        print(  type(self.channel[-1] ) )

    def choose_equipment(self):
        print( self.comboBox_jixing.currentText() )
        self.equipment=self.comboBox_jixing.currentText()
    def chooes_sensor(self):
        print( self.comboBox_sensor.currentText() )
        self.sensor1=self.comboBox_sensor.currentText()
    def config_Ip(self):
        self.url=f"http://{self.lineEdit_IP.text()}:5000/selectAll"
    def config_speed(self):
        self.art_Ai.rate=self.lineEdit_frequency.text()
    def start(self):
        self.timer.start( 1000 )
    def start_measure(self):
        if (self.radioButton_Analog.isChecked()):
            self.plot_plt.clear()
            list=self.art_Ai.start_run()

            mylist=list[int(self.channel[-1])]

            print(mylist)
            self.channel_data=(pd.Series(mylist)*float(self.k)+float(self.b)).tolist()
            # self.channel_data=(pd.Series(self.channel_data[self.channel[-1]])*self.k).tolist()

            print(self.channel_data)
            self.plot_plt.plot( self.channel_data, pen='r' )
            self.savedata.extend( self.channel_data )
            self.savedata_mean.append(np.mean(self.channel_data))

        if(self.radioButton_Digital.isChecked()):
            di_data=self.art_Di.get_data()
            # di_data1=di_data[0:6]
            # di_data2=di_data[7:10]
            # print("di_data1=",di_data1,"di_data2=",di_data2)
            self.textBrowser_port0.append('line0:'+str(di_data[0]))
            self.textBrowser_port0.append( 'line1:' + str( di_data[1] ) )
            self.textBrowser_port0.append( 'line2:' + str( di_data[2] ) )
            self.textBrowser_port0.append( 'line3:' + str( di_data[3] ) )
            self.textBrowser_port0.append( 'line4:' + str( di_data[4] ) )
            self.textBrowser_port0.append( 'line5:' + str( di_data[5] ) )
            self.textBrowser_port0.append( 'line6:' + str( di_data[6] ) )
            self.textBrowser_port1.append( 'line0:' + str( di_data[7] ) )
            self.textBrowser_port1.append( 'line1:' + str( di_data[8] ) )
            self.textBrowser_port1.append( 'line2:' + str( di_data[9] ) )
            self.textBrowser_port1.append( 'line3:' + str( di_data[10] ) )

    def stop_measure(self):
        self.timer.stop()
    def clear_measure(self):
        self.timer.stop()
        self.plot_plt.clear()
    def save_data(self):
        # self.art_di.save_jsondata()
        origin_filename = "data/original_data/" + self.filename + "_artdata.json"
        mean_filename = "data/mean_data/" + self.filename + "_artdata.json"
        self.origin_json = {'time':QDateTime.currentDateTime().toString( "yyyy年MM月dd日hh时mm分ss秒zzz毫秒" ),
                        "equipment":self.equipment,
                        "sensor":self.sensor1,
                        "data":self.savedata}
        self.mean_json = {'time':QDateTime.currentDateTime().toString( "yyyy年MM月dd日hh时mm分ss秒zzz毫秒" ),
                        "equipment":self.equipment,
                        "sensor":self.sensor1,
                        "data":self.savedata_mean}
        with open( origin_filename, 'w' ) as fp:
            json.dump( self.origin_json, fp )
        with open( mean_filename, 'w' ) as fp:
            json.dump( self.mean_json, fp )
    def start_send(self):
        self.timer1.start(1000)
    def start_listening(self):
        # print(1111)
        # self.send_data={'time':QDateTime.currentDateTime().toString( "yyyy年MM月dd日hh时mm分ss秒zzz毫秒" ),
        #                 "equipment":self.equipment,
        #                 "sensor":self.sensor1,
        #                 "data":np.mean(self.channel_data)}
        self.send_data = {'time': QDateTime.currentDateTime().toString( "yyyy年MM月dd日hh时mm分ss秒zzz毫秒" ),
                                          "equipment":self.equipment,
                                          "sensor":self.sensor1,
                                          "data":3.1415926}
        res = requests.post( url=self.url, data=json.dumps( self.send_data ),
                             headers=self.headers )  # 这里传入的data,是body里面的数据。params是拼接url时的参数
        print( res.text )



if __name__ == '__main__':
    app = QtWidgets.QApplication( sys.argv )
    gui = MainWindow()
    gui.show()
    sys.exit( app.exec_() )