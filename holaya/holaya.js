var foreground_colour = 'black';
var background_colour = 'azure';

var body = document.getElementById("body").style.backgroundColor = background_colour;


var letterB = ['***',
               '* *',
               '  *',
               '  *',
               '  *'];

var letterC = [' * ',
               '* *',
               ' * ',
               ' * ',
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

var letterJ = ['*  ',
               ' * ',
               '  *',
               '* *',
               '***'];

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

var letterQ = ['***',
               ' * ',
               '*  ',
               '* *',
               ' **'];

var letterR = ['* *',
               ' * ',
               '***',
               ' * ',
               '***'];

var letterS = [' * ',
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

var letterX = ['** ',
               '* *',
               '  *',
               '* *',
               '** '];

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

var letterVowel = ['   ',
                   '   ',
                   '***',
                   '*  ',
                   '*  '];

var letterSpace = [' ',
                   ' ',
                   ' ',
                   ' ',
                   ' '];

var letterA = [' ', ' ', ' ', ' ', ' '];
var letterE = ['*', ' ', ' ', ' ', ' '];
var letterI = ['*', '*', ' ', ' ', ' '];
var letterO = ['*', ' ', '*', '*', ' '];
var letterU = ['*', '*', ' ', '*', ' '];

var letters = [];
letters['?'] = letterVowel;
letters['B'] = letterB;
letters['C'] = letterC;
letters['D'] = letterD;
letters['F'] = letterF;
letters['G'] = letterG;
letters['H'] = letterH;
letters['J'] = letterJ;
letters['K'] = letterK;
letters['L'] = letterL;
letters['M'] = letterM;
letters['N'] = letterN;
letters['P'] = letterP;
letters['Q'] = letterQ;
letters['R'] = letterR;
letters['S'] = letterS;
letters['T'] = letterT;
letters['V'] = letterV;
letters['W'] = letterW;
letters['X'] = letterX;
letters['Y'] = letterY;
letters['Z'] = letterZ;
letters[' '] = letterSpace;

letters['A'] = letterA;
letters['E'] = letterE;
letters['I'] = letterI;
letters['O'] = letterO;
letters['U'] = letterU;

function write(word) {
  let output = '';
  for (let i = 0; i < word.length + 1; i += 2) {
    output += syllable(word.substring(i, i + 2));
  }
  return output;
}

function Translation(sentence) {
  this.sentence = sentence;

  this.translate = function() {
    return 'Qisa  senatenake  hasa  be?ena  taranasalateda  ?inato  maya  firasata  relekasa  ?ina  ?itasa  sakaripata';
  };

  this.romaji = this.translate();
  this.holaya = write(this.romaji);
}

function test_translate() {

}

// combines two character arrays into one
function combine(letter1, letter2) {
  if (!letter2) {
    return letter1;
  }
  if (!letter1) {
    return letter2;
  }
  let length = Math.min(letter1.length, letter2.length);
  let combine = [];
  for (let i = 0; i < length; i++) {
    combine.push(letter1[i] + ' ' + letter2[i])
  }
  return combine;
}

// displays an HTML table displaying the syllable
function syllable(string) {
  chars = string.toUpperCase();
  if (chars.length == 1) {
    return display(letters[chars], string);
  } else if (chars.length == 2){
    let letter = combine(letters[chars[0]], letters[chars[1]]);
    return display(letter, string);
  } else {
    return '';
  }
}

function display(letter, character) {
  if (character.length == 1) {
    var td = '<td></td>';
  } else {
    var td = '';
  }
  if (letter) {
    let display = '<table style="display:inline-table;"><tr><td colspan="7" style="text-align:center;font-family:monospace;">' + character + '</td></tr>';
    for (row of letter) {
      display += '<tr>' + td;
      for (column of row) {
        display += '<td style="background-color:'
        if (column == '*') {
          display += foreground_colour;
        } else {
          display += background_colour;
        }
        display += ';"></td>';
      }
      display += td + td + td + '</tr>';
    }
    display += '</table>&nbsp;';
    return display;
  } else {
    return '';
  }
}

function glossary() {
  glossary = '';
  let letters = 'bcdfghjklmnpqrstvwxyz';
  let descriptions = ['(sports) bat', 'creature', 'dog tail', 'fence',
    'gold medal', 'half', 'jug', 'king&rsquo;s throne', 'large', 'my back',
    'no king', 'person looking down a microscope', '(upside down) question mark', 'rabbit', 'squiggle', '(spinning) top', 'vacuum cleaner',
    'woman with aching back', 'xylem', 'yell', 'zebra stripes'];
  for (let i = 0; i < letters.length; i++) {
    glossary += '<p>' + write(letters[i]) + ': ' + descriptions[i] + '</p>';
  }
  return glossary;
}
