from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

register = template.Library()

def fill(template, path):
    static_path = staticfiles_storage.url(path)
    return template % static_path

@register.simple_tag
def include_script(script_name):
    src = script_name + ".js"
    return fill("""<script type="text/javascript" src="%s"></script>""", src)

@register.simple_tag
def include_style(style_name):
    href = style_name + ".css"
    return fill("""<link type="text/css" rel="stylesheet" href="%s" />""", href)