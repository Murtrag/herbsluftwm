import os
import re
import subprocess

from random import randint

class Battery:
    # print('test',  subprocess.check_output(['ls', '-l']) )
    def getCapacity(self):
        return str(randint(0,100))

    def getIconName(self):
        pass

    def getTimePrediction(self):
        return f"{randint(0,3)}hour {randint(0,59)}min"
    

class SysInfo:
    def __init__(self):
        self._cmd = subprocess.check_output

    def getMemoryUsage(self, unit="m") -> dict:  
        cmd_out = str(self._cmd(['free',f'-{unit}']))
        cmd_sort = re.findall('\d+', cmd_out)
        return {
                'total_memory': cmd_sort[0],
                'used_memory': cmd_sort[1],
                'percentage_memory': f"{round(int(cmd_sort[0]) / int(cmd_sort[1]), 3)}%",
                # 'free_memory': cmd_sort[2],
                'total_swap': cmd_sort[6],
                'used_swap': cmd_sort[7],
                }

#     def getDiskUssage(self):
#         pass
    def getLoad(self):
        return os.getloadavg()

class Brightness:
    def __init__(self):
        self._cmd = self._cmd = subprocess.check_output

    @property
    def level(self):
        self._cmd(['xbacklight', '-get'])

    @level.setter
    def level(self, value):
        print('set brightness to: ', value)
        return self._cmd(['xbacklight', '-set', value])


