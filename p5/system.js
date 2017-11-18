function System(num) {
  this.gravity = pow(2, random(-2, 7));
  this.planets = [];

  this.setup = function() {
    for (let i = 0; i < num; i++) {
      this.planets.push(new Planet());
    }
  }

  this.findForces = function() {
    forces = [];
    for (let i = 0; i < num; i++) {
      let row = [];
      for (let j = 0; j < i; j++) {
        row.push(this.findForce(this.planets[i], this.planets[j]));
      }
      forces.push(row);
    }
    return forces;
  }

  this.barycentre = function() {
    var barycentre = createVector(0, 0);
    var mass = 0;
    for (var planet of this.planets) {
      var pos = planet.pos.copy();
      barycentre.add(pos.mult(planet.mass));
      mass += planet.mass
    }
    return barycentre.div(mass);
  }

  this.findForce = function(planet, moon) {
    // find the force of the planet on the moon
    let mag = this.gravity * planet.mass * moon.mass;
    planet = planet.pos.copy();
    moon = moon.pos.copy();
    let force = moon.sub(planet);
    mag /= force.magSq();
    force.setMag(mag);
    return force;
  }

  this.update = function() {
    forces = this.findForces();
    for (let i = 0; i < num; i++) {
      for (let j = 0; j < i; j++) {
        planet = this.planets[i];
        moon = this.planets[j];
        if (planet.dist(moon) > planet.radius + moon.radius) {
          planet.addForce(forces[i][j]);
          moon.subForce(forces[i][j]);
        }
      }
      this.planets[i].update();
      this.planets[i].resetAcceleration();
    }
  }

  this.show = function() {
    for (planet of this.planets) {
      planet.show();
    }
  }

}
