async function checkNews() {
    const text = document.getElementById('text-input').value;
    const resultDiv = document.getElementById('result');
    const resultText = document.getElementById('result-text');
    const resultIcon = document.getElementById('result-icon');
    const confidenceLevel = document.getElementById('confidence-level');
    const confidenceValue = document.getElementById('confidence-value');

    if (!text.trim()) {
        alert('Please enter text to analyze!');
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) throw new Error('Server error');

        const data = await response.json();
        
        resultDiv.classList.remove('hidden');
        resultDiv.classList.add('visible');
        
        const isFake = data.prediction === 'FAKE';
        const confidence = (data.probability * 100).toFixed(1);
        
        // Aktualizacja wyglądu
        resultText.textContent = isFake ? 'FAKE NEWS DETECTED' : 'REAL NEWS VERIFIED';
        resultText.style.color = isFake ? '#dc2626' : '#16a34a';
        resultIcon.innerHTML = isFake ? '❌ FAKE' : '✅ REAL';
        
        // Animacja paska pewności
        confidenceLevel.style.width = `${confidence}%`;
        confidenceLevel.style.backgroundColor = isFake ? '#dc2626' : '#16a34a';
        confidenceValue.textContent = `${confidence}%`;
        
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during analysis. Please try again.');
    }
}
