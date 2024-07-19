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
    document.getElementById("initialPrediction").innerText = result.initial_prediction;
    document.getElementById("llamaCategory").innerText = result.llama_category;
    document.getElementById("llamaExplanation").innerText = result.llama_explanation;
}

function rate(rating) {
    document.getElementById("userRating").value = rating;
    const stars = document.querySelectorAll(".rating .fa-star");
    stars.forEach((star, index) => {
        star.classList.toggle("selected", index < rating);
    });
}

async function submitInteraction() {
    const textInput = document.getElementById("textInput").value;
    const initialPrediction = document.getElementById("initialPrediction").innerText;
    const llamaCategory = document.getElementById("llamaCategory").innerText;
    const llamaExplanation = document.getElementById("llamaExplanation").innerText;
    const userRating = document.getElementById("userRating").value;

    const data = {
        text: textInput,
        initial_prediction: initialPrediction,
        llama_category: llamaCategory,
        llama_explanation: llamaExplanation,
        user_rating: parseInt(userRating),
    };

    // display the data in the console
    console.log(data);

    const response = await fetch("/submit_interaction", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    alert("Thank you for your feedback!");
}

