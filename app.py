from flask import Flask, render_template, jsonify, request
from pyexpat.errors import messages
import redis
import json

from utils.speechtotext import WhisperVAD
import ollama

app = Flask(__name__)

# Connect to Redis (assuming Redis is running locally on port 6379)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

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
    llm_model = "llama3.2:1b"
    data = request.json
    question_text = data.get('question')

    # Here you would send the question to your AI model
    # For demonstration, we'll just echo it back

    """
    user_id = data
    # Retrieve user's previous messages (if any)
    conversation_history = redis_client.get(user_id)

    # Start new conversation
    messages = []

    # In case conversation already started
    if conversation_history:
        messages = json.loads(conversation_history)  # Convert from JSON string to Python list

    # Append new user message
    messages.append({"role": "user", "content": question_text})
    """

    response = ollama.chat(
        model=llm_model,
        messages={'role':'user', 'content':question_text},
        stream=False
    )

    ai_response = response['message']['content']

    # Append AI response to history
    # messages.append({"role": "assistant", "content": ai_response})

    # Store updated history in Redis (convert list to JSON string)
    # redis_client.set(user_id, json.dumps(messages))

    final_response = f"I processed your question: {ai_response}"
    
    return jsonify({
        "response": final_response
    })

if __name__ == '__main__':
    app.run(debug=True)
