function Cell (index) {
  thick = '2px';
  this.row = Math.floor(index / 9);
  this.col = index % 9;

  this.setupMode = document.getElementById('setupMode');

  sqrrow = Math.floor(this.row / 3) % 3;
  sqrcol = Math.floor(this.col / 3) % 3;
  this.sqr = 3 * sqrrow + sqrcol;

  sqrrow = this.row % 3;
  sqrcol = this.col % 3;
  this.ind = 3 * sqrrow + sqrcol;

  this.sid = 's' + index;

  this.possibilities = [];
  for (let i = 0; i < 9; i++) {
    this.possibilities.push(true);
  }

  this.cell = document.getElementById(this.sid);

  this.contents = function() {
    content = '';
    for (let i = 0; i < 9; i++) {
      if (this.possibilities[i]) {
        content += (i + 1).toString();
      }
    }
    return content;
  }

  this.borders = function() {
    if (this.row % 3 == 0) {
      this.cell.style.borderTopWidth = thick;
    }
    if (this.col % 3 == 0) {
      this.cell.style.borderLeftWidth = thick;
    }
    if (this.row % 3 == 2) {
      this.cell.style.borderBottomWidth = thick;
    }
    if (this.col % 3 == 2) {
      this.cell.style.borderRightWidth = thick;
    }
  }

  this.setup = function() {
    this.borders();
    this.update();
  }

  this.update = function() {
    this.resize();
    this.cell.innerHTML = this.contents();
  }

  this.resize = function() {
    if (this.contents().length == 1) {
      this.cell.style.fontSize = 'xx-large';
    } else {
      this.cell.style.fontSize = 'large';
    }
  }

  this.set = function(number) {
    number--;
    for (let i = 0; i < 9; i++) {
      this.possibilities[i] = (i == number);
    }
  }

  this.select = function() {
    this.selected = true;
    if (this.setupMode.checked) {
      this.cell.style.backgroundColor = 'red';
    } else {
      this.cell.style.backgroundColor = 'yellow';
    }
  }

  this.deselect = function() {
    this.selected = false;
    this.cell.style.backgroundColor = 'white';
  }

  this.setup();
}
