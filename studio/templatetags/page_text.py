from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()


class EditableTextNode(template.Node):
    def __init__(self, key, nodes):
        self.key = key
        self.nodes = nodes

    def render(self, context):
        item = context.get('page_text', {}).get(self.key)
        if item is None or item['text'] == item['default_text']:
            return self.nodes.render(context)
        # Editors supply plain text; never execute their HTML or template code.
        return mark_safe(str(escape(item['text'])).replace('\r\n', '\n').replace('\n', '<br>'))


@register.tag
def editable_text(parser, token):
    parts = token.split_contents()
    if len(parts) != 2 or parts[1][0] not in ('"', "'"):
        raise template.TemplateSyntaxError('editable_text requires a quoted key')
    nodes = parser.parse(('endeditable_text',))
    parser.delete_first_token()
    return EditableTextNode(parts[1][1:-1], nodes)
