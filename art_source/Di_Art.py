import artdaq
import pprint

from artdaq.constants import (
    LineGrouping)
class DI_Acquisition():
    def __init__(self):
        self.data1=[]
        self.data0=[]
    def get_data(self):
        with artdaq.Task() as task:
            task.di_channels.add_di_chan( 'Dev1/port0/line0:6', line_grouping=LineGrouping.CHAN_PER_LINE )
            self.data0 = task.read()
        with artdaq.Task( 'a' ) as self.task1:
            self.task1.di_channels.add_di_chan( 'Dev1/port1/line0:3', line_grouping=LineGrouping.CHAN_PER_LINE )
            self.data1 = self.task1.read()
        print(self.data0+self.data1)
        return self.data0+self.data1

if __name__ == '__main__':
    di=DI_Acquisition()
    di.get_data()