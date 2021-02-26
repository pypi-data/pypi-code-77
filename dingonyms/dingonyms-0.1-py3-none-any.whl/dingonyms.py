#!/usr/bin/env python3
# encoding: utf-8
# api: cli
# title: dingonyms
# description: scrape synonyms from various web services
# version: 0.1
# license: BSDL
# category: translation
# keywords: dictionary, synonyms, antonyms
# classifiers: word
# architecture: all
# depends: deb:ding (>= 1.8), python (>= 3.7), python:requests (>= 2.1)
#
#
# CLI tool to extract synonyms/antonyms from online services, which formats
# them into dict structures (word|alt :: defintion; etc.) suitable for `ding`.
#
# It's fairly basic, and not all result sets are structured alike.
# Furthermore the extraction schemes aren't likely to last for long; web
# scraping is typically a maintenance task.
# Only scans for singular words (most services wouldn't return results
# otherwise). And might spit out error messages for charset issues as well.
#
# SYNTAX
#
#    dingonyms --thesaurus "Define"
#    dingonyms --merriamwebster "find"
#    dingonyms --openthesaurus "Wort"
#    dingonyms --urban "bazinga"
#
# CONFIG IN ~/.dingrc (take care to change `3` to available index)
#
#    set searchmeth(3,name) {Synonyms}
#    set searchmeth(3,type) {3}
#    set searchmeth(3,dictfile) {}
#    set searchmeth(3,separator) { :: }
#    set searchmeth(3,language1) {Group}
#    set searchmeth(3,language2) {Synonyms}
#    set searchmeth(3,grepcmd) {dingonyms}
#    set searchmeth(3,grepopts) {--thesaurus}
#    set searchmeth(3,maxlength) {30}
#    set searchmeth(3,maxresults) {200}
#    set searchmeth(3,minlength) {2}
#    set searchmeth(3,shapedresult) {1}
#    set searchmeth(3,foldedresult) {0}
#
# You might want to add one entry for each search backend even.
# (Unique index, title/name, and grepopts --parameter each.)




import sys, os, re
import requests, json, html, textwrap
try:
    sys.stdout.reconfigure(encoding="utf-8")
except:
    pass# and pray

# fetch page
def http_get(url):
    return requests.get(
        url,
        headers={"User-Agent":"dingonyms/0.1 (Python 3.x; CLI; Linux) +https://pypi.org/projects/dingonyms"}
    ).text

# output
class out:
    
    @staticmethod
    def fold(other):
        rows = []
        line = []
        for w in other:
            if len("; ".join(line + [w])) > 45:
                rows.append("; ".join(line))
                line = []
            line.append(w)
        if line:
            rows.append("; ".join(line))
        return rows
    
    @staticmethod
    def alternatives(word, other, fold=True):
        if fold:
            other = out.fold(other)
        word = word + (" |" * (len(other) - 1))
        print("{} :: {}".format(word, " | ".join(other)))

    @staticmethod
    def site(name):
        print("✎ {%s}" % name)

    @staticmethod
    def unhtml(text):
        text = re.sub("\s+", " ", text)
        text = re.sub("<br>|</div>", "\n", text, re.I)
        text = re.sub("(<[^<]+(>|$))+", " ", text)
        return re.sub("  +", " ", html.unescape(text))

        

# extraction
class lookup:

    @staticmethod
    def thesaurus_raw(word, html=""):
        if not html:
            html = http_get("https://www.thesaurus.com/browse/%s" % word)
        other = []
        grp = "synonym"
        # look for word links, or grouping divs (not many reliable html structures or legible class names etc.)
        for row in re.findall(' "/browse/([\w.-]+)" | <div\s+id="(meanings|synonyms|antonyms|[a-z]+)" | (</html)', html, re.X):
            if row[0]:
                other.append(row[0])
            else:
                if other:
                    out.alternatives("%s {%s}" % (word, grp), other)
                    other = []
                grp = row[1]

    @staticmethod
    def thesaurus(word):
        out.site("Thesaurus.com")
        html = http_get("https://www.thesaurus.com/browse/%s" % word)
        # there's a nice pretty JSON blob inside the page
        m = re.search("INITIAL_STATE\s*=\s*(\{.+\})[;<]", html)
        if m:
            j = json.loads(re.sub('"state":undefined,', '', m.group(1)))
            for grp in "synonyms", "antonyms":
                if grp == "antonyms":
                    print("❙ {Antonyms} ❙")
                for d in j["searchData"]["relatedWordsApiData"]["data"]:
                    if grp in d and len(d[grp]):
                        out.alternatives(
                            "%s {%s} (%s)" % (d["entry"], d["pos"], d["definition"]),
                            [word["term"] for word in d[grp]]
                        )
        else:
            lookup.thesaurus_raw(word, html)

    @staticmethod
    def openthesaurus(word):
        out.site("OpenThesaurus.de")
        # there's a proper API here
        j = json.loads(http_get("https://www.openthesaurus.de/synonyme/search?q=%s&format=application/json&supersynsets=true" % word))
        for terms in j["synsets"]:
            supersyn = ""
            if terms["supersynsets"] and terms["supersynsets"][0]:
                supersyn = "; ".join([w["term"] for w in terms["supersynsets"][0]][0:3])
                supersyn = "("+supersyn+")"
            out.alternatives(
                "%s %s" % (word, supersyn),
                [w["term"] for w in terms["terms"]]
            )

    @staticmethod
    def merriamwebster(word):
        out.site("Merriam-Webster")
        html = http_get("https://www.merriam-webster.com/thesaurus/%s" % word)
        grp = "Synonyms"
        ls = []
        # word links here are decorated with types (noun/verb), and groups neatly include a reference to the search term (or possibly a different related term)
        for row in re.findall(' href="/thesaurus/([\w.-]+)\#(\w+)" | ="function-label">(?:Words\s)?(Related|Near\sAntonyms|Antonyms|Synonyms|\w+)\s\w+\s<em>([\w.-]+)</em> | (</html)', html, re.X):
            #print(row)
            if row[0]:
                ls.append("%s {%s}" % (row[0], row[1][0]))
            else:
                if ls:
                    out.alternatives(word + " {%s}" % grp, ls)
                    ls = []
                grp = row[2]
                word = row[3]
                
    @staticmethod
    def urban(word):
        out.site("UrbanDictionary")
        html = http_get("https://www.urbandictionary.com/define.php?term=%s" % word)
        for html in re.findall('="def-header">(.+?)="contributor|def-footer">', html, re.S):
            m = re.search('<a class="word" href="/define.php\?term=\w+" name="\w+">([\w.-]+)</a>', html)
            if m:
                word = m.group(1)
                html = re.sub("^.+?</a>", "", html, re.S)
            text = out.unhtml(html)
            if not text:
                continue
            # at this point, it's becoming custom output to wrap flow text into Tk/ding window
            text = re.sub("^[\s|]+", "", text)
            text = textwrap.wrap(text, 45)
            print("%s %s :: %s" % (word, " | " * (len(text) - 1), "|".join(text)))


# __main__
def main():
    ...
if len(sys.argv) == 1:
    print("Syntax :: synonymlookup --site word")
else:
    argv = sys.argv[1:]
    word = "search"
    meth = "thesaurus"
    for w in argv:
        # separate --params from search word
        if not w or w == "--":
            continue
        elif re.match("-", w):
            meth = re.sub("\W+", "", w).lower()
            if not hasattr(lookup, meth):
                print("No such method: `%s`" % meth)
                meth = "thesaurus"
        else:
            word = w
    getattr(lookup, meth)(word)

