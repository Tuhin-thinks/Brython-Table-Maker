import json
from typing import Literal, List, Any, Union
from browser import document


def get_md_table(_header: List[str], _items: List[List[Union[str, Any]]],
                 padding=10, fill_char="",
                 alignment: Literal['left', 'right', 'center'] = "center"):
    """
    To generate a table for markdown.
    :param _header:
    :param _items:
    :param padding:
    :param fill_char:
    :param alignment:
    :return:
    """

    def __get_padding_line():
        sep_formatter = "|{:" + fill_char + str(padding) + "}"
        header_separator = ""

        for_center = lambda: ":" + "-" * (padding - 2) + ":"
        for_right = lambda: "-" * (padding - 1) + ":"
        for_left = lambda: ":" + "-" * (padding - 1)

        # this is also responsible for adding the padding line & alignment of cell contents
        fill_char_list = for_center() if alignment == "center" else for_left() if alignment == "left" else for_right()

        for _ in _header:
            header_separator += sep_formatter
        header_separator += "|"
        header_separator = header_separator.format(*[fill_char_list for _ in _header])

        return header_separator

    header_formatter = ""

    if alignment == "center":
        align_char = "^"
    elif alignment == "right":
        align_char = ">"
    else:
        align_char = "<"

    for _head in _header:
        _str = "|{:^" + str(padding) + "}"
        header_formatter += _str.format(_head)
    header_formatter += "|"

    row_formatter = ""
    for _ in _header:
        row_formatter += "|{:" + align_char + str(padding) + "}"
    row_formatter = row_formatter + "|"

    rows = ""
    for item_info in _items:
        # if there is item missing add an empty string at the end
        padded_item_info = item_info + [""] * (len(_header) - len(item_info))
        rows += row_formatter.format(*padded_item_info)
        rows += "\n"

    return header_formatter + "\n" + __get_padding_line() + "\n" + rows


def convert_md_table():
    """
    Function to convert JSON data into markdown table.
    """
    header = document['col-names'].innerText.split(",")

    # load items from json input, text area
    items = json.loads(document['items-no-display'].innerText)
    print(items)
    # load padding from input
    padding = int(document['padding'].value)
    # load alignment from input
    alignment = document['alignment'].value

    print(header, items, padding, alignment)

    # get the markdown table
    md_table = get_md_table(_header=header, _items=items,
                            padding=padding, alignment=alignment)

    # set the markdown table to the output text area
    document['md'].value = md_table


def clear_input():
     document['md'].value = ""
     print("Input cleared!")


# these 2 lines are equivalent to adding onclick function on javascript
document['convert-md'].bind('click', lambda ev: convert_md_table())
document['clear'].bind('click', lambda ev: clear_input())
