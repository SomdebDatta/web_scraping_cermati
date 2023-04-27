def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(clean, '', text)