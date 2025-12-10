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

@register.filter
def other_participant(conversation, user):
    """
    Devuelve el otro participante (User) en la conversación o None si no existe.
    """
    try:
        return conversation.participants.exclude(id=user.id).first()
    except Exception:
        return None

