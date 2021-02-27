from .default import DEFAULT_TAG, VOID_TAG


@DEFAULT_TAG
def a(href=None, children='', **k):
    return str(children)


@DEFAULT_TAG
def abbr(children='', **k):
    return str(children)


@DEFAULT_TAG
def acronym(children='', **k):
    return str(children)


@DEFAULT_TAG
def address(children='', **k):
    return str(children)


@DEFAULT_TAG
def applet(children='', **k):
    return str(children)


@VOID_TAG
def area(children='', **k):
    return str(children)


@DEFAULT_TAG
def article(children='', **k):
    return str(children)


@DEFAULT_TAG
def aside(children='', **k):
    return str(children)


@DEFAULT_TAG
def audio(children='', **k):
    return str(children)


@DEFAULT_TAG
def b(children='', **k):
    return str(children)


@VOID_TAG
def base(children='', **k):
    return str(children)


@DEFAULT_TAG
def basefont(children='', **k):
    return str(children)


@DEFAULT_TAG
def bdi(children='', **k):
    return str(children)


@DEFAULT_TAG
def bdo(children='', **k):
    return str(children)


@DEFAULT_TAG
def big(children='', **k):
    return str(children)


@DEFAULT_TAG
def blockquote(children='', **k):
    return str(children)


@DEFAULT_TAG
def body(children='', **k):
    return str(children)


@VOID_TAG
def br(children='', **k):
    return str(children)


@DEFAULT_TAG.update(is_in_dom=True)
def button(children='', **k):
    return str(children)


@DEFAULT_TAG
def canvas(children='', **k):
    return str(children)


@DEFAULT_TAG
def caption(children='', **k):
    return str(children)


@DEFAULT_TAG
def center(children='', **k):
    return str(children)


@DEFAULT_TAG
def cite(children='', **k):
    return str(children)


@DEFAULT_TAG
def code(children='', **k):
    return str(children)


@VOID_TAG
def col(children='', **k):
    return str(children)


@DEFAULT_TAG
def colgroup(children='', **k):
    return str(children)


@DEFAULT_TAG
def data(children='', **k):
    return str(children)


@DEFAULT_TAG
def datalist(children='', **k):
    return str(children)


@DEFAULT_TAG
def dd(children='', **k):
    return str(children)


@DEFAULT_TAG.update(name='del')
def _del(children='', **k):
    return str(children)


@DEFAULT_TAG
def details(children='', **k):
    return str(children)


@DEFAULT_TAG
def dfn(children='', **k):
    return str(children)


@DEFAULT_TAG
def dialog(children='', **k):
    return str(children)


@DEFAULT_TAG
def dir(children='', **k):
    return str(children)


@DEFAULT_TAG
def div(children='', **k):
    return str(children)


@DEFAULT_TAG
def dl(children='', **k):
    return str(children)


@DEFAULT_TAG
def dt(children='', **k):
    return str(children)


@DEFAULT_TAG
def em(children='', **k):
    return str(children)


@VOID_TAG
def embed(children='', **k):
    return str(children)


@DEFAULT_TAG
def fieldset(children='', **k):
    return str(children)


@DEFAULT_TAG
def figcaption(children='', **k):
    return str(children)


@DEFAULT_TAG
def figure(children='', **k):
    return str(children)


@DEFAULT_TAG
def font(children='', **k):
    return str(children)


@DEFAULT_TAG
def footer(children='', **k):
    return str(children)


@DEFAULT_TAG
def form(children='', **k):
    return str(children)


@DEFAULT_TAG
def frame(children='', **k):
    return str(children)


@DEFAULT_TAG
def frameset(children='', **k):
    return str(children)


@DEFAULT_TAG
def h1(children='', **k):
    return str(children)


@DEFAULT_TAG
def h2(children='', **k):
    return str(children)


@DEFAULT_TAG
def h3(children='', **k):
    return str(children)


@DEFAULT_TAG
def h4(children='', **k):
    return str(children)


@DEFAULT_TAG
def h5(children='', **k):
    return str(children)


@DEFAULT_TAG
def h6(children='', **k):
    return str(children)


@DEFAULT_TAG
def head(children='', **k):
    return str(children)


@DEFAULT_TAG
def header(children='', **k):
    return str(children)


@VOID_TAG
def hr(children='', **k):
    return str(children)


@DEFAULT_TAG
def html(children='', **k):
    return str(children)


@DEFAULT_TAG
def i(children='', **k):
    return str(children)


@DEFAULT_TAG
def iframe(children='', **k):
    return str(children)


@VOID_TAG
def img(children='', **k):
    return str(children)


@VOID_TAG.update(name='input')
def _input(children='', **k):
    return str(children)


@DEFAULT_TAG
def ins(children='', **k):
    return str(children)


@DEFAULT_TAG
def kbd(children='', **k):
    return str(children)


@DEFAULT_TAG
def label(children='', **k):
    return str(children)


@DEFAULT_TAG
def legend(children='', **k):
    return str(children)


@DEFAULT_TAG
def li(children='', **k):
    return str(children)


@VOID_TAG
def link(children='', **k):
    return str(children)


@DEFAULT_TAG
def main(children='', **k):
    return str(children)


@DEFAULT_TAG.update(name='map')
def _map(children='', **k):
    return str(children)


@DEFAULT_TAG
def mark(children='', **k):
    return str(children)


@VOID_TAG
def meta(children='', **k):
    return str(children)


@DEFAULT_TAG
def meter(children='', **k):
    return str(children)


@DEFAULT_TAG
def nav(children='', **k):
    return str(children)


@DEFAULT_TAG
def noframes(children='', **k):
    return str(children)


@DEFAULT_TAG
def noscript(children='', **k):
    return str(children)


@DEFAULT_TAG
def object(children='', **k):
    return str(children)


@DEFAULT_TAG
def ol(children='', **k):
    return str(children)


@DEFAULT_TAG
def optgroup(children='', **k):
    return str(children)


@DEFAULT_TAG
def option(children='', **k):
    return str(children)


@DEFAULT_TAG
def output(children='', **k):
    return str(children)


@DEFAULT_TAG
def p(children='', **k):
    return str(children)


@VOID_TAG
def param(children='', **k):
    return str(children)


@DEFAULT_TAG
def picture(children='', **k):
    return str(children)


@DEFAULT_TAG
def pre(children='', **k):
    return str(children)


@DEFAULT_TAG
def progress(children='', **k):
    return str(children)


@DEFAULT_TAG
def q(children='', **k):
    return str(children)


@DEFAULT_TAG
def rp(children='', **k):
    return str(children)


@DEFAULT_TAG
def rt(children='', **k):
    return str(children)


@DEFAULT_TAG
def ruby(children='', **k):
    return str(children)


@DEFAULT_TAG
def s(children='', **k):
    return str(children)


@DEFAULT_TAG
def samp(children='', **k):
    return str(children)


@DEFAULT_TAG
def section(children='', **k):
    return str(children)


@DEFAULT_TAG
def select(children='', **k):
    return str(children)


@DEFAULT_TAG
def small(children='', **k):
    return str(children)


@VOID_TAG
def source(children='', **k):
    return str(children)


@DEFAULT_TAG
def span(children='', **k):
    return str(children)


@DEFAULT_TAG
def strike(children='', **k):
    return str(children)


@DEFAULT_TAG
def strong(children='', **k):
    return str(children)


@DEFAULT_TAG
def sub(children='', **k):
    return str(children)


@DEFAULT_TAG
def summary(children='', **k):
    return str(children)


@DEFAULT_TAG
def sup(children='', **k):
    return str(children)


@DEFAULT_TAG
def svg(children='', **k):
    return str(children)


@DEFAULT_TAG
def table(children='', **k):
    return str(children)


@DEFAULT_TAG
def tbody(children='', **k):
    return str(children)


@DEFAULT_TAG
def td(children='', **k):
    return str(children)


@DEFAULT_TAG
def template(children='', **k):
    return str(children)


@DEFAULT_TAG
def textarea(children='', **k):
    return str(children)


@DEFAULT_TAG
def tfoot(children='', **k):
    return str(children)


@DEFAULT_TAG
def th(children='', **k):
    return str(children)


@DEFAULT_TAG
def thead(children='', **k):
    return str(children)


@DEFAULT_TAG
def time(children='', **k):
    return str(children)


@DEFAULT_TAG
def title(children='', **k):
    return str(children)


@DEFAULT_TAG
def tr(children='', **k):
    return str(children)


@VOID_TAG
def track(children='', **k):
    return str(children)


@DEFAULT_TAG
def tt(children='', **k):
    return str(children)


@DEFAULT_TAG
def u(children='', **k):
    return str(children)


@DEFAULT_TAG
def ul(children='', **k):
    return str(children)


@DEFAULT_TAG
def var(children='', **k):
    return str(children)


@DEFAULT_TAG
def video(children='', **k):
    return str(children)


@VOID_TAG
def wbr(children='', **k):
    return str(children)