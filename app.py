from flask import Flask, render_template,jsonify
from utils.speechtotext import WhisperTranscriber 

app = Flask(__name__)
transcriber = WhisperTranscriber()
transcription_results = []


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


def transcription_callback(text, language):
    transcription_results.append({"text": text, "language": language})

@app.route('/start_transcription', methods=['POST'])
def start_transcription():
    global transcription_results
    transcription_results = []
    success = transcriber.start(callback=transcription_callback)
    return jsonify({"success": success, "status": "started" if success else "already running"})

@app.route('/stop_transcription', methods=['POST'])
def stop_transcription():
    success = transcriber.stop()
    return jsonify({
        "success": success, 
        "status": "stopped" if success else "not running",
        "results": transcription_results
    })

@app.route('/get_transcription', methods=['GET'])
def get_transcription():
    return jsonify({"results": transcription_results, "is_running": transcriber.running})

if __name__ == '__main__':
    app.run(debug=True)