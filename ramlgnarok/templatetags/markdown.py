from django import template
from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.lexers import get_lexer_for_mimetype
from pygments.formatters import HtmlFormatter

import markdown

register = template.Library()


@register.filter(is_safe=True)
def md(content):
    if content is not None:
        return mark_safe(markdown.markdown(
            content, [
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ],
        ))
    return ''


@register.filter(is_safe=True)
def example(body):
    if body:
        example = body.raw[body.mime_type].get('example', None)

        if example is not None:
            lexer = get_lexer_for_mimetype(body.mime_type, stripall=True)
            formatter = HtmlFormatter(linenos=False, cssclass="codehilite")
            return mark_safe(highlight(example, lexer, formatter))
    return ''
