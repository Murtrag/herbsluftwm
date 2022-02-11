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

# Serve static files
@app.route('/js/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

# Main page
@app.route('/')
def hello_world():
    system = SysInfo()
    battery = Battery()
    audio = AudioVol()
    brightness = Brightness()
    context = {
        "battery": {
            "cap": battery.getCapacity(),
            "prediction": battery.getTimePrediction()
            },
        "memory": system.getMemoryUsage(),
        "load": system.getLoad(),
        "brightness": brightness.level,
        "audio": audio.level
    }
    return render_template('index.html', **context)

# APIs
# Dashboard
@app.route('/stats', methods=['GET', 'POST'])
def get_stats():
    query = request.get_json().get('query')
    return stat_chain.handle(query)
    # print(flask.request.values) #.get('user')

# Brightness
@app.route('/brightness', methods=['PUT'])
def change_brightness():
    print(request.get_json().get('brightness'))
    brightness = Brightness()
    brightness.level = request.get_json().get('brightness')
    return {'brightness': brightness.level}

# Audio volume
@app.route('/audio', methods=['PUT'])
def change_audio_vol():
    print(request.get_json().get('audio'))
    audio = AudioVol()
    audio.level = request.get_json().get('audio')
    return {'audio': audio.level}
