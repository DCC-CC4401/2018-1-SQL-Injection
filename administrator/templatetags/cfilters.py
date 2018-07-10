from django import template
from django.template.defaultfilters import stringfilter
from inventario_cei.models import Reserve

register = template.Library()

@register.filter
@stringfilter
def reserveState(value): # Only one argument.
    """Converts a string into all lowercase"""
    # return Reserve.get_state_display(value)
    return {'a':'Aceptada',
        'r':'Rechazada',
        'p':'Pendiente'} [value]


