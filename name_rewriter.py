from posixpath import split


filename_ml = "matrix_labels.txt"

# Open the .txt file in read mode
with open(filename_ml, 'r', encoding='utf-8') as file:
    # Read the content of the file and save it to a string
    text_content = file.read()

pieces = []

split_by_pavel = text_content.split("pavel pivarshev,\n")
for piece in split_by_pavel:
    piece_text = ""
    split_piece = piece.split("\n")
    for line in split_piece:
        if line != "":
            piece_text += line
            piece_text += "\n"
    pieces.append(piece_text[:-1])
        
# for piece in pieces:
#     print(piece)

output_prefix = "<div class=\"scroll-item\">\n <table><tr><td id=\"vert-description\">\n"
bold = "<b><i>"
br = "<br>"
unbold = "</i></b>"
output_suffix = "</td><td id=\"vert-image\">\n <a target=\"_blank\" href=\"artworks/individual panels/___\">\n<img src=\"artworks/individual panels/___\"></a>\n</td></tr></table>\n</div>\n\n"

piece_info_list = []

for piece in pieces:
    split_line = piece.split("\n")
    date = split_line[-1]
    piece_info = ""
    piece_info += output_prefix
    piece_info += bold
    for line in split_line:
        piece_info += line
        piece_info += br
    piece_info += unbold
    piece_info += br
    piece_info += br
    piece_info += date
    piece_info += output_suffix
    piece_info_list.append(piece_info)

print("\n\n\n\n\n\n\n\n")

for p in piece_info_list[60:]:
    print(p)

