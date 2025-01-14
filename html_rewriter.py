from posixpath import split
from typing import final


filename_ml = "matrix_html.txt"

# Open the .txt file in read mode
with open(filename_ml, 'r', encoding='utf-8') as file:
    # Read the content of the file and save it to a string
    text_content = file.read()

pieces = []

split_by_div = text_content.split("</div>")
del split_by_div[-1]
for piece in split_by_div:
    # isolate vert-desc & by vert-image
    split1 = piece.split("</td>")
    first_half = split1[0]
    second_half = split1[1]
    vert_description = first_half.split("<tr>")[1]
    vert_description += "</td>"
    vert_image = second_half
    vert_image += "</td>"
    pieces.append((vert_description, vert_image))

final_text_string = ""

prefix = "<div class=\"scroll-item\"><table><tr>"
suffix = "</tr></table></div>"

for d, i in pieces:
    final_code = prefix + i + d + suffix
    final_text_string += final_code
    final_text_string += "\n"

print(final_text_string)

