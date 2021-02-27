import re
import string
import random

from .default import cached_tag, __extra__


def _get_random_name(length=10):
    """https://stackoverflow.com/a/23728630/2213647"""
    return ''.join(
        random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(length)
    )


@cached_tag.update(cache=True)
class style:
    def __init__(self, *, lang='css', scoped=False, children=''):
        if scoped:
            scoped, children = self._scope_style(children)
        self.lang = lang
        self.scoped = scoped
        self.children = children

    def _scope_style(self, styles):
        """https://stackoverflow.com/a/32134836/8851903"""
        style_name = _get_random_name()
        scoped_data = f'pyx-style="{style_name}"'
        css_rules = re.findall(r'[^\{]+\{[^\}]*\}', styles, re.MULTILINE)
        return (
            ('pyx-style', style_name),
            '\n'.join(
                ','.join(
                    (f'[{scoped_data}] {item}')
                    for item in rule.strip().split(',')
                )
                for rule in css_rules
            )
        )

    def __render__(self, tag):
        __extra__.js += f'''
            $('[pyx-id="{hash(tag)}"]').parent().attr{self.scoped}
        '''
        # __extra__.css += self.children
        return f'<style>{self.children}</style>'
