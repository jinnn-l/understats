/**
 * @author Amy Sitwala https://medium.com/code-nebula/automatically-generate-chart-colors-with-chart-js-d3s-color-scales-f62e282b2b41
 */ 

const COLOUR_SCALE = d3.interpolateWarm;
const COLOUR_RANGE_INFO = {
  colourStart: 0,
  colourEnd: 1,
  useEndAsStart: false,
}; 

function calculatePoint(i, intervalSize) {
  var { colourStart, colourEnd, useEndAsStart } = COLOUR_RANGE_INFO;
  return (useEndAsStart
    ? (colourEnd - (i * intervalSize))
    : (colourStart + (i * intervalSize)));
};

function interpolateColors(dataLength) {
  var { colourStart, colourEnd } = COLOUR_RANGE_INFO;
  var colorRange = colourEnd - colourStart;
  var intervalSize = colorRange / dataLength;
  var i, colorPoint;
  var colorArray = [];

  for (i = 0; i < dataLength; i++) {
    colorPoint = calculatePoint(i, intervalSize, COLOUR_RANGE_INFO);
    colorArray.push(COLOUR_SCALE(colorPoint));
  }

  return colorArray;
};