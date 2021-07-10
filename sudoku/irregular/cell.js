let thick = '2px';
let layout = [
    [0, 1, 1, 1, 2, 2, 2, 0, 0],
    [0, 1, 1, 5, 5, 5, 2, 2, 2],
    [1, 1, 5, 5, 6, 6, 6, 2, 2],
    [1, 7, 5, 6, 6, 8, 6, 6, 2],
    [1, 7, 5, 5, 0, 8, 8, 6, 3],
    [4, 7, 7, 5, 7, 7, 8, 6, 3],
    [4, 4, 7, 7, 7, 8, 8, 3, 3],
    [4, 4, 4, 8, 8, 8, 3, 3, 0],
    [0, 0, 4, 4, 4, 3, 3, 3, 0]
]

class Cell {
    constructor(index) {
        this.row = Math.floor(index / 9);
        this.col = index % 9;
        this.rgn = layout[this.row][this.col];

        this.setupMode = document.getElementById('setupMode');

        // let sqrrow = Math.floor(this.row / 3) % 3;
        // let sqrcol = Math.floor(this.col / 3) % 3;
        // this.sqr = 3 * sqrrow + sqrcol;

        // sqrrow = this.row % 3;
        // sqrcol = this.col % 3;
        // this.ind = 3 * sqrrow + sqrcol;

        this.sid = 's' + index;

        this.possibilities = [];
        for (let i = 0; i < 9; i++) {
            this.possibilities.push(true);
        }

        this.cell = document.getElementById(this.sid);
        this.setup();
    }

    contents() {
        content = '';
        for (let i = 0; i < 9; i++) {
            if (this.possibilities[i]) {
                content += (i + 1).toString();
            }
        }
        return content;
    };

    borders() {
        if (this.row == 0) {
            this.cell.style.borderTopWidth = thick;
        }
        if (this.row == 8) {
            this.cell.style.borderBottomWidth = thick;
        }
        if (this.col == 0) {
            this.cell.style.borderLeftWidth = thick;
        }
        if (this.col == 8) {
            this.cell.style.borderRightWidth = thick;
        }
        if (layout[Math.max(0, this.row - 1)][this.col] != this.rgn) {
            this.cell.style.borderTopWidth = thick;
        }
        if (layout[Math.min(8, this.row + 1)][this.col] != this.rgn) {
            this.cell.style.borderBottomWidth = thick;
        }
        if (layout[this.row][Math.max(0, this.col - 1)] != this.rgn) {
            this.cell.style.borderLeftWidth = thick;
        }
        if (layout[this.row][Math.min(8, this.col + 1)] != this.rgn) {
            this.cell.style.borderRightWidth = thick;
        }
    };

    setup() {
        this.borders();
        this.update();
    };

    update() {
        this.resize();
        this.cell.innerHTML = this.contents();
    };

    resize() {
        if (this.contents().length == 1) {
            this.cell.style.fontSize = 'xx-large';
        } else if (this.contents().length >= 6) {
            this.cell.style.fontSize = 'small';
        } else {
            this.cell.style.fontSize = 'large';
        }
    };

    set(number) {
        number--;
        for (let i = 0; i < 9; i++) {
            this.possibilities[i] = (i == number);
        }
    };

    select() {
        this.selected = true;
        if (this.setupMode.checked) {
            this.cell.style.backgroundColor = 'red';
        } else {
            this.cell.style.backgroundColor = 'yellow';
        }
    };

    deselect() {
        this.selected = false;
        this.cell.style.backgroundColor = 'white';
    };

}