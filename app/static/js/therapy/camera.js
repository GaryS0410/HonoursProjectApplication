let canvas = document.querySelector('#canvas');
let context = canvas.getContext('2d');
let video = document.querySelector('#video');

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
}

document.getElementById('snap').addEventListener('click', () => {
    intervalId = setInterval(takePhoto, 1000); 
})

function disableButtons() {
    document.getElementById('snap').disabled = true;
    document.getElementById('stop').disabled = true;
}

function enableButtons() {
    document.getElementById('snap').disabled = false;
    document.getElementById('stop').disabled = false;
}