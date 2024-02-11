from django import template
import json

register = template.Library()

@register.filter
def parse_json(json_string):
    try:
        return json.loads(json_string)
    except ValueError:
        return {}