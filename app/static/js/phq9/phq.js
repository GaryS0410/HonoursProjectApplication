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

function fetchData() {
    return fetch('/quizPredict')
        .then((response) => {
            console.log(response);
            return response.json();
        })
        .then((data) => {
            let resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '';
            for (const [emotion, count] of Object.entries(data.emotions_count)) {
                let p = document.createElement('p');
                p.innerHTML = "Emotion: " + emotion + " Instances of emotion: " + count;
                resultDiv.appendChild(p);
            }
        })
        .catch((error) => {
            console.log('Something went wrong.')
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

document.getElementById('snap').addEventListener('click', () => {
    takePhoto();
})

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
        $(".question input").prop("disabled", false);
        fetchData();
    }
}