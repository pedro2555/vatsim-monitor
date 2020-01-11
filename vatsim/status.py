from random import choice
import itertools
import requests

from vatsim import STATUS_SERVERS

def status():

    # get information file from vatsim, process it to a clearer version by
    # removing redundant lines
    url = _pick_url()
    raw = _download(url)
    
    # split the file into groups, one group per client type
    sections = _split_sections(raw)

    return sections

def _pick_url():
    """Returns a random VATSIM status url from a list of known urls.
    
    See `vatsim.STATUS_SERVERS` for a complete list of servers.
    """
    return choice(STATUS_SERVERS)

def _download(url):
    """Fetches the given URL. Returns iterable for 200 responses."""
    # if the response is empty, stop the iterator
    resp = requests.get(url)
    if resp.status_code != 200:
        return

    # return a iterator for the downloaded status file
    yield from resp.iter_lines(decode_unicode=True)
        
def _split_sections(iterator):
    # group the iterator into ordered section headers and section items
    groups = itertools.groupby(iterator, _is_section_header)

    for is_section_header, value in groups:

        # capture the start of a new section
        # ie. !GENERAL:
        if is_section_header:

            # grab the actual section name by truncating 1st and last chars
            section = next(value)[1:-1]

            # the section items are in the next group
            _, items = next(groups)

            # clean comments, and empty lines
            # items = filter(_is_empty, items)

            yield section, filter(_is_empty, list(items))

def _is_section_header(line):
    return line.startswith('!')

def _is_empty(line):
    _line = line.strip()
    
    # empty _lines occur rather frequently
    is_empty = _line == ''

    # lines starting with a ';' are comments
    is_comment = _line.startswith(';')

    return not is_empty and not is_comment

