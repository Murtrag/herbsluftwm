import os
import re
import json
import subprocess

from random import randint


_cmd = subprocess.check_output

class Battery:
    # print('test',  subprocess.check_output(['ls', '-l']) )
    def getCapacity(self):
        return str(randint(0,100))

    def getIconName(self):
        pass

    def getTimePrediction(self):
        return f"{randint(0,3)}hour {randint(0,59)}min"
    

class SysInfo:
    # def __init__(self):
    #   self._cmd = subprocess.check_output

    def getMemoryUsage(self, unit="m") -> dict:  
        cmd_out = str(_cmd(['free',f'-{unit}']))
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

    def getDiskInfo(self): #getDiskInfo
        def collect_data(cmd_out_dev):
            dev_json = json.loads(cmd_out_dev)['blockdevices']
            temp = _cmd(['hddtemp']).decode('utf-8')
            temp_split = re.split('\\n|\:', temp)

            response = list()
            
            for dev in dev_json:
                if dev['type'] == 'disk':
                    try:
                        i = temp_split.index(dev['path']) + 2 # +2 because in this list the line with the temperature is two lines further
                        temperature = re.search(
                            '(\d)°C',
                            temp_split[i]
                        ).groups(1)[0]
                    except (AttributeError, ValueError):
                        temperature = None
                        
                    response.append({
                            'name': dev['name'],
                            'label': dev['label'],
                            'path': dev['path'],
                            'size': dev['size'],
                            'state': dev['state'],
                            'temp': temperature
                        })
            return response
            
        cmd_out_dev = _cmd(['lsblk', '-dJO'])
        out = collect_data(cmd_out_dev)

        # compare with temperatures and display all of them with No Reading if no sensor
        return out

    def __cmd_sensors_to_dict(self, cmd_out):
        def get_temp(line):
            return re.search('\+(\d{1,2})', line).groups(1)[0]
            
        cmd_list = str(cmd_out).split('\\n')
        dict_out = {}
        last_key = str()
        for line in cmd_list:
            if "Adapter:" in line:
                last_key = line[9:]
                dict_out[last_key] = {'sensor': [], 'package':[]}
            if "Package" in line:
                dict_out[last_key]['package'].append(get_temp(line))
                continue
            if "\\xc2\\xb0C" in line: # °C 
                dict_out[last_key]['sensor'].append(get_temp(line))
        return dict_out
            
        

    def coresTemp(self):
    # sensors
        cmd_out = _cmd(['sensors'])
        return self.__cmd_sensors_to_dict(cmd_out)

class Brightness:
    # def __init__(self):
    #     self._cmd = self._cmd = subprocess.check_output

    @property
    def level(self):
        try:
            return float(str(_cmd(['xbacklight', '-get']))[2:-3] )
        except ValueError: #If the device doasn't support this func the command returns None so I can't cast it to float
            return 100.0


    @level.setter
    def level(self, value):
        _cmd(['xbacklight', '-set', value])

class AudioVol:
    # def __init__(self):
    #     self._cmd = self._cmd = subprocess.check_output

    def __strip_level(self, text):
        return int(re.search('(\d+)%', text).group(1))

    @property
    def level(self):

        cmd_out = _cmd(['amixer', 'sget', 'Master'])
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
        # print('set brightness to: ', value)
        _cmd(['amixer', 'set', 'Master', f'{value}%'])

if '__main__' == __name__:
    # t = AudioVol()
    # print( t.level )
    # t.level = 100

    from pprint import pprint
    t = SysInfo()
    # pprint(t.coresTemp())
    pprint( t.getDiskInfo() )


