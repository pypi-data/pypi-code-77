import click
import os
import doctrans


@click.group()
def cli():
    pass


def _callback(ctx, param, value):
    opts = {
        "format": ["pdf", "docx"],
        "trans": ['google', 'kakao'],
        "doctool": ['pymupdf', 'pydocx'],
        "font": [os.path.splitext(font)[0] for font in os.listdir("doctrans/fonts")]
    }
    options = opts[param.name]
    while value not in options:
        value = input(f"{param} must be selected in {options} :")
    return value


def _callback_lang(ctx, param, value):
    src_options = ["auto", "en", "ko"]
    target_options = ["en", "ko"]

    if isinstance(value, tuple) and len(value) == 2:
        src, target = value
    else:
        src = target = None

    while src not in src_options:
        src = input(f"src lang must be selected in {src_options} :")
    while src not in src_options:
        target = input(f"target lang must be selected in {target_options} :")
    return src, target


def _get_files(initaildir="/") -> list:
    from tkinter import filedialog
    from tkinter import Tk
    root = Tk()
    root.filename = filedialog.askopenfilenames(
        initialdir=initaildir,
        title="choose your file",
        filetypes=(("pdf files", "*.pdf"), ("docx files", "*.docx"), ("all files", "*"))
    )
    root.withdraw()
    return list(root.filename)


def _get_pdf_files(initaildir="/") -> list:
    from tkinter import filedialog
    from tkinter import Tk
    root = Tk()
    root.filename = filedialog.askopenfilenames(
        initialdir=initaildir,
        title="choose your file",
        filetypes=(("pdf files", "*.pdf"), ("all files", "*"))
    )
    root.withdraw()
    return list(root.filename)


@click.command(name="mupdf")
@click.option('--format', '-f', prompt="result file format", callback=_callback, help='result file file format. ex) pdf or docx')
@click.option('--trans', '-t', prompt="text translator", callback=_callback, help='select text translator. ex) google or kakao')
@click.option('--lang', '-l', prompt="src lang, target lang", callback=_callback_lang, nargs=2, default=('auto', 'ko'), help='source language and target language ex) en ko')
@click.option('--font', default="malgun_gothic", callback=_callback, help='result font style')
@click.option('--nothread', is_flag=True, default=False, help="Not use multi-threading")
@click.argument('file_path', nargs=-1, type=click.Path(exists=True))
def mupdf_text(format, trans, lang, font, nothread, file_path):
    """python -m dotrans mupdf --format {pdf, docx} --trans {google, kakao} --lang {auto, en, ko} {en, ko} --font {malgun_gothic ...}
--thread FILEPATH"""
    doctrans.run(
        list(file_path),
        './results/',
        doc_trans=doctrans.DocTrans("pymupdf"),
        text_trans=doctrans.TextTrans(trans),
        font=doctrans.Font(font),
        format=doctrans.Extension('.' + format),
        from_lang=doctrans.Lang(lang[0]),
        to_lang=doctrans.Lang(lang[1]),
        use_thread=not nothread
    )


@click.command(name="mupdf-explorer")
@click.option('--format', '-f', prompt="result file format", callback=_callback, help='result file file format. ex) pdf or docx')
@click.option('--trans', '-t', prompt="text translator", callback=_callback, help='select text translator. ex) google or kakao')
@click.option('--lang', '-l', prompt="src lang, target lang", callback=_callback_lang, nargs=2, default=('auto', 'ko'), help='source language and target language ex) en ko')
@click.option('--font', default="malgun_gothic", callback=_callback, help='result font style')
@click.option('--nothread', is_flag=True, default=False, help="Not use multi-threading")
def mupdf_explorer(format, trans, lang, font, nothread):
    """python -m doctrans mupdf-explorer --format {pdf, docx} --trans {google, kakao} --lang {auto, en, ko} {en, ko} --font {malgun_gothic ...}
    --thread"""
    doctrans.run(
        list(_get_pdf_files()),
        './results/',
        doc_trans=doctrans.DocTrans("pymupdf"),
        text_trans=doctrans.TextTrans(trans),
        font=doctrans.Font(font),
        format=doctrans.Extension('.' + format),
        from_lang=doctrans.Lang(lang[0]),
        to_lang=doctrans.Lang(lang[1]),
        use_thread=not nothread
    )


@click.command(name="docx")
@click.option('--format', '-f', prompt="result file format", callback=_callback, help='result file file format. ex) pdf or docx')
@click.option('--trans', '-t', prompt="text translator", callback=_callback, help='select text translator. ex) google or kakao')
@click.option('--lang', '-l', prompt="src lang, target lang", callback=_callback_lang, nargs=2, default=('auto', 'ko'), help='source language and target language ex) en ko')
@click.option('--font', default="malgun_gothic", callback=_callback, help='result font style')
@click.option('--nothread', is_flag=True, default=False, help="Not use multi-threading")
@click.argument('file_path', nargs=-1, type=click.Path(exists=True))
def docx_text(format, trans, lang, font, nothread, file_path):
    """python -m doctrans docx --format {pdf, docx} --trans {google, kakao} --lang {auto, en, ko} {en, ko} --font {malgun_gothic ...}
--thread FILEPATH"""
    doctrans.run(
        list(file_path),
        './results/',
        doc_trans=doctrans.DocTrans("pydocx"),
        text_trans=doctrans.TextTrans(trans),
        font=doctrans.Font(font),
        format=doctrans.Extension('.' + format),
        from_lang=doctrans.Lang(lang[0]),
        to_lang=doctrans.Lang(lang[1]),
        use_thread=not nothread
    )


@click.command(name="docx-explorer")
@click.option('--format', '-f', prompt="result file format", callback=_callback, help='result file file format. ex) pdf or docx')
@click.option('--trans', '-t', prompt="text translator", callback=_callback, help='select text translator. ex) google or kakao')
@click.option('--lang', '-l', prompt="src lang, target lang", callback=_callback_lang, nargs=2, default=('auto', 'ko'), help='source language and target language ex) en ko')
@click.option('--font', default="malgun_gothic", callback=_callback, help='result font style')
@click.option('--nothread', is_flag=True, default=False, help="Not use multi-threading")
def docx_explorer(format, trans, lang, font, nothread):
    """python -m doctrans docx-explorer --format {pdf, docx} --trans {google, kakao} --lang {auto, en, ko} {en, ko} --font {malgun_gothic ...}
    --thread"""
    doctrans.run(
        list(_get_files()),
        './results/',
        doc_trans=doctrans.DocTrans("pydocx"),
        text_trans=doctrans.TextTrans(trans),
        font=doctrans.Font(font),
        format=doctrans.Extension('.' + format),
        from_lang=doctrans.Lang(lang[0]),
        to_lang=doctrans.Lang(lang[1]),
        use_thread=not nothread
    )


@click.command()
def quickstartpdf():
    """python -m doctrans quickstartpdf"""
    target_lang = input("select target language in ['ko', 'en']:")
    while target_lang not in ['ko', 'en']:
        target_lang = input("select target language in ['ko', 'en']:")
    doctrans.run(
        list(_get_pdf_files()),
        './results/',
        doc_trans=doctrans.DocTrans("pymupdf"),
        text_trans=doctrans.TextTrans("google"),
        font=doctrans.Font("malgun_gothic"),
        format=doctrans.Extension('.pdf'),
        from_lang=doctrans.Lang("auto"),
        to_lang=doctrans.Lang(target_lang),
        use_thread=True
    )


@click.command()
def quickstartdocx():
    """python -m doctrans quickstartdocx"""
    target_lang = input("select target language in ['ko', 'en']:")
    while target_lang not in ['ko', 'en']:
        target_lang = input("select target language in ['ko', 'en']:")
    doctrans.run(
        list(_get_files()),
        './results/',
        doc_trans=doctrans.DocTrans("pydocx"),
        text_trans=doctrans.TextTrans("google"),
        font=doctrans.Font("hy_shinmyeongjo"),
        format=doctrans.Extension('.pdf'),
        from_lang=doctrans.Lang("auto"),
        to_lang=doctrans.Lang(target_lang),
        use_thread=True
    )


cli.add_command(mupdf_text)
cli.add_command(mupdf_explorer)
cli.add_command(docx_text)
cli.add_command(docx_explorer)
cli.add_command(quickstartpdf)
cli.add_command(quickstartdocx)

if __name__ == "__main__":
    cli()
