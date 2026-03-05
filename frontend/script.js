const API = "https://ai-threat-intelligence-backend.onrender.com";

function login() {

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    fetch(API + "/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(res => res.json())
    .then(data => {

        if(data.access_token){

            localStorage.setItem("token", data.access_token);

            window.location.href = "index.html";

        } else {

            document.getElementById("login_status").innerText = "Login Failed";

        }

    });

}


function scanURL(){

    const url = document.getElementById("url").value;

    const token = localStorage.getItem("token");

    document.getElementById("result").innerText = "Scanning target...";

    fetch(API + "/scan/url", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },

        body: JSON.stringify({
            url: url
        })

    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("result").innerText =
        `
Target: ${data.url}

Prediction: ${data.prediction}

Confidence: ${data.confidence}

Risk Score: ${data.risk_score}
        `;

    })
    .catch(err => {

        document.getElementById("result").innerText =
        "Error connecting to threat engine";

    });

}


function logout(){

localStorage.removeItem("token");

window.location.href="login.html";

}