#!/usr/bin/env python3
# encoding: utf-8
# api: cli
# type: filter
# title: dingonyms
# description: scrape synonyms from various web services
# version: 0.2
# license: PD
# category: dictionary
# keywords: glossary, synonyms, antonyms
# classifiers: search, dict
# architecture: all
# depends: deb:ding (>= 1.8), python (>= 3.7), python:requests (>= 2.1)
#
#
# CLI tool to extract synonyms/antonyms from online services, which formats
# them into dict structures (word|alt :: definition; etc.) suitable for `ding`.
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
#    dingonyms --synonym "Wort"
#    dingonyms --urban "bazinga"
#    dingonyms --openthesaurus "Wort"
#    dingonyms --woxikon "Wort"
#
# Flags can be abbreviated and also combined: --thes --merrweb would query two
# services at once, or --all even all.
# Reason for supporting multiple sites is allowing to fall back on others if
# one extraction method breaks.
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
#
# SETUP (pip3 install -U dingonyms)
#
# You might have to symlink ~/.local/bin/dingonyms into ~/bin after
# installation. pip-package binaries are often only picked up in
# terminal/interactive shells.
#



import sys, os, re
import requests, json, html, textwrap
try:
    sys.stdout.reconfigure(encoding="utf-8")
except:
    pass# and pray


def http_get(url):
    """ fetch page per requests GET, add user-agent header """
    return requests.get(
        url,
        headers={"User-Agent":"dingonyms/0.1 (Python 3.x; CLI; Linux) +https://pypi.org/projects/dingonyms"}
    ).text


class out:
    """ output utility functions """
    
    @staticmethod
    def fold(other):
        """ Wrap list of words acrosss multiple lines, conjoin ~45 chracters of words in each """
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
        """ craft `Word :: Synonyms` lines """
        if fold:
            other = out.fold(other)
        pipes = len(other) - len(word.split("|"))
        word = word + (" |" * pipes)
        print("{} :: {}".format(word, " | ".join(other)))

    @staticmethod
    def site(name):
        """ output prefix for online service """
        print("✎ {%s}" % name)

    @staticmethod
    def group(name="Antonyms"):
        """ section prefix """
        print("❙ {%s} ❙" % name)

    @staticmethod
    def unhtml(text):
        """ crude html2text for urbandictionary flow text """
        text = re.sub("\s+", " ", text)
        text = re.sub("<br>|</div>", "\n", text, re.I)
        text = re.sub("(<[^<]+(>|$))+", " ", text)
        return re.sub("  +", " ", html.unescape(text))

        
class lookup:
    """
        Online service backends and extraction.
        Not a real object, just a function collection.
    """

    def thesaurus_raw(self, word, html=""):
        """ thesaurus-?(raw|htm) """
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

    def thesaurus(self, word):
        """ thesauru s |t | t[he]+s[saurus]* """
        out.site("Thesaurus.com")
        html = http_get("https://www.thesaurus.com/browse/%s" % word)
        # there's a nice pretty JSON blob inside the page
        m = re.search("INITIAL_STATE\s*=\s*(\{.+\})[;<]", html)
        if m:
            j = json.loads(re.sub('"\w+":undefined,', '', m.group(1)))
            for grp in "synonyms", "antonyms":
                if grp == "antonyms":
                    out.group("Antonyms")
                for d in j["searchData"]["relatedWordsApiData"]["data"]:
                    if grp in d and len(d[grp]):
                        out.alternatives(
                            "%s {%s} (%s)" % (d["entry"], d["pos"], d["definition"]),
                            [word["term"] for word in d[grp]]
                        )
        else:
            self.thesaurus_raw(word, html)

    def openthesaurus(self, word):
        """ openthesaurus | open | ot | opnt\w+ """
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
            
    def woxikon(self, word):
        """ woxikon | w | wx | wxk\w* """
        out.site("Woxikon")
        html = http_get("https://synonyme.woxikon.de/synonyme/%s.php" % word.lower())
        grp = ""
        ls = []
        for row in re.findall(' <a\s+href="[^"]+/synonyme/[\w.%-]+">(\w[^<]+)</a> | Bedeutung:\s+<b>(\w[^<]+)< | </html ', html, re.X):
            if row[0]:
                ls.append(row[0])
            else:
                if ls:
                    out.alternatives("%s (%s)" % (word, grp), ls)
                    ls = []
                grp = row[1]

    def merriamwebster(self, word):
        """ merriam-?webster | mw | mer\w* | m\w*w\*b\w* | \w*web\*w """
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

    #def reverso(self, word):
    #https://synonyms.reverso.net/synonym/de/word

    def synonym(self, word):
        """
            synonym(\.?com) | s | sy?n\w* |
            
            Doing a fair bit of super-specific HTML lookarounds here, because
            there's a wealth of decoration. DOM traversal might have been simpler
            in this case.
        """
        out.site("synonym.com")
        html = http_get("https://www.synonym.com/synonyms/%s" % word)
        html = re.sub('^.+?="result-group-container">', "", html, 0, re.S)
        html = re.sub('<div class="rightrail-container">.+$', "", html, 0, re.S)
        ...
        rx = """
            <div\sclass="word-title.+?> \s*\d\.\s ([\w.\-]+) \s* 
               \s* .*?
               \s* <span\s+class="part-of-speech">\s*(\w+)[.\s]*</span>
               \s* <span\s+class="pronunciation">\((.+?)\)</span>
               \s* <span\s+class="definition"> (.+?) </div> |
            <a\sclass="chip[^">]*"\shref="/synonyms/([\w.-]+)" |
            <div\sclass="card-title[^>]+>\s*(Antonyms)\s*</div> |
            </html>
        """
        ls = []
        for group, verb, pron, defs, add_word, antonyms in re.findall(rx, html, re.X|re.S):
            if add_word:
                ls.append(add_word)
            else:
                if ls:
                    out.alternatives(word, ls)
                    ls = []
                if antonyms:
                    word = " 🞬 {Antonyms}"
                    continue
                    #if not ls:
                    #    continue
                defs = re.sub('(<[^>]+>|\s+)+', " ", defs, 0, re.S).strip()
                defs = " |   ".join(textwrap.wrap(defs, 50))
                word = group + " {" + verb + "} [" + pron + "] |  (" + defs + ")"

                
    def urban(self, word):
        """ urban | u | u\w*[brn]\w* """
        out.site("UrbanDictionary")
        html = http_get("https://www.urbandictionary.com/define.php?term=%s" % word)
        for html in re.findall('="def-panel\s*"[^>]*>(.+?)="contributor|def-footer">', html, re.S):
            if re.search('<div class="ribbon">[\w\s]+ Word of the Day</div>', html):
                continue
            else:
                html = re.sub('^.+?="def-header">', "", html, 1, re.S)
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
            
    def all(s, word):
        """ all | a | Run through all available services """
        for method in (s.thesaurus, s.merriamwebster, s.synonym, s.openthesaurus, s.woxikon, s.urban):
            method(word)

# instantiate right away
lookup = lookup()


# __main__
def __main__():
    if len(sys.argv) == 1:
        return print("Syntax :: dingonyms --site word")
    word = "search"
    methods = []
    for arg in sys.argv[1:]:
        # separate --params from search word
        if not arg or arg == "--":
            continue
        elif not re.match("-", arg):
            word = arg
        else:
            for name, method in vars(lookup.__class__).items():
                if re.match("^[/+–-]+(%s)" % method.__doc__, arg, re.X|re.I|re.U):
                    methods.append(name)
    if not methods:
        methods = ["thesaurus"]
    for run in methods:
        getattr(lookup, run)(word)
    pass
if __main__ == "__init__":
    __main__()

