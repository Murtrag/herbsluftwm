import os
import re
import json
import subprocess

from random import randint

# from timer import time_dec
    

_cmd = subprocess.check_output

class Battery:
    # print('test',  subprocess.check_output(['ls', '-l']) )
    dummy_bat = '''
  native-path:          BAT1
  vendor:               SDI
  model:                PA5185U-1BRS
  power supply:         yes
  updated:              Sat 26 Feb 2022 05:00:39 PM CET (33 seconds ago)
  has history:          yes
  has statistics:       yes
  battery
    present:             yes
    rechargeable:        yes
    state:               fully-charged
    warning-level:       none
    energy:              31.536 Wh
    energy-empty:        0 Wh
    energy-full:         31.536 Wh
    energy-full-design:  31.68 Wh
    energy-rate:         7.1568 W
    voltage:             14.407 V
    percentage:          100%
    capacity:            99.5455%
    technology:          lithium-ion
    icon-name:          'battery-empty-symbolic'
  History (rate):
    1645891239	7.157	fully-charged
    '''
    def __fetch_bat_data(self):
        def __split_elems(line):
            try:
                key, val = line.split(": ") 
                return {key.strip(): val.strip()}
            except ValueError:
                # This is for lines which doasn't have pair key:val like title val and a History
                return {}

        # cmd_out = Battery.dummy_bat.strip()
        # cmd_bat_file = _cmd(['upower','-e', '|', 'grep', '"BAT"']).decode('utf-8')
        try:
            cmd_bat_file = re.search('\s(.+BAT.+)\s', _cmd(['upower','-e']).decode('utf-8')).groups(1)[0]
        except AttributeError:
            cmd_bat_file = Battery.dummy_bat
        cmd_out = _cmd(['upower', '-i', cmd_bat_file]).decode('utf-8')
        cmd_split = cmd_out.split('\n')
        # cmd_to_dict = {**__split_elems(line) for line in cmd_split}
        cmd_to_dict = dict() 
        for line in cmd_split:
            cmd_to_dict.update(__split_elems(line))
        return cmd_to_dict

    def getCapacity(self):
        # bat_data = self.__fetch_bat_data()
        return self.__fetch_bat_data()['percentage'][:-1] #@TODO battery level must be a number

        # return str(randint(0,100))

    def getIconName(self):
        # ac-adapter-symbolic
        # battery-missing-symbolic
        

        # battery-empty-symbolic
        # battery-caution-symbolic

        # battery-low-symbolic v
        # battery-good-symbolic v

        # battery-full-symbolic v

        # battery-caution-charging-symbolic v

        # battery-low-charging-symbolic v
        # battery-good-charging-symbolic v

        # battery-full-charged-symbolic  V
        # battery-full-charging-symbolic v
        return self.__fetch_bat_data()['icon-name'][1:-10]

    def getTimePrediction(self):
        # pass
        try:
            return self.__fetch_bat_data()['time to empty']
        except KeyError:
            return "-----"
        # return f"{randint(0,3)}hour {randint(0,59)}min"
    

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

    def getDisksInfo(self): #getDiskInfo
        def collect_data(cmd_out_dev):
            dev_json = json.loads(cmd_out_dev)['blockdevices']
            temp = _cmd(['hddtemp'], stderr=subprocess.DEVNULL).decode('utf-8') # this takes 0.7s!!!!
            temp_split = re.split('\\n|\:', temp)

            response = list()
            
            for dev in dev_json:
                if dev['type'] == 'disk':
                    try:
                        i = temp_split.index(dev['path']) + 2 # +2 because in this list the line with the temperature is two lines further
                        temperature = re.search(
                            '(\d+)°C',
                            temp_split[i]
                        ).groups(1)[0]
                    except (AttributeError, ValueError):
                        temperature = None
                        
                    response.append({
                            'name': dev['name'] or '---',
                            'label': dev['label'] or '---',
                            'path': dev['path'],
                            'size': dev['size'],
                            'state': dev['state'],
                            'temp': temperature or '---'
                        })
            return response
            
        cmd_out_dev = _cmd(['lsblk', '-dJO'])
        out = collect_data(cmd_out_dev)

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
            'left': left,
            'right': right,
            'avg': round((left + right) / 2, 2)
        }
        return response

    @level.setter
    def level(self, value):
        # print('set brightness to: ', value)
        _cmd(['amixer', 'set', 'Master', f'{value}%'])

if '__main__' == __name__:
    # import time
    # t = AudioVol()
    # print( t.level )
    # t.level = 100

    # from pprint import pprint
    # t = SysInfo()
    # pprint(t.coresTemp())
    # pprint( t.getDisksInfo() )

    t = Battery()
    print(
        # t.getCapacity(),
        t.getIconName(),
        # t.getTimePrediction()
    )
    # uno =  time.perf_counter_ns() 
    # sys = SysInfo()
    # sys.getDisksInfo()
    # dos = time.perf_counter_ns()
    # print(dos - uno)

