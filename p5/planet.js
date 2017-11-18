function Planet (name) {
  this.mass = random(1, 25);
  // this.radius = random(1, 50);
  this.radius = this.mass;
  sizeoftheuniverse = 5;
  this.pos = createVector(random(width/sizeoftheuniverse, (sizeoftheuniverse-1)*width/sizeoftheuniverse), random(height/sizeoftheuniverse, (sizeoftheuniverse-1)*height/sizeoftheuniverse));
  this.vel = createVector(random(-1, 1), random(-1, 1));
  this.acc = createVector(0, 0);
  let colour = [];
  for (let i = 0; i < 3; i++) {
    colour.push(floor(random(256)));

  }
  this.colour = color(colour[0], colour[1], colour[2]);

  this.dist = function (moon) {
    return this.pos.dist(moon.pos)
  }

  this.show = function () {
    fill(this.colour);
    noStroke();
    ellipse(this.pos.x, this.pos.y, 2*this.radius, 2*this.radius);
  }

  this.resetAcceleration = function () {
    this.acc.setMag(0);
  }

  this.addForce = function (force) {
    force = force.copy();
    force.div(this.mass);
    this.acc.add(force);
  }

  this.subForce = function (force) {
    force = force.copy();
    force.div(this.mass);
    this.acc.sub(force);
  }

  this.update = function() {
    this.vel.add(this.acc);
    this.pos.add(this.vel);
  }

}
