let canvas = document.querySelector('#canvas');
let context = canvas.getContext('2d');
let video = document.querySelector('#video');

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true }).then((stream) => {
        video.srcObject = stream;
        video.play();
    })
}

function upload(file){
    var formdata = new FormData();
    formdata.append('snap', file);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/saveImage', true);
    xhr.onload = function() {
        if (this.status == 200) {
            console.log(this.response);
        } else {
            console.error(xhr);
        }
        alert(this.response);
    };
    xhr.send(formdata);
}

function takePhoto() {
    context.drawImage(video, 0, 0, 640, 480)
    canvas.toBlob(upload, 'image/jpeg')
}

document.getElementById('snap').addEventListener('click', () => {
    setInterval(takePhoto, 1500)
})