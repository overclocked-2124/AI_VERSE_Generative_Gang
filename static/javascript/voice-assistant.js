document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('mic-button');
    const conversation = document.getElementById('conversation');
    const loadingSpinner = document.getElementById('loading-spinner');
    const clearButton = document.getElementById('clear-button');
    
    let isListening = false;
    let pollInterval;
    
    // Handle mic button click
    micButton.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent form submission
        
        if (!isListening) {
            // Start listening
            loadingSpinner.style.display = 'inline-block';
            micButton.textContent = '🛑 Stop Listening';
            
            try {
                const response = await fetch('/start_listening', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    isListening = true;
                    // Start polling for questions
                    pollInterval = setInterval(checkForQuestions, 500);
                } else {
                    console.error('Failed to start listening');
                    resetUI();
                }
            } catch (error) {
                console.error('Error starting listening:', error);
                resetUI();
            }
        } else {
            // Stop listening
            try {
                const response = await fetch('/stop_listening', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                if (response.ok) {
                    clearInterval(pollInterval);
                    resetUI();
                } else {
                    console.error('Failed to stop listening');
                }
            } catch (error) {
                console.error('Error stopping listening:', error);
            }
        }
    });
    
    // Function to check for new questions
    async function checkForQuestions() {
        try {
            const response = await fetch('/check_for_questions');
            
            if (response.ok) {
                const data = await response.json();
                
                if (data.has_questions) {
                    // Process each question
                    for (const question of data.questions) {
                        displayUserQuestion(question.text);
                        await processQuestion(question.text);
                    }
                }
            }
        } catch (error) {
            console.error('Error checking for questions:', error);
        }
    }
    
    // Function to display user's question
    function displayUserQuestion(text) {
        const userMessage = document.createElement('p');
        userMessage.innerHTML = `<strong>You:</strong> ${text}`;
        conversation.appendChild(userMessage);
        conversation.scrollTop = conversation.scrollHeight;
    }
    
    // Function to process a question with the AI
    async function processQuestion(questionText) {
        try {
            const response = await fetch('/process_question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ question: questionText })
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Display AI response
                const aiMessage = document.createElement('p');
                aiMessage.innerHTML = `<strong>AI:</strong> ${data.response}`;
                conversation.appendChild(aiMessage);
                conversation.scrollTop = conversation.scrollHeight;
            }
        } catch (error) {
            console.error('Error processing question:', error);
        }
    }
    
    // Function to reset UI
    function resetUI() {
        loadingSpinner.style.display = 'none';
        micButton.textContent = '🎤 Speak';
        isListening = false;
    }
    
    // Handle clear button click
    clearButton.addEventListener('click', (event) => {
        event.preventDefault();
        conversation.innerHTML = '';
    });
});
