import re


def shorten_text(text, maxchars, ellipsis=' ...'):
    """ Returns first few words from the `text`, but no more than `maxchars`, and appends
        an `ellipsis`. This function works only on plain text (no HTML!), removes any leading
        and trailing spaces, and squashes any number of consequent whitespaces (including
        newlines) into a single space.

        :param text: Input string, possibly quite long.
        :param maxchars: Maximum length or result string.
        :param ellipsis: Trailing sign to indicate implied continuation.
        :return: Shortened substring with squashed whitespaces.
    """
    if not isinstance(text, str) or maxchars <= 0:
        return ''
    if not isinstance(ellipsis, str):
        ellipsis = ''

    if len(text) > maxchars:
        counter = i = 0
        for char in text:
            if not char.isspace():
                counter += 1
            i += 1
            if counter >= maxchars:
                break
        text = text[:i]

    text = re.sub(r'\s+', ' ', text).strip()[:maxchars+1]

    index_of_last_space = text.rfind(' ')
    if index_of_last_space > 0:
        return text[:index_of_last_space] + ellipsis
    else:
        return text[:maxchars] + ellipsis

