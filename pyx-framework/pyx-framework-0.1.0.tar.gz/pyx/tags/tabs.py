from .all import li, ul, div, a
from ..utils import state, ChildrenComponent, __extra__
from ..main import cached_tag
from .default import DEFAULT_TAG
from .script import script


@cached_tag
def tab(*, name, children, on_click=None, url=None, href=None):
    return li(children=(
        a(children=name, href=href) if href else name
    ))


@DEFAULT_TAG.update(is_in_dom=True)
def tabs(tag, selected=None, children=(), _class=''):
    if selected is None and children:
        selected = children[0].kw.name
    tag.selected = state(selected)

    for child in children:
        child.kw.active = tag.selected == child.kw.name
        child.kw.on_click = lambda t=child: set_selected(t)

    def set_selected(t):
        tag.selected = t.kw.name
        return 'selected: ' + str(tag.selected)

    return [
        ul(children=children),
        div(_class=_class, children=ChildrenComponent([
            child.kw.get('children')
            for child in children
            if not isinstance(child, str) and child.kw.active
        ])),
        script(children='''
            const activeTab = $('tab[active]')
            const name = activeTab.attr('name')
            window.history.pushState(name, name, activeTab.attr('url'))
            function handleToggleTab() {
                $('tab').off('click::after').on('click::after', (e, { self }) => {
                    if (self.attr('active')) {
                        console.log(self)
                    }
                    const name = self.attr('name')
                    window.history.pushState(name, name, self.attr('url'))
                    handleToggleTab() // after reload old jQuery not working
                })
            }
            handleToggleTab()
        ''')
    ]
