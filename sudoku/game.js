function Game() {
  this.cells = [];
  this.rows = [];
  this.cols = [];
  this.sqrs = [];
  this.highlighted = [];
  this.colors = ['red', 'orange', 'blue', 'green', 'purple'];

  for (let i = 0; i < 9; i++) {
    this.highlighted.push(false);
  }

  for (let i = 0; i < 81; i++) {
    this.cells.push(new Cell(i));
  }
  for (let row = 0; row < 9; row++) {
    block = new Block(this.cells.filter(cell => cell.row == row));
    this.rows.push(block);
  }
  for (let col = 0; col < 9; col++) {
    block = new Block(this.cells.filter(cell => cell.col == col));
    this.cols.push(block);
  }
  for (let sqr = 0; sqr < 9; sqr++) {
    block = new Block(this.cells.filter(cell => cell.sqr == sqr));
    this.sqrs.push(block);
  }

  this.selected = this.cells[0];

  this.set = function(row, col, number) {
    cell = this.rows[row].cells[col]
    number--;
    cell.set(number + 1);
    for (let i = 0; i < 9; i++) {
      if (i != col) {
        this.rows[row].cells[i].possibilities[number] = false;
      }
    }
    for (let i = 0; i < 9; i++) {
      if (i != row) {
        this.rows[i].cells[col].possibilities[number] = false;
      }
    }
    for (let i = 0; i < 9; i++) {
      if (i != cell.ind) {
        this.sqrs[cell.sqr].cells[i].possibilities[number] = false;
      }
    }
    this.update();
  }

  this.setup = function(arr) {
    for (let i = 0; i < 81; i++) {
      row = Math.floor(i / 9);
      col = i % 9;
      if (arr[i] != 0) {
        this.set(row, col, arr[i]);
      }
    }
    this.update();
  }

  this.update = function() {
    for (let cell of this.cells) {
      cell.update();
    }
  }

  this.click = function(event) {
    let id = event.target.id;
    for (let cell of this.cells) {
      if (cell.sid == id) {
        cell.select();
        this.selected = cell;
      } else {
        cell.deselect();
      }
    }
  }

  this.keypress = function(event) {
    number = parseInt(event.key);
    if (event.key == 'ArrowUp') {
      row = (this.selected.row + 8) % 9;
      col = this.selected.col;
      this.select(this.rows[row].cells[col]);
    } else if (event.key == 'ArrowDown') {
      row = (this.selected.row + 1) % 9;
      col = this.selected.col;
      this.select(this.rows[row].cells[col]);
    } else if (event.key == 'ArrowLeft') {
      col = (this.selected.col + 8) % 9;
      row = this.selected.row;
      this.select(this.rows[row].cells[col]);
    } else if (event.key == 'ArrowRight') {
      col = (this.selected.col + 1) % 9;
      row = this.selected.row;
      this.select(this.rows[row].cells[col]);
    } else if (event.keyCode == 32 && this.selected.contents().length == 1) {
      this.cleanCousins(this.selected);
    } else if (number != 0) {
      this.selected.possibilities[number - 1] = false;
      if (this.selected.contents().length == 1) {
        this.cleanCousins(this.selected);
      }
      this.selected.update();
    }
  }

  this.select = function(square) {
    for (let cell of this.cells) {
      if (cell.sid == square.sid) {
        cell.select();
        this.selected = cell;
      } else {
        cell.deselect();
      }
    }
  }

  this.cleanCousins = function(cell) {
    for (square of this.findCousins(cell)) {
      number = parseInt(cell.contents()) - 1;
      len = square.contents().length;
      square.possibilities[number] = false;
      if (len == 2 && square.contents().length == 1) {
        this.cleanCousins(square);
      }
      square.update();
    }
  }

  this.highlight = function(number) {
    if (this.highlighted[number - 1]) {
      this.highlighted[number - 1] = false;
      this.unhighlight(number);
    } else {
      this.highlighted[number - 1] = true;
      for (cell of this.cells) {
        cell.cell.innerHTML = cell.cell.innerHTML.replace(number, '<span class="light">' + number + '</span>');
      }
      color = this.colors[Math.floor(5 * Math.random())];
      styleblock = document.getElementById('style');
      style = styleblock.innerHTML;
      for (let clr of this.colors) {
        style = style.replace(clr, color);
      }
      styleblock.innerHTML = style;

    }
  }

  this.unhighlight = function(number) {
    for (cell of this.cells) {
      cell.cell.innerHTML = cell.cell.innerHTML.replace('<span class="light">' + number + '</span>', number);
    }
  }

  this.findCousins = function(square) {
    return this.cells.filter(cell => ((cell.row == square.row || cell.col == square.col || cell.sqr == square.sqr) && cell.sid != square.sid));
  }
}
