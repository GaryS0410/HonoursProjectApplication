var intervalId;

function getPrediction() {
    fetch('/predict')
    .then((response) => {
        return response.json();
    })
    .then(data => {
        const entries = Object.entries(data);
        entries.sort((a, b) => b[1] - a[1]);
        console.log(entries[0][0]);        

        var x = document.createElement("H4");
        var y = document.createTextNode("Most Common Emotion: " + entries[0][0])
        x.appendChild(y);
        document.body.appendChild(x);

        const labels = Object.keys(data);
        const values = Object.values(data);

        var display = document.getElementById('pieChartCanvas');
        var emotionsChart = new Chart(display, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: ["blue", "red", "yellow", "orange", "pink", "purple", "green"],
                }]
            },
            options: {
                responsive: true
            },
        });
    })
    .catch((error) => {
        console.log('No photo could be captured.')
    })
}

document.getElementById('stop').addEventListener('click', () => {
    clearInterval(intervalId);
    alert('Session Stopped');
    getPrediction();
})