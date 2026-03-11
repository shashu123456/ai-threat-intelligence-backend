async function scanURL() {

    let url = document.getElementById("urlInput").value

    let response = await fetch("/scan", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: url})
    })

    let data = await response.json()

    document.getElementById("result").innerHTML =
        "Prediction: " + data.prediction +
        "<br>Confidence: " + data.confidence +
        "<br>Risk Score: " + data.risk_score

    addFeed(url, data)
}

function addFeed(url, data) {

    let list = document.getElementById("feedList")

    let item = document.createElement("li")

    item.innerText =
        url + " → " + data.prediction + " (risk " + data.risk_score + ")"

    list.prepend(item)
}

async function loadStats(){

    let response = await fetch("/analytics/stats")

    let data = await response.json()

    const ctx = document.getElementById('statsChart')

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Total','Phishing','Safe'],
            datasets: [{
                label: 'Threat Stats',
                data: [data.total_scans,data.phishing,data.safe]
            }]
        }
    })
}

loadStats()