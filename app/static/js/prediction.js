// var intervalId;

// async function fetchData() {
//     try {
//         const response = await fetch('/predict');
//         return response.json();
//     } catch (error) {
//         console.log('Something went wrong.')
//     }
// }

// function displayMostCommonEmotion(data) {
//     const entries = Object.entries(data.emotions_count);
//     entries.sort((a, b) => b[1] - a[1]);
//     console.log(entries[0][0]);

//     var heading = document.getElementById("mostCommon");
//     heading.innerHTML = "";
//     var currentText = "Your Most Common Emotion: ";
//     var newText = entries[0][0];
//     heading.textContent = currentText + newText;
// }

// function createPieChart(data) {
//     const emotionsCount = data.emotions_count;
//     const labels = Object.keys(emotionsCount);
//     const values = Object.values(emotionsCount);

//     var display = document.getElementById('pieChartCanvas');
//     var context = display.getContext("2d");
//     context.clearRect(0, 0, display.width, display.height);

//     var emotionsChart = new Chart(display, {
//         type: 'pie', 
//         data: {
//             labels: labels,
//             datasets: [{
//                 data: values,
//                 backgroundColor: ["blue", "red", "yellow", "orange", "pink", "purple", "green"]
//             }]
//         },
//         options: {
//             responsive: true
//         },
//     });
// }

// function displayEmotionScore(score) {
//     var heading = document.getElementById("emotionScore");
//     heading.innerHTML = "";
//     var currentText = "Your Emotion Score is: "
//     heading.textContent = currentText + score;
// }

// function getPrediction() {
//     fetchData()
//         .then(data => {
//             displayEmotionScore(data.emotional_score);
//             // displayMostCommonEmotion(data);
//             createPieChart(data);
//         });
// }

// document.getElementById('stop').addEventListener('click', () => {
//     clearInterval(intervalId);
//     getPrediction();
// })