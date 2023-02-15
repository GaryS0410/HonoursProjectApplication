
// var ctx = document.getElementById('pieChartCanvas{{ loop.index }}').getContext('2d');
// var sessionData = {{ session["emotions_count"] | tojson }};

// // Extract the emotion types and their count
// var labels = [];
// var data = [];

// for (var emotion in sessionData) {
//     labels.push(emotion);
//     data.push(sessionData[emotion]);
// }

// var myPieChart = new Chart(ctx, {
//     type: 'pie',
//     data: {
//         labels: labels,
//         datasets: [{
//             data: data,
//             backgroundColor: ["blue", "red", "yellow", "orange", "pink", "purple", "green"]
//         }]
//     },
//     options: {
//         responsive: true
//     },
// });

var ctx = document.getElementById(canvasId).getContext('2d');

// Extract the emotion types and their count
var labels = [];
var chartData = [];

for (var emotion in data) {
    labels.push(emotion);
    chartData.push(data[emotion]);
}

var myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            data: chartData,
            backgroundColor: ["blue", "red", "yellow", "orange", "pink", "purple", "green"]
        }]
    },
    options: {
        responsive: true
    },
});