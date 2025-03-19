document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('mic-button');
    const conversation = document.getElementById('conversation');
    const loadingSpinner = document.getElementById('loading-spinner');
    const clearButton = document.getElementById('clear-button');
    
    let isListening = false;
    let resultCheckInterval;

    // Function to start transcription
    async function startTranscription() {
        try {
            loadingSpinner.style.display = 'inline-block';
            micButton.textContent = '🛑 Stop Listening';
            
            const response = await fetch('/start_transcription', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                isListening = true;
                
                // Start polling for results
                resultCheckInterval = setInterval(checkForResults, 2000); // Check every 2 seconds
            } else {
                console.error('Failed to start transcription');
                resetUI();
            }
        } catch (error) {
            console.error('Error starting transcription:', error);
            resetUI();
        }
    }
    
    // Function to stop transcription
    async function stopTranscription() {
        try {
            clearInterval(resultCheckInterval);
            
            const response = await fetch('/stop_transcription', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                displayResults(data.results);
            } else {
                console.error('Failed to stop transcription');
            }
            
            resetUI();
        } catch (error) {
            console.error('Error stopping transcription:', error);
            resetUI();
        }
    }
    
    // Function to check for new transcription results
    async function checkForResults() {
        try {
            const response = await fetch('/get_transcription');
            
            if (response.ok) {
                const data = await response.json();
                
                // If we have results, display them
                if (data.results.length > 0) {
                    displayResults(data.results);
                }
                
                // If transcription has stopped on the server side
                if (!data.is_running && isListening) {
                    clearInterval(resultCheckInterval);
                    resetUI();
                }
            }
        } catch (error) {
            console.error('Error checking for results:', error);
        }
    }
    
    // Function to display transcription results
    function displayResults(results) {
        // Clear existing content if needed
        // conversation.innerHTML = '';
        
        // Display each result
        results.forEach(result => {
            // Check if this result is already displayed to avoid duplicates
            const resultText = result.text.trim();
            if (resultText && !isResultAlreadyDisplayed(resultText)) {
                const userMessage = document.createElement('p');
                userMessage.innerHTML = `<strong>You:</strong> ${resultText}`;
                conversation.appendChild(userMessage);
                
                // Simulate AI response (replace with actual AI response logic)
                const aiResponse = `I heard you say something in ${result.language}. How can I help with that?`;
                const aiMessage = document.createElement('p');
                aiMessage.innerHTML = `<strong>AI:</strong> ${aiResponse}`;
                conversation.appendChild(aiMessage);
                
                // Scroll to the bottom of the conversation
                conversation.scrollTop = conversation.scrollHeight;
            }
        });
    }
    
    // Helper function to check if a result is already displayed
    function isResultAlreadyDisplayed(text) {
        const paragraphs = conversation.querySelectorAll('p');
        for (let p of paragraphs) {
            if (p.textContent.includes(text)) {
                return true;
            }
        }
        return false;
    }
    
    // Function to reset UI elements
    function resetUI() {
        loadingSpinner.style.display = 'none';
        micButton.textContent = '🎤 Speak';
        isListening = false;
    }
    
    // Handle mic button click
    micButton.addEventListener('click', async (event) => {
        event.preventDefault(); // Prevent form submission
        
        if (!isListening) {
            await startTranscription();
        } else {
            await stopTranscription();
        }
    });
    
    // Handle clear button click
    clearButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent form submission
        conversation.innerHTML = ''; // Clear the conversation display
    });
});
