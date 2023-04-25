import json
import pprint
import artdaq
from PyQt5.QtCore import QThread, QDateTime
from artdaq.constants import AcquisitionType
pp = pprint.PrettyPrinter(indent=4)
import numpy as np

# 导入requests包
import requests


# data = {"name": "plusroax", "age": 18}  # Post请求发送的数据，字典格式



class AI_Acquisition():
    def __init__(self):
        # self.headers = {'content-type': 'application/json'}
        # self.url = "http://127.0.0.1:5000/selectAll"
        # url="49.234.121.115"
        # self.url = f"http://{url}:8888/selectAll"
        self.rate=10000
        self.sample_mode = AcquisitionType.CONTINUOUS
        self.origin_json={}
        self.mean_json={}
        self.data = []
        self.data1 = []
        self.channel1 = []
        self.channel2 = []
        self.channel3 = []
        self.channel4 = []
        self.channel5 = []
        self.channel6 = []
        self.channel7 = []
        self.channel8 = []
        self.channel9 = []
        self.channel10 = []
        self.channel11 = []
        self.channel12 = []
        self.channel13 = []
        self.channel14 = []
        self.channel15 = []
        self.channel16 = []
        self.channel1_datas = []
        self.channel2_datas = []
        self.channel3_datas = []
        self.channel4_datas = []
        self.channel5_datas = []
        self.channel6_datas = []
        self.channel7_datas = []
        self.channel8_datas = []
        self.channel9_datas = []
        self.channel10_datas = []
        self.channel11_datas = []
        self.channel12_datas = []
        self.channel13_datas = []
        self.channel14_datas = []
        self.channel15_datas = []
        self.channel16_datas = []
        self.filename = QDateTime.currentDateTime().toString( "yyyy年MM月dd日hh时mm分ss秒zzz毫秒" )

    def start_run(self):
        with artdaq.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0:15")
            task.timing.cfg_samp_clk_timing(
                self.rate, sample_mode=self.sample_mode, samps_per_chan=self.rate)
            data = task.read( number_of_samples_per_channel=10000 )
            self.data=data
            self.deal_data( data )
        return self.data
            # for _ in range(2):
            #     data = task.read(number_of_samples_per_channel=10000)
            #     self.deal_data(data)
            #     print('Task Data: ')
            #     pp.pprint(data)

    def deal_data(self,save_data):
        #一秒10k原始电压信号数据
        self.channel1.extend(save_data[0])
        self.channel2.extend( save_data[1] )
        self.channel3.extend( save_data[2] )
        self.channel4.extend( save_data[3] )
        self.channel5.extend( save_data[4] )
        self.channel6.extend( save_data[5] )
        self.channel7.extend( save_data[6] )
        self.channel8.extend( save_data[7] )
        self.channel9.extend( save_data[8] )
        self.channel10.extend( save_data[9] )
        self.channel10.extend( save_data[10] )
        self.channel12.extend( save_data[11] )
        self.channel13.extend(save_data[12])
        self.channel14.extend( save_data[13] )
        self.channel15.extend( save_data[14] )
        self.channel16.extend( save_data[15] )

        #原始数据求均值10k求一个均值
        self.channel1_datas.append(np.mean(save_data[0]))
        self.channel2_datas.append( np.mean( save_data[1] ) )
        self.channel3_datas.append( np.mean( save_data[2] ) )
        self.channel4_datas.append( np.mean( save_data[3] ) )
        self.channel5_datas.append( np.mean( save_data[4] ) )
        self.channel6_datas.append( np.mean( save_data[5] ) )
        self.channel7_datas.append( np.mean( save_data[6] ) )
        self.channel8_datas.append( np.mean( save_data[7] ) )
        self.channel9_datas.append( np.mean( save_data[8] ) )
        self.channel10_datas.append( np.mean( save_data[9] ) )
        self.channel11_datas.append( np.mean( save_data[10] ) )
        self.channel12_datas.append(np.mean(save_data[11]))
        self.channel13_datas.append( np.mean( save_data[12] ) )
        self.channel14_datas.append( np.mean( save_data[13] ) )
        self.channel15_datas.append( np.mean( save_data[14] ) )
        self.channel16_datas.append(np.mean(save_data[15]))

    def save_txtdata(self):
        origin_filename = "../data/original_data/"+self.filename + "_artdata.txt"

        mean_filename = "../data/mean_data/"+self.filename + "_artdata.txt"
        with open( str( mean_filename ), "a", newline="" ) as f:
            f.write("channel1:")
            f.writelines([str( x ) for x in self.channel1_datas])
            f.write( '\n' )
            f.write( "channel2:" )
            f.writelines( [str( x ) for x in self.channel2_datas] )
            f.write( '\n' )
            f.write( "channel3:" )
            f.writelines( [str( x ) for x in self.channel3_datas] )
            f.write( '\n' )
            f.write( "channel4:" )
            f.writelines( [str( x ) for x in self.channel4_datas] )
            f.write( '\n' )
            f.write( "channel5:" )
            f.writelines([str( x ) for x in self.channel5_datas] )
            f.write( '\n' )
            f.write( "channel6:" )
            f.writelines( [str( x ) for x in self.channel6_datas])
            f.write( '\n' )
            f.write( "channel7:" )
            f.writelines( [str( x ) for x in self.channel7_datas] )
            f.write( '\n' )
            f.write( "channel8:" )
            f.writelines( [str( x ) for x in self.channel8_datas] )
            f.write( '\n' )
            f.write( "channel9:" )
            f.writelines( [str( x ) for x in self.channel9_datas] )
            f.write( '\n' )
            f.write( "channel10:" )
            f.writelines( [str( x ) for x in self.channel10_datas] )
            f.write( '\n' )
            f.write( "channel11:" )
            f.writelines( [str( x ) for x in self.channel11_datas] )
            f.write( '\n' )
            f.write( "channel12:" )
            f.writelines([str( x ) for x in self.channel12_datas] )
            f.write( '\n' )
            f.write( "channel13:" )
            f.writelines( [str( x ) for x in self.channel13_datas] )
            f.write( '\n' )
            f.write( "channel14:" )
            f.writelines( [str( x ) for x in self.channel14_datas] )
            f.write( '\n' )
            f.write( "channel15:" )
            f.writelines( [str( x ) for x in self.channel15_datas] )
            f.write( '\n' )
            f.write( "channel15:" )
            f.writelines( [str( x ) for x in self.channel16_datas] )
            f.write( '\n' )
            f.close()
        with open( str( origin_filename ), "a", newline="" ) as f:
            f.write("channel1:")
            f.writelines([str( x ) for x in self.channel1])
            f.write( '\n' )
            f.write( "channel2:" )
            f.writelines( [str( x ) for x in self.channel2] )
            f.write( '\n' )
            f.write( "channel3:" )
            f.writelines( [str( x ) for x in self.channel3] )
            f.write( '\n' )
            f.write( "channel4:" )
            f.writelines( [str( x ) for x in self.channel4] )
            f.write( '\n' )
            f.write( "channel5:" )
            f.writelines([str( x ) for x in self.channel5] )
            f.write( '\n' )
            f.write( "channel6:" )
            f.writelines( [str( x ) for x in self.channel6])
            f.write( '\n' )
            f.write( "channel7:" )
            f.writelines( [str( x ) for x in self.channel7] )
            f.write( '\n' )
            f.write( "channel8:" )
            f.writelines( [str( x ) for x in self.channel8] )
            f.write( '\n' )
            f.write( "channel9:" )
            f.writelines( [str( x ) for x in self.channel9] )
            f.write( '\n' )
            f.write( "channel10:" )
            f.writelines( [str( x ) for x in self.channel10] )
            f.write( '\n' )
            f.write( "channel11:" )
            f.writelines( [str( x ) for x in self.channel11] )
            f.write( '\n' )
            f.write( "channel12:" )
            f.writelines([str( x ) for x in self.channel12] )
            f.write( '\n' )
            f.write( "channel13:" )
            f.writelines( [str( x ) for x in self.channel13] )
            f.write( '\n' )
            f.write( "channel14:" )
            f.writelines( [str( x ) for x in self.channel14] )
            f.write( '\n' )
            f.write( "channel15:" )
            f.writelines( [str( x ) for x in self.channel15] )
            f.write( '\n' )
            f.write( "channel15:" )
            f.writelines( [str( x ) for x in self.channel16] )
            f.write( '\n' )
            f.close()
    # def save_jsondata(self):
        # origin_filename = "../data/original_data/"+self.filename + "_artdata.json"
        # mean_filename = "../data/mean_data/"+self.filename + "_artdata.json"
        # self.origin_json = {"channel1":self.channel1,
        #                     "channel2": self.channel2,
        #                     "channel3": self.channel3,
        #                     "channel4": self.channel4,
        #                     "channel5": self.channel5,
        #                     "channel6": self.channel6,
        #                     "channel7": self.channel7,
        #                     "channel8": self.channel8,
        #                     "channel9": self.channel9,
        #                     "channel10": self.channel10,
        #                     "channel11": self.channel11,
        #                     "channel12": self.channel12,
        #                     "channel13": self.channel13,
        #                     "channel14": self.channel14,
        #                     "channel15": self.channel15,
        #                     "channel16": self.channel16
        #                     }
        # self.mean_json = {"channel1": self.channel1_datas,
        #                     "channel2": self.channel2_datas,
        #                     "channel3": self.channel3_datas,
        #                     "channel4": self.channel4_datas,
        #                     "channel5": self.channel5_datas,
        #                     "channel6": self.channel6_datas,
        #                     "channel7": self.channel7_datas,
        #                     "channel8": self.channel8_datas,
        #                     "channel9": self.channel9_datas,
        #                     "channel10": self.channel10_datas,
        #                     "channel11": self.channel11_datas,
        #                     "channel12": self.channel12_datas,
        #                     "channel13": self.channel13_datas,
        #                     "channel14": self.channel14_datas,
        #                     "channel15": self.channel15_datas,
        #                     "channel16": self.channel16_datas
        #                     }
        # with open( origin_filename, 'w' ) as fp:
        #     json.dump(self.origin_json, fp)
        # with open( mean_filename, 'w' ) as fp:
        #     json.dump(self.mean_json, fp)
        # self.send_data(self.mean_json)

    def send_data(self):

        res = requests.post( url=self.url, data=json.dumps( self.mean_json ),
                             headers=self.headers )  # 这里传入的data,是body里面的数据。params是拼接url时的参数
        print(res.text)

if __name__ == '__main__':
    art_ai=AI_Acquisition()
    art_ai.start_run()
    art_ai.save_jsondata()