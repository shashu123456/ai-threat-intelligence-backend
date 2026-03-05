const API="https://ai-threat-intelligence-backend.onrender.com"

function login(){

let email=document.getElementById("email").value
let password=document.getElementById("password").value

fetch(API+"/auth/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
email:email,
password:password
})

})

.then(r=>r.json())

.then(data=>{

localStorage.setItem("token",data.access_token)

window.location="index.html"

})

}

function scanURL(){

let url=document.getElementById("url").value

let token=localStorage.getItem("token")

fetch(API+"/scan/url",{

method:"POST",

headers:{
"Content-Type":"application/json",
"Authorization":"Bearer "+token
},

body:JSON.stringify({url:url})

})

.then(r=>r.json())

.then(data=>{

document.getElementById("result").innerText=

"Prediction: "+data.prediction+
"\nRisk Score: "+data.risk_score+
"\nExplanation: "+data.explanation

})

}