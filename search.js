if (window.location.href.indexOf("?") != -1) {
    search();
}

function search() {
    document.getElementById("results").innerHTML = "Searching...";
    var url = "searching.json";
    var xmlhttp = new XMLHttpRequest();
    var andButton = document.getElementById("and")
    xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            let text = JSON.parse(this.responseText);
            let terms = getTerms();
            if (!terms.length) {
                arr = [];
            } else if (terms.length == 1) {
                arr = oneTermSearch(text, terms);
            } else {
                arr = multiTermSearch(text, terms, andButton.checked);
            }
            display(arr, text, "results", terms, andButton.checked);
        }
    };
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
}

// returns array of terms
function getTerms() {
    var andOr;
    var url;
    var searchString;
    var text;
    const MARKUP = ["%E2%80%99", "'",
        "%c3%bb", "$u",
        "%c9%a8", "\u0268",
        "%C9%A8", "\u0268",
        "%27", "'",
        "\u0294", "''",
        "\u00ec", "$e",
        "%28", "(",
        "%29", ")",
        "%c5%97", ",r",
        "%20", "+",
        "%24", "$",
        "%25", "%",
        "%3b", " ",
        "%26", "&",
        "%2cr", ",r"
    ];
    url = window.location.href;
    url = url.split("?");
    searchString = url[1].split("&");
    try {
        andOr = searchString[1].split("=")[1];
    } catch (err) {
        andOr = "and"
    }
    if (andOr == "or") {
        document.getElementById("or").checked = true
    }
    text = searchString[0].split("=")[1];
    for (i = 0; i < MARKUP.length; i += 2) {
        text = text.split(MARKUP[i]).join(MARKUP[i + 1]).toLowerCase();
    }
    document.getElementById("term").value = text.split("+").join(" ");
    return text.split("+").filter(i => i != "");
}

function unique(arr) {
    return arr.filter(
        (item, pos, ary) => !pos || item !== ary[pos - 1]
    );
}

function uniquePageNumbers(pages) {
    return pages.map(page => {
        page.lines = unique(page.lines.sort());
        return page;
    });
}

function multiTermSearch(arr, terms, andButton) {
    let pages = [].concat(...terms.map(term => oneTermSearch(arr, term)));
    pages.sort((a, b) => a.page - b.page);
    let output = [];
    let current = undefined;
    for (let page of pages) {
        if (current && page.page === current.page) {
            current.lines.push(...page.lines);
            current.count++;
        } else {
            if (current) { output.push(current); }
            current = {page: page.page, lines: page.lines, count: 1};
        }
    }
    output = uniquePageNumbers(output);
    filter = andButton ? page => page.count === terms.length : page => true;
    return output.filter(filter);
}

function oneTermSearch(arr, term) {
    pages = arr.terms[term];
    text = [];
    for (page in pages) {
        text.push({
            page: parseInt(page),
            lines: pages[page].map(line => parseInt(line))
        });
    }
    return text;
}

// capitalises first letter
function capitalise(string) {
    if (string.length == 0) {
        return ''
    }
    if (string.startsWith('&rsquo;')) {
        return string.replace('&rsquo;', '&#x294;');
    } else {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
}

function markdown(terms) {
    const MARKING = [
        ")a", "&agrave;",
        "()e", "&ecirc;",
        ")e", "&egrave;",
        ")i", "&igrave;",
        ")o", "&ograve;",
        ")u", "&ugrave;",
        "_o", "&#x14d;",
        "+h", "&#x2b0;",
        ",c", "&#x255;",
        ",n", "&#x14b;",
        "''", "&#x294;",
        "'", "&rsquo;",
        "$h", "&#x2b1;",
        "-i", "&#x268;",
        "=j", "&#x25f;",
        "$l", "&#x28e;",
        "$n", "&#x272;",
        "$r", "&#x279;",
        ",r", "&#x157;",
        "!e", "&#x259;",
        "-u", "&#x289;",
        "_u", "&#x16b;",
        ".", "&middot;"
    ]
    return terms.map(term => {
        for (i = 0; i < MARKING.length; i++) {
            term = term.split(MARKING[i]).join(MARKING[++i]);
        }
        return term;
    });
}

function titleSearch(arr, terms, andButton) {
    let names = arr.names.map((elt, i) => ({
        name: elt,
        url: arr.urls[i],
        count: 0,
    }));
    terms.forEach(term => {
        names.forEach(name => {
            if (name.name.toLowerCase().includes(term)) { name.count++; }
        });
    });
    numTerms = terms.length;
    // filter = andButton ? name => name.count === terms.length : name =>
    filter = name => (andButton ? name.count === terms.length : name.count);
    names = names.filter(filter);
    return `<div class="title-results"><ul>${names.map(
        name => `<a href="${name.url}">${name.name}</a></li>`
    ).join(';<br> ')}</ul></div>`;
}

function display(pages, data, id, terms, andButton) {
    terms = markdown(terms);
    let regexes = terms.map(term =>
            RegExp(`(${term}|${capitalise(term)})`, 'g'));
    document.getElementById(id).innerHTML = `${titleSearch(data, terms, andButton)}${
    !arr.length ? terms.join(' ') + " not found" :
         `<ol>${pages.map(page => {
            let pagenum = page.page;
            let link = data.urls[pagenum];
            let name = data.names[pagenum];
            let lines = page.lines.map(
                linenum => highlight(regexes, data.sentences[linenum]));
            return `<li><a href="${link}">${name}</a>: ${
                lines.join(' &hellip; ')}</li>`;
    }).join('')}</ol>`}`;
}

function highlight(terms, line) {
    terms.forEach(term => {
        line = line.replace(term, '<strong>$1</strong>');
    });
    return line;
}
