from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="add_class")
def add_class(field, css):
    """Add CSS classes to Django form fields easily in templates.

    This filter is defensive: if `field` is a BoundField it calls
    `as_widget(attrs={...})`. If `field` is already a rendered string
    (or doesn't expose `as_widget`) we return it unchanged.
    """
    # BoundField exposes as_widget; strings and plain values do not.
    as_widget = getattr(field, "as_widget", None)
    if callable(as_widget):
        try:
            return as_widget(attrs={"class": css})
        except Exception:
            # In case widget rendering fails, fall back to original value
            return field
    # Not a BoundField (already rendered or simple value) — return as-is
    return mark_safe(field)
