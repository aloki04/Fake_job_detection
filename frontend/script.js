console.log("Frontend JS loaded");

function scrollToDetect() {
    document.getElementById("detect").scrollIntoView({ behavior: "smooth" });
}

function checkJob() {
    const text = document.getElementById("jobText").value;

    if (text.trim() === "") {
        alert("Please enter job description");
        return;
    }

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(data => {
    document.getElementById("result").innerText =
        "Prediction: " + data.prediction;

    const confidence = data.confidence; // already percentage

    document.getElementById("confidenceValue").innerText =
        confidence + "% confidence";

    const bar = document.getElementById("confidenceBar");
    bar.style.width = confidence + "%";

    // Optional color based on result
    if (data.prediction === "Fake Job") {
        bar.style.background = "linear-gradient(90deg, #ff4d4d, #ff9800)";
    } else {
        bar.style.background = "linear-gradient(90deg, #4caf50, #2e7d32)";
    }
})


    .catch(err => {
        alert("Backend not reachable");
        console.error(err);
    });
}
