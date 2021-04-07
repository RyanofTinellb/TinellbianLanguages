{
  "template": [
    "    <script type=\"text/javascript\">",
    "        let terms = window.location.href.split(\"?highlight=\")[1];",
    "        terms = terms.split(\"+\");",
    "        let loc = document.getElementsByClassName(\"main-contents\")[0];",
    "        let text = loc.innerHTML;",
    "        for (term of terms) {",
    "            const rep = new RegExp(`(^|\\\\W)(${term})($|\\\\W)`, \"gim\");",
    "            text = text.replace(rep, \"$1<highlight>$2</highlight>$3\");",
    "            text = text.replace(/(<[^>]*?)<highlight>([^>]*?)<.highlight>([^>]*?>)/g, \"$1$2$3\");",
    "            text = text.replace(/(<[^>]*?)<highlight>([^>]*?)<.highlight>([^>]*?>)/g, \"$1$2$3\");",
    "            text = text.replace(/<highlight>/g, \"<highlight id=\\\"searchterm\\\">\");",
    "        }",
    "        loc.innerHTML = text;",
    "        loc = document.getElementsByTagName(\"h1\")[0];",
    "        loc.innerHTML += \" <a href=\\\"#searchterm\\\">&rarr;</a>\";        ",
    "    // imaginary comment",
    "    </script>"
  ],
  "styles": {}
}