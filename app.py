from flask import Flask, render_template, jsonify, request, session
import redis
import json
from flask_session import Session
from utils.speechtotext import WhisperVAD
import ollama
import uuid

app = Flask(__name__)

# Configuring Flask session to use Redis
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False  # Session expires when browser closes
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_KEY_PREFIX"] = "chat_"
app.config["SESSION_REDIS"] = redis.Redis(host='localhost', port=6379, decode_responses=True)

Session(app)

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

    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())  # Generate a unique ID for the session

    user_id = session['user_id']

    # Connect to Redis and retrieve conversation history
    redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
    conversation_history = redis_client.get(user_id)

    # Start new conversation
    messages = []

    # In case conversation already started
    if conversation_history:
        messages = json.loads(conversation_history)  # Convert from JSON string to Python list

    # Append new user message
    messages.append({"role": "user", "content": question_text})

    # Context memory using Flask Session
    #if 'conversation_history' not in session:   #Initialising the chat history
    #    session['conversation_history'] = []

    # Appending the user's question to the chat history
    #session['conversation_history'].append({'role':'user', 'content':question_text})


    response = ollama.chat(
        model=llm_model,
        messages=session['conversation_history'],   # Providing the past chat history to the AI for each response
        stream=False
    )

    ai_response = response['message']['content']

    # Append AI response to history
    session['conversation_history'].append({'role':'assistant', 'content':ai_response})

    messages.append({"role": "assistant", "content": ai_response})

    #Store updated history in Redis (convert list to JSON string)
    redis_client.set(user_id, json.dumps(messages))
    
    return jsonify({
        "response": ai_response
    })

if __name__ == '__main__':
    app.run(debug=True)
