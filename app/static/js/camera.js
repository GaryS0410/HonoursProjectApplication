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
        alert('Got Photo');
        console.log(data);
    })
    .catch(error => {
        alert('Could not get photo');
        console.error(error);
    })
}

function takePhoto() {
    context.drawImage(video, 0, 0, 640, 480);
    canvas.toBlob(upload, 'image/jpeg', 0.95);
}

document.getElementById('snap').addEventListener('click', () => {
    intervalId = setInterval(takePhoto, 3000); 
})