// POINTS CHART
const pointsChart = new Chart(document.getElementById('pointsChart'), {
    type: 'line',
    data: {
        labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
        datasets: [{
            label: 'Points',
            data: [5,10,15,20,25,30,40],
            borderWidth: 2,
            tension: 0.4
        }]
    }
});

// CO2 CHART
const co2Chart = new Chart(document.getElementById('co2Chart'), {
    type: 'bar',
    data: {
        labels: ['Plastic','Paper','Organic','Metal'],
        datasets: [{
            label: 'CO2 Saved',
            data: [2,3,1,4],
            borderWidth: 1
        }]
    }
});