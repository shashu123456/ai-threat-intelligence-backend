async function register() {
    await fetch("/auth/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });
}

async function login() {
    let res = await fetch("/auth/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: email.value,
            password: password.value
        })
    });

    let data = await res.json();
    localStorage.setItem("token", data.access_token);
    window.location = "/dashboard";
}

async function scan() {
    let res = await fetch("/scan/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: url.value})
    });

    let data = await res.json();

    result.innerHTML = `
        Result: ${data.result} <br>
        Risk: ${data.risk_score}
    `;
}