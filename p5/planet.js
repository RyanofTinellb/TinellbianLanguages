function Planet (name) {
  this.mass = random(1, 10);
  this.pos = createVector(random(height/3, 2*height/3), random(height/3, 2*height/3));
  this.vel = createVector(random(-1, 1), random(-1, 1));
  this.name = name

  this.show = function () {
    stroke(255);
    ellipse(this.pos.x, this.pos.y, this.mass, this.mass);
  }

  this.update = function() {
    this.acc = createVector(0, 0);
    for (let planet of planets) {
      if (this != planet) {
        var acc = p5.Vector.sub(planet.pos, this.pos);
        var rSq = acc.magSq();
        acc.setMag(g * planet.mass / rSq);
        this.acc = p5.Vector.add(this.acc, acc);
      }
    }
    this.vel = p5.Vector.add(this.vel, this.acc);
    this.pos = p5.Vector.add(this.pos, this.vel);
  }

}
