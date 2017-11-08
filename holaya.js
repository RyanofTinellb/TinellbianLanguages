var letterB = ['***',
               '* *',
               '  *',
               '  *',
               '  *'];

var letterC = [' * ',
               '* *',
               ' * ',
               '* *',
               '* *'];

var letterD = [' * ',
               '* *',
               '* *',
               '  *',
               '** '];

var letterF = ['***',
               '* *',
               '***',
               '* *',
               '***'];

var letterG = ['* *',
               ' * ',
               ' * ',
               '* *',
               ' * '];

var letterH = [' * ',
               ' * ',
               '***',
               ' * ',
               ' * '];

var letterK = ['*  ',
               '*  ',
               '***',
               '* *',
               '* *'];

var letterL = ['***',
               '*  ',
               '* *',
               '***',
               '  *'];

var letterM = ['  *',
               '  *',
               '  *',
               '  *',
               '***'];


var letterN = ['*  ',
               '*  ',
               '***',
               '* *',
               '***'];

var letterP = [' * ',
               ' * ',
               ' * ',
               '  *',
               '***'];

var letterR = ['* *',
               ' * ',
               '***',
               ' * ',
               '***'];

var letterS = ['***',
               '* *',
               '  *',
               ' * ',
               '***'];

var letterT = [' * ',
               ' * ',
               '* *',
               ' * ',
               ' * '];

var letterV = [' * ',
               ' * ',
               '** ',
               ' * ',
               ' **'];

var letterW = [' * ',
               ' * ',
               '***',
               '  *',
               '  *'];

var letterY = ['*  ',
               ' * ',
               '*  ',
               '***',
               '  *'];

var letterZ = ['***',
               ' * ',
               '***',
               ' * ',
               '***'];

var letters = [];
letters['B'] = letterB;
letters['b'] = letterB;
letters['C'] = letterC;
letters['c'] = letterC;
letters['D'] = letterD;
letters['d'] = letterD;
letters['F'] = letterF;
letters['f'] = letterF;
letters['G'] = letterG;
letters['g'] = letterG;
letters['H'] = letterH;
letters['h'] = letterH;
letters['K'] = letterK;
letters['k'] = letterK;
letters['L'] = letterL;
letters['l'] = letterL;
letters['M'] = letterM;
letters['m'] = letterM;
letters['N'] = letterN;
letters['n'] = letterN;
letters['P'] = letterP;
letters['p'] = letterP;
letters['R'] = letterR;
letters['r'] = letterR;
letters['S'] = letterS;
letters['s'] = letterS;
letters['T'] = letterT;
letters['t'] = letterT;
letters['V'] = letterV;
letters['v'] = letterV;
letters['W'] = letterW;
letters['w'] = letterW;
letters['Y'] = letterY;
letters['y'] = letterY;
letters['Z'] = letterZ;
letters['z'] = letterZ;

function write(word) {
  let output = '';
  for (letter of word) {
    output += display(letters[letter], letter);
  }
  return output;
}

function display(letter, character) {
  if (letter) {
    let display = '<table style="display:inline-table;"><tr><td colspan="5" style="text-align:center;">' + character + '</td></tr>';
    for (row of letter) {
      display += '<tr><td></td>';
      for (column of row) {
        display += '<td style="background-color:'
        if (column == '*') {
          display += 'black';
        } else {
          display += 'powderblue';
        }
        display += ';"></td>';
      }
      display += '<td></td></tr>';
    }
    display += '</table>&nbsp;';
    return display;
  } else {
    return '';
  }
}

function glossary() {
  glossary = '';
  let letters = 'bcdfghklmnprstvwyz';
  let descriptions = ['bat', 'creature', 'dog tail', 'fence', 'gold medal', 'half', 'king&rsquo;s throne', 'large', 'my back', 'no king', 'person looking down a microscope', 'rabbit', 'squiggle', '(spinning) top', 'vacuum', 'woman with aching back', 'yell', 'zebra stripes'];
  for (let i = 0; i < letters.length; i++) {
    glossary += '<p>' + write(letters[i]) + ': ' + descriptions[i] + '</p>';
  }
  return glossary;
}
