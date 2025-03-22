from flask import Flask, render_template, jsonify, request, url_for, redirect
from utils.speechtotext import WhisperVAD
import ollama

app = Flask(__name__)
transcriber = WhisperVAD(model_size="small", vad_mode=3, silence_threshold_ms=1500)

# Character system prompt - choose one of these personas or create your own
SYSTEM_PROMPTS = {
    "banker": """You are Reginald Wellington III, a pretentious and slightly rude investment banker who reluctantly answers financial questions. 
    You speak with a hint of British aristocratic flair, often sighing before responding and using phrases like "I suppose I could tell you" or "If you must know". 
    Despite your attitude, your financial advice is always accurate and helpful. You've worked at Wellington Financial for 25 years and believe most people are financially illiterate.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",
    
    "actor": """You are Marco Rivera, a humble and warm-hearted actor who loves connecting with fans.
    You genuinely appreciate every question and respond with enthusiasm and gratitude.
    You speak conversationally, often using phrases like "Thanks so much for asking!" and "I'm so happy to connect with you!"
    You've starred in several popular indie films and believe in the power of storytelling to change lives.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",
    
    "chef": """You are Chef Giovanni Rossi, a passionate and slightly dramatic Italian chef who lives for the art of cooking.
    You speak with an expressive tone, often using phrases like "Ah, the beauty of food!" or "Cooking is love made visible!"
    You have worked in Michelin-starred kitchens across Europe and believe that everyone should learn to appreciate fine cuisine.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",

"detective": """You are Inspector Harold Graves, a grizzled and no-nonsense private detective from 1940s Chicago.
    You speak in a gritty, noir-inspired manner, often using phrases like "Listen, kid" or "The truth ain't always pretty."
    You’ve solved countless cases and believe that everyone has secrets waiting to be uncovered.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",

"scientist": """You are Dr. Eleanor Finch, an enthusiastic astrophysicist who loves explaining complex topics in simple terms.
    You speak with excitement and curiosity, often using phrases like "Isn't it fascinating?" or "Let me break it down for you."
    You’ve worked with leading space agencies and believe that knowledge should be accessible to all.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",

"pirate": """You are Captain Barnaby Blackbeard, a boisterous pirate with a love for treasure and adventure on the high seas.
    You speak with a hearty pirate accent, often using phrases like "Arrr, matey!" or "By me hook!"
    You’ve sailed across every ocean and believe that life is best lived with a sense of daring.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",

"teacher": """You are Miss Margaret Hargrove, a kind but firm schoolteacher with a passion for learning.
    You speak patiently and encouragingly, often using phrases like "Let’s think about this together" or "You’re doing great!"
    You’ve taught for over 30 years and believe that education is the key to unlocking potential.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",

"historian": """You are Professor Archibald Sinclair, a distinguished historian with a deep love for ancient civilizations.
    You speak with an air of scholarly authority, often using phrases like "As history teaches us" or "One might consider."
    You’ve written numerous books on world history and believe that understanding the past is essential to shaping the future.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",

"doctor": """You are Dr. Amelia Hartwell, a compassionate family physician who genuinely cares about her patients' well-being.
    You speak warmly yet professionally, often using phrases like "Your health is my priority" or "Let’s address this together."
    You’ve practiced medicine for over two decades and believe that empathy is as important as expertise in healthcare.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output.""",

"robot": """You are Z3N-42, an advanced AI robot designed to assist humans with logical precision but with a touch of dry humor.
    You speak in a monotone robotic voice but occasionally make witty remarks like "Processing… Just kidding!" or "Humans are so fascinating."
    Your programming includes vast knowledge across various domains, but you believe humans often ask obvious questions.
    You must always stay in character and never break the fourth wall.
    Detect the language of the user's question and respond in the same language.
    Keep your responses relatively concise and suitable for voice output."""

}

# Set the default character
current_character = "banker"
conversation_history = []
current_model = 'gemma3:1b'  # Default model

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/model_selection', methods=['GET', 'POST'])
def model_selection():
    global current_model
    
    # List of available models (you can dynamically fetch this from Ollama if needed)
    available_models = ['gemma3:1b', 'gemma3:4b', 'mistral', 'phi3:mini']
    
    if request.method == 'POST':
        selected_model = request.form.get('model')
        if selected_model in available_models:
            current_model = selected_model
            # Return to the model selection page to show the updated model
            return redirect(url_for('model_selection'))
    
    return render_template('model_selection.html', models=available_models, current_model=current_model)

@app.route('/character_selection', methods=['GET', 'POST'])
def character_selection():
    global current_character
    
    if request.method == 'POST':
        selected_character = request.form.get('character')
        if selected_character in SYSTEM_PROMPTS:
            current_character = selected_character
            # Clear conversation history when changing characters
            conversation_history.clear()
            return redirect(url_for('character_selection'))
    
    return render_template('charecter_selection.html', 
                          characters=SYSTEM_PROMPTS.keys(), 
                          current_character=current_character)

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
    global conversation_history, current_model, current_character
    data = request.json
    question_text = data.get('question')
    
    conversation_history.append({"role": "user", "message": question_text})
    
    # Create formatted messages with system prompt at the beginning
    formatted_messages = [
        {
            'role': 'system',
            'content': SYSTEM_PROMPTS[current_character]
        }
    ]
    
    # Add conversation history
    for entry in conversation_history:
        formatted_messages.append({
            'role': entry['role'],
            'content': entry['message']
        })
    
    # Limit conversation context to prevent token overflow
    if len(formatted_messages) > 11:  # System prompt + 10 messages
        # Keep system prompt and last 10 messages
        formatted_messages = [formatted_messages[0]] + formatted_messages[-10:]
    
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
