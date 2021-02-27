import re

from ..utils import __extra__
from ..main import cached_tag, Component, Tag


DEFAULT_HEAD = '''
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script type="text/javascript" src="/static/js/pyx.js"></script>
<script type="text/typescript" src="/static/js/test.ts"></script>
<link type="text/css" rel="stylesheet" href="/static/css/pyx.css"/>
<style>
    {extra_css}
</style>
{extra_head}
'''

__extra__.css = ''
__extra__.head = ''

DEFAULT_BODY = '''
<error>
    <render_error/>
</error>
<script>
    {extra_js}
</script>
{extra_body}
'''

__extra__.js = ''
__extra__.body = ''

DEFAULT_TAG = cached_tag.update(is_in_dom=False, children_raw=True)
VOID_TAG = DEFAULT_TAG.update(_void_tag=True)


@DEFAULT_TAG.update(name='input')
def inp(**k):
    return


@Tag
def python(tag, **k):
    __locals = {}
    __globals = globals().copy()
    if '_locals' in k:
        __globals.update(tag.kw.pop('_locals'))
    if 'src' in k:
        with open(k['src'], 'r') as src:
            code = '\n'.join('    ' + line for line in src.readlines())
    else:
        children = str(k.get('children', ''))
        tabs = re.search('\n?(?P<spaces> *)', children).group('spaces')
        code = re.sub('^' + tabs, '    ', children, flags=re.MULTILINE)
    exec(f'''
def __python__():
{code}
''', __globals, __locals)
    return __locals['__python__']()


@DEFAULT_TAG
def render_error(traceback, **k):
    return f'ERROR:\n  traceback: {traceback}\n  kwargs: {k}'


@DEFAULT_TAG
class __fragment__:
    def __init__(self, tag, **k):
        self.children = tag.kw.pop('children')

    def __render__(self, tag: Tag):
        return self.children


@cached_tag.update(name='head', children_raw=True)
def __head__(*, children=''):
    return DEFAULT_HEAD.format(
        extra_css=__extra__.css,
        extra_head=__extra__.head,
    ) + children


@cached_tag.update(name='body', children_raw=True)
def __body__(*, children=''):
    return children + DEFAULT_BODY.format(
        extra_js=__extra__.js,
        extra_body=__extra__.body,
    )


@cached_tag.update(name='html', children_raw=True)
def __html__(*, head='', children=''):
    __extra__.css = ''
    __extra__.head = ''
    __extra__.js = ''
    __extra__.body = ''
    _body = __body__(children=str(children))
    _head = __head__(children=str(head))
    return [_head, _body]
