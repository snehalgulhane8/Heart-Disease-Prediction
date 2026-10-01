const API_URL = "http://127.0.0.1:8000";

const form = document.getElementById("predictionForm");

const loading = document.getElementById("loading");

const result = document.getElementById("result");

const resultIcon = document.getElementById("resultIcon");

const resultTitle = document.getElementById("resultTitle");

const resultMessage = document.getElementById("resultMessage");

const probability = document.getElementById("probability");

const predictButton = document.getElementById("predictButton");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    result.classList.add("hidden");

    loading.classList.remove("hidden");

    predictButton.disabled = true;


    // Get values from form

    const data = {

        age: Number(
            document.getElementById("age").value
        ),

        sex: Number(
            document.getElementById("sex").value
        ),

        cp: Number(
            document.getElementById("cp").value
        ),

        trestbps: Number(
            document.getElementById("trestbps").value
        ),

        chol: Number(
            document.getElementById("chol").value
        ),

        fbs: Number(
            document.getElementById("fbs").value
        ),

        restecg: Number(
            document.getElementById("restecg").value
        ),

        thalach: Number(
            document.getElementById("thalach").value
        ),

        exang: Number(
            document.getElementById("exang").value
        ),

        oldpeak: Number(
            document.getElementById("oldpeak").value
        ),

        slope: Number(
            document.getElementById("slope").value
        )

    };


    try {

        const response = await fetch(
            `${API_URL}/predict`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        if (!response.ok) {

            throw new Error(
                "Server returned an error"
            );

        }


        const prediction =
            await response.json();


        console.log(
            "Prediction:",
            prediction
        );


        if (prediction.error) {

            throw new Error(
                prediction.error
            );

        }


        // Hide loading

        loading.classList.add("hidden");

        result.classList.remove("hidden");


        // Show result

        if (
            prediction.prediction === 1 ||
            prediction.result === "Higher Risk"
        ) {

            resultIcon.textContent = "⚠️";

            resultTitle.textContent =
                "Higher Risk Detected";

            resultTitle.style.color =
                "#e63946";

            resultMessage.textContent =
                "The model indicates a higher likelihood of heart disease.";

        }

        else {

            resultIcon.textContent = "✅";

            resultTitle.textContent =
                "Lower Risk Detected";

            resultTitle.style.color =
                "#16a34a";

            resultMessage.textContent =
                "The model indicates a lower likelihood of heart disease.";

        }


        probability.textContent =
            `${prediction.probability}%`;


        // Scroll to result

        result.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    }

    catch (error) {

        console.error(error);

        loading.classList.add("hidden");

        result.classList.remove("hidden");

        resultIcon.textContent = "❌";

        resultTitle.textContent =
            "Connection Error";

        resultTitle.style.color =
            "#e63946";

        resultMessage.textContent =
            "Unable to connect to the prediction server. Make sure FastAPI is running.";

        probability.textContent = "--";

    }


    predictButton.disabled = false;

});


function resetPrediction() {

    form.reset();

    result.classList.add("hidden");

    window.scrollTo({
        top: document.getElementById("prediction").offsetTop,
        behavior: "smooth"
    });

}