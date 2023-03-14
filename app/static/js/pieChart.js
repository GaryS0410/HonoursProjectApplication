function createPieChart(canvasId, data){
    var labels = [];
    var data = [];


    var emotion_colours = {
        "angry": "red",
        "disgust": "green",
        "fear": "black",
        "happy": "yellow",
        "sad": "blue",
        "surprise": "pink",
        "neutral": "orange"
    }

    for (var emotion in sessionData) {
        labels.push(emotion)
        data.push(sessionData[emotion]);
    }

    var label_colours  = labels.map(label => emotion_colours[label]);

    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: label_colours
            }]
        },
        options: {
            responsive: true,
            legend: {
                labels: {
                    fontColor: '#c7c6cd'
                }
            }
        },
    });
}