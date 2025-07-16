import json
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def quill_to_html(value):
    """
    Convert Quill JSON content to HTML
    """
    if not value:
        return ""
    
    try:
        # Try to parse as JSON
        content = json.loads(value)
        if isinstance(content, dict) and 'ops' in content:
            # Extract text from Quill JSON
            text = ""
            for op in content['ops']:
                if 'insert' in op:
                    if isinstance(op['insert'], str):
                        text += op['insert']
                    elif isinstance(op['insert'], dict) and 'image' in op['insert']:
                        text += f'<img src="{op["insert"]["image"]}" alt="Image">'
            
            # Convert line breaks to <br> tags
            text = text.replace('\n', '<br>')
            return mark_safe(text)
        else:
            # If it's not Quill JSON, return as plain text
            return mark_safe(value.replace('\n', '<br>'))
    except (json.JSONDecodeError, TypeError):
        # If it's not valid JSON, return as plain text
        return mark_safe(value.replace('\n', '<br>'))

@register.filter
def quill_to_text(value):
    """
    Convert Quill JSON content to plain text
    """
    if not value:
        return ""
    
    try:
        # Try to parse as JSON
        content = json.loads(value)
        if isinstance(content, dict) and 'ops' in content:
            # Extract text from Quill JSON
            text = ""
            for op in content['ops']:
                if 'insert' in op and isinstance(op['insert'], str):
                    text += op['insert']
            return text
        else:
            # If it's not Quill JSON, return as is
            return value
    except (json.JSONDecodeError, TypeError):
        # If it's not valid JSON, return as is
        return value 