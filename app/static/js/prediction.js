var intervalId;

function fetchData(){
    return fetch('/predict')
        .then((response) => {
            return response.json();
        })
        .catch((error) => {
            console.log('Something went wrong.')
        });
}

function displayMostCommonEmotion(data) {
    const entries = Object.entries(data);
    entries.sort((a, b) => b[1] - a[1]);
    console.log(entries[0][0]);

    var heading = document.getElementById("mostCommon");
    var currentText = heading.textContent;
    var newText = entries[0][0];
    heading.textContent = currentText + newText;
}

function createPieChart(data) {
    const labels = Object.keys(data);
    const values = Object.values(data);

    var display = document.getElementById('pieChartCanvas');
    var context = display.getContext("2d");
    context.clearRect(0, 0, display.width, display.height);

    if(typeof emotionsChart !== 'undefined') {
        emotionsChart.destory();
    }
    
    var emotionsChart = new Chart(display, {
        type: 'pie', 
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ["blue", "red", "yellow", "orange", "pink", "purple", "green"]
            }]
        },
        options: {
            responsive: true
        },
    });
}

function getPrediction() {
    fetchData()
        .then(data => {
            displayMostCommonEmotion(data);
            createPieChart(data);
        });
}

document.getElementById('stop').addEventListener('click', () => {
    clearInterval(intervalId);
    alert('Session Stopped');
    getPrediction();
})