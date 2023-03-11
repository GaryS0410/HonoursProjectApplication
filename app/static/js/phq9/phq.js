let canvas = document.querySelector('#webcamCanvas');
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

function upload(file) {
    var formdata = new FormData();
    formdata.append('snap', file);

    fetch('/quizGet', {
        method: 'POST',
        body: formdata,
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

// document.getElementById('snap').addEventListener('click', () => {
//     takePhoto();
// })

function showNextQuestion() {
    var currentQuestion = $(".question:visible");
    var nextQuestion = currentQuestion.next(".question");

    if (nextQuestion.length) {
        console.log("Next question...")
        currentQuestion.hide();
        currentQuestion.find("input").prop("disabled", true);
        nextQuestion.show();
        nextQuestion.find("input").prop("disabled", false);
    } else {
        takePhoto();
        $(".question input").prop("disabled", false);
        document.getElementById("phq9-form").submit();
    }
}

function showPreviousQuestion() {
    var currentQuestion = $(".question:visible");
    var previousQuestion = currentQuestion.prev(".question");

    if (previousQuestion.length) {
        console.log("Previous question...")
        currentQuestion.hide();
        currentQuestion.find("input").prop("disabled", true);
        previousQuestion.show();
        previousQuestion.find("input").prop("disabled", false);
    }
}