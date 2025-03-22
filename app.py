from flask import Flask, render_template, jsonify, request,url_for,redirect
from utils.speechtotext import WhisperVAD
import ollama

app = Flask(__name__)
transcriber = WhisperVAD(model_size="small", vad_mode=3, silence_threshold_ms=1500)


conversation_history = []
# You can change to any model you have pulled: llama2, mistral, etc.
current_model = 'gemma3:1b'  # Default model


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/aiselect')
def aiselect():
    global current_model
    
    # List of available models (you can dynamically fetch this from Ollama if needed)
    available_models = ['gemma3:1b', 'llama2', 'mistral', 'phi3:mini']
    
    if request.method == 'POST':
        selected_model = request.form.get('model')
        if selected_model in available_models:
            current_model = selected_model
            return redirect(url_for('voiceassistant'))
    
    return render_template('aiselect.html', models=available_models, current_model=current_model)

@app.route('/custommodel')
def custommodel():
    return render_template('custommodel.html')

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

@app.route('/process_question', methods=['POST'])
def process_question():
    global conversation_history, current_model
    data = request.json
    question_text = data.get('question')
    
    
    conversation_history.append({"role": "user", "message": question_text})
    
    
    formatted_messages = []
    for entry in conversation_history:
        formatted_messages.append({
            'role': entry['role'],
            'content': entry['message']
        })
    
    
    if len(formatted_messages) > 10:
        formatted_messages = formatted_messages[-10:]
    
    try:
        
        response = ollama.chat(
            model=current_model,  
            messages=formatted_messages
        )
        
        
        ai_response = response['message']['content']
        
    except Exception as e:
        ai_response = f"Error processing request: {str(e)}"
    
    
    conversation_history.append({"role": "assistant", "message": ai_response})
    
    
    if len(conversation_history) > 20:
        conversation_history = conversation_history[-20:]
    
    return jsonify({"response": ai_response})


if __name__ == '__main__':
    app.run(debug=True)
