from django import template
register = template.Library()

@register.simple_tag(name='style')
def apply_stylesheet(styles):
    context = {
        'styles': styles,
    }
    return template.Template(context).render(template.Context())
