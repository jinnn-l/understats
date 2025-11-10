const groupLabels = JSON.parse(document.getElementById('group-labels').textContent);
const dataLabels = JSON.parse(document.getElementById('data-labels').textContent);
const data = JSON.parse(document.getElementById('data').textContent);
const numberOfDatasets = dataLabels.length;

var colours = interpolateColors(numberOfDatasets);

let dataset = [];
for (let i = 0; i < numberOfDatasets; i++) {
  dataset.push({
    label: groupLabels[i],
    backgroundColor: colours[i],
    borderColor: colours[i],
    borderWidth: 1,
    outlierColor: '#999999',
    padding: 10,
    itemRadius: 0,
    data: data
  })
};

const boxplotData = {
  labels: groupLabels,
  datasets: dataset,
};

window.onload = () => {
  const ctx = document.getElementById("canvas").getContext("2d");
  window.myBar = new Chart(ctx, {
    type: 'boxplot',
    data: boxplotData,
    options: {
      responsive: true,
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Chart.js Boxplot'
      }
    }
  });
};