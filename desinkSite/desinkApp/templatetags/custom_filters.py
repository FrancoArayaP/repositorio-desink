from django import template

register = template.Library()

@register.filter
def clp_format(value):
    try:
        # Convertir a entero
        value = int(float(value))
        # Formatear con separador de miles usando puntos
        return "${:,}".format(value).replace(",", ".")
    except (ValueError, TypeError):
        return value
