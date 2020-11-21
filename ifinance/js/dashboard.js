/* globals Chart:false, feather:false */

(function () {
  'use strict'

  feather.replace()

  // Graphs
  var ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [
        'Jun/18',
        'Jul/18',
        'Ago/18',
        'Set/18',
        'Out/18',
        'Nov/18',
        'Dez/18',
        'Jan/19',
        'Fev/19',
        'Mar/19',
        'Abr/19',
        'Mai/19',
        'Jun/19',
        'Jul/19',
        'Ago/19',
        'Set/19',
        'Out/19',
        'Nov/19',
        'Dez/19',
        'Jan/20',
        'Fev/20',
        'Mar/20',
        'Abr/20',
        'Mai/20',
        'Jun/20',
        'Jul/20',
        'Ago/20',
        'Set/20'
      ],
      datasets: [{
        data: [
          0,
          1063.81,
          1495.17,
          1495.17,
          1495.17,
          4682.89,
          6832.12,
          6247.38,
          6980.69,
          8891.50,
          8023.56,
          7131.82,
          8805.52,
          14869.09,
          23538.44,
          37224.97,
          49015.16,
          55065.15,
          51892.15,
          51461.16,
          49083.04,
          35297.25,
          40274.37,
          45573.41,
          67535.49,
          94810.31,
          88088.73,
          89143.12
        ],
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#5cb85c',
        borderWidth: 4,
        pointBackgroundColor: '#5cb85c'
      }]
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: false
          }
        }]
      },
      legend: {
        display: false
      }
    }
  })
}())