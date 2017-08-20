from django import template

register = template.Library()


@register.inclusion_tag('material_forms/input_text.html')
def input_text(field, label=None):
    if not label:
        label = field.label
    return {
        'field': field,
        'label': label,
    }


@register.inclusion_tag('material_forms/submit.html')
def submit(text="Submit"):
    return {'text': text, }
