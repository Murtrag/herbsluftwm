from flask import (
    Flask,
    request,
    render_template,
    send_from_directory
)

from utils.system import (
    Battery,
    SysInfo,
    Brightness,
    AudioVol
)
from utils.dashboard_validation import stat_chain

app = Flask(__name__)

system = SysInfo()
battery = Battery()
audio = AudioVol()
brightness = Brightness()

# Serve static files
@app.route('/js/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Main page
@app.route('/')
def main():
# bgcolor=$(hc get frame_border_normal_color|sed 's,^\(\#[0-9a-f]\{6\}\)[0-9a-f]\{2\}$,\1,')
# selbg=$(hc get window_border_active_color|sed 's,^\(\#[0-9a-f]\{6\}\)[0-9a-f]\{2\}$,\1,')
# selfg='#101010'
    context = {
        "panel":{
            "bgcolor": "green",
            "selbg": "orange",
            "selfg": "blue"
        },
        "battery": {
            "cap": battery.getCapacity(),
            "prediction": battery.getTimePrediction()
            },
        "memory": system.getMemoryUsage(),
        "load": system.getLoad(),
        "brightness": brightness.level,
        "audio": audio.level,
        "hdds": system.getDisksInfo() 
    }
    return render_template('index.html', **context)

# APIs
# Dashboard
@app.route('/stats', methods=['POST'])
def get_stats():
    query = request.get_json().get('query')
    # print("query: ", query)
    return stat_chain.handle(query)
    # print(flask.request.values) #.get('user')

# Brightness
@app.route('/brightness', methods=['PUT'])
def change_brightness():
    # print(request.get_json().get('brightness'))
    brightness = Brightness()
    brightness.level = request.get_json().get('brightness')
    return {'brightness': brightness.level}

# Audio volume
@app.route('/audio', methods=['PUT'])
def change_audio_vol():
    # print(request.get_json().get('audio'))
    audio = AudioVol()
    audio.level = request.get_json().get('audio')
    return {'audio': audio.level}
