function createPieChart(canvasId, data){
    var labels = [];
    var data = [];

    for (var emotion in sessionData) {
        labels.push(emotion)
        data.push(sessionData[emotion]);
    }

    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: ["blue", "red", "yellow", "orange", "pink", "purple", "green"]
            }]
        },
        options: {
            responsive: true
        },
    });
}