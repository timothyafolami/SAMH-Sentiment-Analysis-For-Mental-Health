async function predictSentiment() {
    const textInput = document.getElementById("textInput").value;
    const response = await fetch("/predict_sentiment", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: textInput })
    });
    const result = await response.json();
    const outputDiv = document.getElementById("output");
    outputDiv.innerHTML = `Prediction: ${result.prediction}`;
}
