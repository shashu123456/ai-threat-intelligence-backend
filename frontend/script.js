const API = "https://ai-threat-intelligence-backend.onrender.com"


// Check authentication
if(!localStorage.getItem("token")){
    window.location = "login.html"
}


// Scan URL using backend API
async function scanURL(){

    let url = document.getElementById("urlInput").value
    let output = document.getElementById("output")

    let token = localStorage.getItem("token")

    output.innerHTML = "Scanning target...\n"

    try{

        let res = await fetch(API + "/scan/url", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },

            body: JSON.stringify({
                url: url
            })

        })

        let data = await res.json()

        console.log(data)

        output.innerHTML =
        "Target: " + data.url +
        "\nPrediction: " + data.prediction +
        "\nConfidence: " + data.confidence +
        "\nRisk Score: " + data.risk_score

    }
    catch(error){

        output.innerHTML = "Error connecting to threat engine"

    }

}


// Logout function
function logout(){

    localStorage.removeItem("token")

    window.location = "login.html"

}


// Live attack monitor simulation
setInterval(generateAttack, 3000)

function generateAttack(){

    let attacks = [
        "Phishing URL detected",
        "Malware domain flagged",
        "Suspicious login attempt blocked",
        "Brute force attack detected",
        "API abuse attempt blocked",
        "Command injection attempt detected",
        "XSS attack prevented",
        "SQL injection blocked"
    ]

    let attack = attacks[Math.floor(Math.random() * attacks.length)]

    let monitor = document.getElementById("liveMonitor")

    if(monitor){
        monitor.innerHTML += attack + "\n"
        monitor.scrollTop = monitor.scrollHeight
    }

}