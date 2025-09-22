from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Adds the argument to the value."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def calc_delay(value, multiplier=100, offset=0):
    """Calculate animation delay: (value * multiplier) + offset"""
    try:
        return (int(value) * int(multiplier)) + int(offset)
    except (ValueError, TypeError):
        return 0

@register.filter
def animation_delay(counter, base_delay=100):
    """Generate staggered animation delays for loops"""
    try:
        return int(counter) * int(base_delay)
    except (ValueError, TypeError):
        return 0