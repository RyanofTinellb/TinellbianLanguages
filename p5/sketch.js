var planets = ['Sun', 'Earth'];
var numberofplanets = 2;
var g = 50;
var sun;
var earth;

function setup() {
  createCanvas(600, 600);
  for (let i = 0; i < numberofplanets; i++) {
    p = new Planet(planets[i]);
    planets[i] = p;
  }
  console.log(document);
  sun = document.getElementById('Sun');
  earth = document.getElementById('Earth');
}

function draw() {
  background(0);
  for (let planet of planets) {
    planet.update();
    planet.show();
  }
}
