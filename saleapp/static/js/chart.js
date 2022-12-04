function drawCateStats(labels, data, color) {
 const ctx = document.getElementById('myChart');

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: labels,
      datasets: [{
        label: 'Số lượng',
        data: data,
        backgroundColor: color,
        borderColor: color,
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

function drawRevenueStats(labels, data) {
const ctx = document.getElementById('revenueStats');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Doanh thu',
        data: data,
        borderWidth: 1,
        backgroundColor: ['red', 'green', 'blue', 'gold', 'rgba(135, 156, 150, 0.7)']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}