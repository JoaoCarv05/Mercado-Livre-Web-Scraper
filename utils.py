def get_text_or_default(elements, index, default="não consta", attribute=None):
    try:
        if attribute:
            return elements[index][attribute]
        return elements[index].get_text()
    except IndexError:
        return default