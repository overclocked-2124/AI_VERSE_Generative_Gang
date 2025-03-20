from flask import Flask, render_template, jsonify, request
from utils.speechtotext import WhisperVAD

app = Flask(__name__)
transcriber = WhisperVAD(model_size="small", vad_mode=3, silence_threshold_ms=1500)

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/voiceassistant')
def voiceassistant():
    return render_template('voice-assistant.html')

@app.route('/start_listening', methods=['POST'])
def start_listening():
    success = transcriber.start()
    return jsonify({"success": success, "status": "started" if success else "already running"})

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    success = transcriber.stop()
    return jsonify({
        "success": success, 
        "status": "stopped" if success else "not running"
    })

@app.route('/check_for_questions', methods=['GET'])
def check_for_questions():
    results = transcriber.get_transcription_results()
    return jsonify({
        "has_questions": len(results) > 0,
        "questions": results
    })

@app.route('/process_question', methods=['POST'])
def process_question():
    data = request.json
    question_text = data.get('question')
    
    # Here you would send the question to your AI model
    # For demonstration, we'll just echo it back
    ai_response = f"I processed your question: {question_text}"
    
    return jsonify({
        "response": ai_response
    })

if __name__ == '__main__':
    app.run(debug=True)
