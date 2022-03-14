import pytest
from utils import system

def test_cmd():
	''' Check if shortcut _cmd too subprocess.check_output works correctly'''
	assert callable(system._cmd)

def test_battery():
	assert 1==1


@pytest.fixture()
def battery_resource():
	battery = system.Battery()
	print("battery: setup")
	yield battery 
	print("battery: teardown ")

class TestBattery:
	def test_fetch_bat_data(self, battery_resource):
		t = battery_resource._Battery__fetch_bat_data()
		assert len(t)>0, "Battery output should not be an empty dict"
		vital_keys = {'percentage', 'icon-name'}
		assert len(vital_keys & t.keys()) == len(vital_keys), "Battery output is missing some vital keys"
		
	def test_getCappacity(self, battery_resource):
		t = battery_resource.getCapacity()
		assert type(t) is int, "Battery level must be a number"
		assert t >=0 & t <=100 , "Battery level must be in a range <0 ; 100>"

	def test_getIconName(self, battery_resource):
		possible_status = {
		"ac-adapter",
		"battery-missing",
		"battery-empty",
		"battery-caution",
		"battery-low",
		"battery-good",
		"battery-full",
		"battery-caution-charging",
		"battery-low-charging",
		"battery-good-charging",
		"battery-full-charged",
		"battery-full-charging"
		}
		t = battery_resource.getIconName()
		assert t in possible_status #@TODO apply scenarious here

	def test_getTimePrediction(self, battery_resource):
		t = battery_resource.getTimePrediction()
		assert type(t) is str #@TODO time prediction should be a datetime delta rather than str


@pytest.fixture()
def sys_info_resource():
	sys_info = system.SysInfo()
	print("SysInfo: setup")
	yield sys_info 
	print("SysInfo: teardown ")

class TestSysInfo:

    def test_getMemoryUsage(self, sys_info_resource):
        t = sys_info_resource.getMemoryUsage()
        vital_keys = {"total_memory", "used_memory", "percentage_memory", "total_swap", "used_swap"}
        assert len(t.keys() & vital_keys) == len( vital_keys)
        # Check if all values are numbers
	
    def test_getLoad(self, sys_info_resource):
        t = sys_info_resource.getLoad()
        assert len(t) == 3, "Load should contain 3 values"
        assert all(type(v) is float for v in t), "Values in load should be float type"

    def test_getDisksInfo(self, sys_info_resource):
        t = sys_info_resource.getDisksInfo()
        assert type(t) is list
	
    def test__cmd_sensors_to_dict(self, sys_info_resource):
        pass
        # t = sys_info_resource._SysInfo__cmd_sensors_to_dict()
        # assert 1==1
	
    def test_coresTemp(self, sys_info_resource):
        t = sys_info_resource.coresTemp()
        assert type(t) is dict

@pytest.fixture()
def brightness_resource():
	brightness = system.Brightness()
	print("battery: setup")
	yield brightness 
	print("battery: teardown ")

class TestBrightness:
	
    def test_level_getter(self, brightness_resource):
        brightness = brightness_resource.level
        assert type(brightness) is float, "brightness level should be type of float"
        pass

    def test_level_setter(self):
        pass

@pytest.fixture()
def audio_resource():
	audio_vol = system.AudioVol()
	print("battery: setup")
	yield audio_vol 
	print("battery: teardown ")

class TestAudioVol:
	
	def test_level_getter(self, audio_resource):
		level = audio_resource.level
		assert len({"left", "right", "avg"} & level.keys()) == len(level), "Audio vol level missing keys"
		assert all(type(v) in (int, float) for v in level.values()), "All level values should be int or float type"

	def test_level_setter(self, audio_resource):
		level = audio_resource.level
		old_val = level
		new_val = 10
		assert level['avg'] == new_val
		audio_resource.level = old_val
