from flask import Flask, render_template, jsonify, request
from utils.speechtotext import WhisperVAD
import ollama

app = Flask(__name__)
transcriber = WhisperVAD(model_size="small", vad_mode=3, silence_threshold_ms=1500)

# Global variable to store the conversation history
conversation_history = []

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
    return jsonify({"success": success, "status": "stopped" if success else "not running"})

@app.route('/check_for_questions', methods=['GET'])
def check_for_questions():
    results = transcriber.get_transcription_results()
    return jsonify({
        "has_questions": len(results) > 0,
        "questions": results
    })

@app.route('/process_question', methods=['POST'])  # Added route decorator here
def process_question():
    global conversation_history
    data = request.json
    question_text = data.get('question')
    
    # Append user question to conversation history
    conversation_history.append({"role": "user", "message": question_text})
    
    # Format conversation history for Ollama (which expects "content" instead of "message")
    formatted_messages = []
    for entry in conversation_history:
        formatted_messages.append({
            'role': entry['role'],
            'content': entry['message']
        })
    
    # Keep only the last 10 messages for Ollama (maintaining history depth of 10)
    if len(formatted_messages) > 10:
        formatted_messages = formatted_messages[-10:]
    
    try:
        # Process with Ollama
        response = ollama.chat(
            model='gemma3:4b',  # You can change to any model you have pulled: llama2, mistral, etc.
            messages=formatted_messages
        )
        
        # Extract the AI response
        ai_response = response['message']['content']
        
    except Exception as e:
        ai_response = f"Error processing request: {str(e)}"
    
    # Append the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "message": ai_response})
    
    # Keep conversation history manageable (optional additional limit)
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
    
    return jsonify({"response": ai_response})

if __name__ == '__main__':
    app.run(debug=True)
