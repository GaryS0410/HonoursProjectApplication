let canvas = document.querySelector('#canvas');
let context = canvas.getContext('2d');
let video = document.querySelector('#video');

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        video.srcObject = stream;
        video.play();
    }).catch((err) => {
        console.log('Could not access webcam', err);
        alert("No webcam detected. Please try again with a functioning camera.");
    });
}

function upload(file){
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
}

document.getElementById('snap').addEventListener('click', () => {
    intervalId = setInterval(takePhoto, 1000); 
})

function disableStartButton() {
    document.getElementById('snap').disabled = true;
}

function enableStartButton() {
    document.getElementById('snap').disabled = false;
}

function disableStopButton() {
    document.getElementById('stop').disabled = true;
}

function enableStopButton() {
    document.getElementById('stop').disabled = false;
}

document.getElementById('snap').addEventListener('click', () => {
    intervalId = setInterval(takePhoto, 1000);
    disableStartButton();
    enableStopButton();
})

document.getElementById('stop').addEventListener('click', () => {
    clearInterval(intervalId);
    enableStartButton();
    disableStopButton();
    alert('Session Stopped');
    getPrediction();
})

disableStopButton();
enableStartButton();