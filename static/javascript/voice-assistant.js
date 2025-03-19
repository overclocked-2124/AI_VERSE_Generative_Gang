document.addEventListener('DOMContentLoaded', () => {
    const micButton = document.getElementById('mic-button');
    const conversation = document.getElementById('conversation');
    const loadingSpinner = document.getElementById('loading-spinner');

    micButton.addEventListener('click', () => {
        loadingSpinner.style.display = 'inline-block'; // Show loading spinner
        micButton.textContent = '🎤 Listening...';

        // Simulate voice recognition start
        setTimeout(() => {
            // Simulate transcription
            const userSpeech = "Hello, how can you assist me today?";
            const aiResponse = "I can help you with various tasks like setting reminders, answering questions, and more.";
            
            // Display conversation
            conversation.innerHTML += `<p><strong>You:</strong> ${userSpeech}</p>`;
            conversation.innerHTML += `<p><strong>AI:</strong> ${aiResponse}</p>`;
            
            // Reset button text and hide loading spinner
            micButton.textContent = '🎤 Speak';
            loadingSpinner.style.display = 'none'; // Hide loading spinner
        }, 2000);
    });

    // Clear conversation button functionality
    document.getElementById('clear-button').addEventListener('click', () => {
        conversation.innerHTML = ''; // Clear the conversation display
    });
});
