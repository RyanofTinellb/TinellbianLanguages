function setup() {
  createCanvas(window.innerWidth - 20, window.innerHeight - 20);
  textSize(40);
  numberofplanets = floor(random(2, 8))
  system = new System(numberofplanets);
  system.setup();
}

function draw() {
  background(0);
  stroke(255);
  fill(255);
  let gravity = round(100 * system.gravity) / 100;
  text('Gravity: ' + gravity, 10, 80);
  barycentre = system.barycentre();
  translate(width/2 - barycentre.x, height/2 - barycentre.y);
  system.update();
  system.show();
}
