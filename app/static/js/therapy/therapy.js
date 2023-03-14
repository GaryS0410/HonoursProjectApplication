let canvas = document.querySelector('#canvas');
let context = canvas.getContext('2d');
let video = document.querySelector('#video');
var intervalId;

// Time stuff
let sessionDuration = 0;

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        enableButtons()
        video.srcObject = stream;
        video.play();
    }).catch((err) => {
        console.log('Could not access webcam', err);
        disableButtons()
        video.textContent = "Please make sure your camera is functional and the browser has access to"
        alert("No webcam detected. Please try again with a functioning camera.");
    });
}

function upload(file) {
    var formdata = new FormData();
    formdata.append('snap', file);

    fetch('/startSession', {
        method: 'POST',
        body: formdata
    })
    .then(response => response.blob())
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error(error);
    })
}

function takePhoto() {
    context.drawImage(video, 0, 0, 640, 480);
    canvas.toBlob(upload, 'image/jpeg', 0.95);

    if (sessionDuration > 0 && new Date().getTime() - sessionStartTime >= sessionDuration) {
        clearInterval(intervalId);
        getPrediction();
    }
}

document.getElementById('snap').addEventListener('click', () => {
    intervalId = setInterval(takePhoto, 2000);
    sessionStartTime = new Date().getTime();
})

function disableButtons() {
    document.getElementById('snap').disabled = true;
    document.getElementById('stop').disabled = true;
}

function enableButtons() {
    document.getElementById('snap').disabled = false;
    document.getElementById('stop').disabled = false;
}

async function fetchData() {
    try {
        const response = await fetch('/predict');
        return response.json();
    } catch (error) {
        console.log('Something went wrong.')
    }
}

function displayMostCommonEmotion(data) {
    const entries = Object.entries(data.emotions_count);
    entries.sort((a, b) => b[1] - a[1]);
    console.log(entries[0][0]);

    var heading = document.getElementById("mostCommon");
    heading.innerHTML = "";
    var currentText = "Your Most Common Emotion: ";
    var newText = entries[0][0];
    heading.textContent = currentText + newText;
}

function createPieChart(data) {
    const emotionsCount = data.emotions_count;
    const labels = Object.keys(emotionsCount);
    const values = Object.values(emotionsCount);

    var emotion_colours = {
        "angry": "red",
        "disgust": "green",
        "fear": "black",
        "happy": "yellow",
        "sad": "blue",
        "surprise": "pink",
        "neutral": "orange"
    }

    var label_colours = labels.map(label => emotion_colours[label]);

    var display = document.getElementById('pieChartCanvas');
    var context = display.getContext("2d");
    context.clearRect(0, 0, display.width, display.height);

    var emotionsChart = new Chart(display, {
        type: 'pie', 
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: label_colours
            }]
        },
        options: {
            responsive: true
        },
    });
}

function displayEmotionScore(score) {
    var heading = document.getElementById("emotionScore");
    heading.innerHTML = "";
    var currentText = "Your Emotion Score is: "
    heading.textContent = currentText + score;
}

function getPrediction() {
    fetchData()
        .then(data => {
            displayEmotionScore(data.emotional_score);
            createPieChart(data);
        });
}

document.getElementById('stop').addEventListener('click', () => {
    clearInterval(intervalId);
    getPrediction();
})

document.getElementById('sessionLengthDropdown').addEventListener('click', (event) => {
    sessionDuration = parseInt(event.target.getAttribute('value'));
})

