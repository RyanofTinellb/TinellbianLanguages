let input = document.getElementById('input');
let output = document.getElementById('output');
let lookAhead = document.getElementById('lookAhead');
let lookBehind = document.getElementById('lookBehind');

function createText() {
    let main = {};
    let text = '\n' + input.value;
    let num = parseInt(lookAhead.value);
    text = text.replace(/(\W) /g, '$1');
    let first;
    let second = text.substr(0, num);
    let randomLetter = '\n';
    for (let i = 1; i < text.length - num + 1; i++) {
        first = second.charAt(0);
        second = text.substr(i, num);
        if (main[first] === undefined) {
            main[first] = [];
        }
        main[first].push(second);
    }
    text = randomLetter;
    for (let i = 0; i < 10000; i++) {
        let arr = main[randomLetter];
        if (arr === undefined) {
            text += '\n';
            arr = main['\n'];
        }
        randomLetter = arr[Math.random() * arr.length << 0];
        text += randomLetter;
        randomLetter = randomLetter.slice(-1);
    }
    text = text.replace(/(\W)/g, '$1 ').replace(/(\n)+/g, '<br>')
            .replace(/(<br> )+/g, '<br>')
            .replace(/’ /g, '’').replace(/ ”/g, '”').replace(/“ /g, '“');
    output.innerHTML = text;
}
