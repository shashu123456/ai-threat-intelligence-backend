async function register(){

let email=document.getElementById("email").value
let password=document.getElementById("password").value

let res=await fetch("/auth/register",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({email,password})

})

let data=await res.json()

alert(data.message)

window.location="/login"

}


async function login(){

let email=document.getElementById("email").value
let password=document.getElementById("password").value

let res=await fetch("/auth/login",{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({email,password})

})

let data=await res.json()

if(data.token){

localStorage.setItem("token",data.token)

window.location="/dashboard"

}else{

alert("Invalid login")

}

}