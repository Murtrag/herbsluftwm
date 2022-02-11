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
        try:
            return float(str(self._cmd(['xbacklight', '-get']))[2:-3] )
        except ValueError: #If the device doasn't support this func the command returns None so I can't cast it to float
            return 100.0


    @level.setter
    def level(self, value):
        self._cmd(['xbacklight', '-set', value])

class AudioVol:
    def __init__(self):
        self._cmd = self._cmd = subprocess.check_output

    def __strip_level(self, text):
        return int(re.search('(\d+)%', text).group(1))

    @property
    def level(self):

        cmd_out = self._cmd(['amixer', 'sget', 'Master'])
        left_out, right_out = str(cmd_out).split('\\n')[-3:-1]

        left = self.__strip_level(left_out)
        right = self.__strip_level(right_out)

        response = {
            'left': re.search('(\d+)%', left_out).group(1),
            'right': re.search('(\d+)%', right_out).group(1),
            'avg': round((left + right) / 2, 2)
        }
        return response

    @level.setter
    def level(self, value):
        print('set brightness to: ', value)
        self._cmd(['amixer', 'set', 'Master', f'{value}%'])

if '__main__' == __name__:
    t = AudioVol()
    # print( t.level )
    # t.level = 100


