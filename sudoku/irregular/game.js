class Game {
    constructor() {
        this.cells = [];
        this.rows = [];
        this.cols = [];
        this.rgns = [];
        this.highlighted = Array(9).fill(false);
        this.colors = ['red', 'orange', 'blue', 'green', 'purple'];
        this.color = this.colors[Math.floor(5 * Math.random())];
        this.setupMode = document.getElementById('setupMode');
        for (let i = 0; i < 81; i++) {
            this.cells.push(new Cell(i));
        }
        for (let row = 0; row < 9; row++) {
            let house = new House(this.cells.filter(cell => cell.row == row));
            this.rows.push(house);
        }
        for (let col = 0; col < 9; col++) {
            let house = new House(this.cells.filter(cell => cell.col == col));
            this.cols.push(house);
        }
        for (let rgn = 0; rgn < 9; rgn++) {
            let house = new House(this.cells.filter(cell => cell.rgn == rgn));
            this.rgns.push(house);
        }
        this.selected = this.cells[0];
    }
    set(cell, number) {
        number--;
        cell.set(number + 1);
        this.cleanCousins(cell);
        this.update();
    };
    setup(arr) {
        for (let i = 0; i < 81; i++) {
            row = Math.floor(i / 9);
            col = i % 9;
            if (arr[i] != 0) {
                this.set(row, col, arr[i]);
            }
        }
        this.update();
    };
    update() {
        for (let cell of this.cells) {
            cell.update();
        }
    };
    click(event) {
        let id = event.target.id;
        for (let cell of this.cells) {
            if (cell.sid == id) {
                cell.select();
                this.selected = cell;
            } else {
                cell.deselect();
            }
        }
    };
    keypress(event) {
        let row;
        let col;
        let number = parseInt(event.key);
        if (event.key == 'ArrowUp') {
            row = (this.selected.row + 8) % 9;
            col = this.selected.col;
            this.select(this.rows[row].cells[col]);
            event.preventDefault();
        } else if (event.key == 'ArrowDown') {
            row = (this.selected.row + 1) % 9;
            col = this.selected.col;
            this.select(this.rows[row].cells[col]);
            event.preventDefault();
        } else if (event.key == 'ArrowLeft') {
            col = (this.selected.col + 8) % 9;
            row = this.selected.row;
            this.select(this.rows[row].cells[col]);
            event.preventDefault();
        } else if (event.key == 'ArrowRight') {
            col = (this.selected.col + 1) % 9;
            row = this.selected.row;
            this.select(this.rows[row].cells[col]);
            event.preventDefault();
        } else if (event.key == "+" && this.selected.contents().length == 1) {
            this.cleanCousins(this.selected);
        } else if (number != 0 && !isNaN(number)) {
            if (this.setupMode.checked) {
                this.set(this.selected, number);
            } else {
                this.selected.possibilities[number - 1] = false;
                if (this.selected.contents().length == 1) {
                    this.cleanCousins(this.selected);
                }
            }
            this.selected.update();
            this.keeplit();
        }
    };
    keySelect(number) {
        if (this.setupMode.checked) {
            this.set(this.selected, number);
        } else {
            this.selected.possibilities[number - 1] = false;
            if (this.selected.contents().length == 1) {
                this.cleanCousins(this.selected);
            }
        }
        this.selected.update();
    };

    select(square) {
        for (let cell of this.cells) {
            if (cell.sid == square.sid) {
                cell.select();
                this.selected = cell;
            } else {
                cell.deselect();
            }
        }
    };

    cleanCousins(cell) {
        this.findCousins(cell).forEach(square => {
            let number = parseInt(cell.contents()) - 1;
            let len = square.contents().length;
            square.possibilities[number] = false;
            if (len == 2 && square.contents().length == 1) {
                this.cleanCousins(square);
            }
            square.update();
        });
    };

    highlight(number) {
        this.color = this.colors[Math.floor(5 * Math.random())];
        if (this.highlighted[number - 1]) {
            this.unlight(number);
        } else {
            this.relight(number);
        }
    };

    relight(number) {
        this.highlighted[number - 1] = true;
        for (let cell of this.cells) {
            cell.cell.innerHTML = cell.contents().replace(number, '<span class="light">' + number + '</span>');
        }
        let styleblock = document.getElementById('style');
        let style = styleblock.innerHTML;
        for (let clr of this.colors) {
            style = style.replace(clr, this.color);
        }
        styleblock.innerHTML = style;
    }

    unlight(number) {
        this.highlighted[number - 1] = false;
        for (let cell of this.cells) {
            cell.cell.innerHTML = cell.contents().replace('<span class="light">' + number + '</span>', number);
        }
    }

    keeplit() {
        this.highlighted.forEach((v, i) => {
            if (v) {
                this.relight(i + 1)
            }
        })
    }

    findCousins(square) {
        return this.cells.filter(cell => ((cell.row == square.row || cell.col == square.col || cell.rgn == square.rgn) && cell.sid != square.sid));
    };
}