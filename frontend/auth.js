const API = "https://ai-threat-intelligence-backend.onrender.com"

async function login(){

let email = document.getElementById("email").value
let password = document.getElementById("password").value

let status = document.getElementById("status")

status.innerHTML = "Authenticating..."

try{

let res = await fetch(API + "/auth/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body: JSON.stringify({
email:email,
password:password
})

})

let data = await res.json()

if(data.access_token){

localStorage.setItem("token",data.access_token)

status.innerHTML = "Access Granted"

setTimeout(()=>{
window.location="index.html"
},1000)

}else{

status.innerHTML = "Login Failed"

}

}catch(e){

status.innerHTML = "Server Error"

}

}