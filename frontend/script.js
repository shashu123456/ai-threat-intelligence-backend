const API = "https://ai-threat-intelligence-backend.onrender.com"

async function scanURL(){

let url = document.getElementById("urlInput").value
let output = document.getElementById("output")

output.innerHTML = "Scanning target...\n"

try{

let res = await fetch(API + "/scan/url",{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body: JSON.stringify({
url:url
})
})

let data = await res.json()

console.log(data)

output.innerHTML =
"Target: " + url +
"\nPrediction: " + data.prediction +
"\nConfidence: " + data.confidence +
"\nRisk Score: " + data.risk_score

}
catch(err){

output.innerHTML =
"Connection Failed\nBackend API not reachable"

}

}