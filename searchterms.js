async function searchterms() {
    document.getElementById('results').innerHTML = 'Searching...';
    let data = await fetch('searching.json');
    data = await data.json();
    display(data, 'results');
}

// displays results as list
// @param Array arr: results array
function display(arr, id) {
    entries = Object.entries(arr['terms']);
    urls = arr['urls'];
    document.getElementById(id).innerHTML =
        `<ol>${entries.sort().map(
                entry => `${entry[0]} ${
                    Object.keys(entry[1]).map(
                        page => `<a href="${urls[page]}">${page}</a>`
                    ).join(', ')
                }`
            ).join('<br>')}</ol>`;
}
