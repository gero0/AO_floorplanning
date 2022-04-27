from PIL import Image, ImageDraw


def get_bounds(blocks):
    max_y = max([block.positionY + block.height for block in blocks])
    max_x = max([block.positionX + block.width for block in blocks])
    return (max_x, max_y)


def draw_block(block, img_size, img_d):
    # Invert Y coordinate, because for pil 0,0 is top left corner of screen,
    top_left_x = block.positionX
    top_left_y = img_size[1] - (block.positionY + block.height)
    bottom_right_y = img_size[1] - block.positionY
    bottom_right_x = block.positionX + block.width
    shape = [(top_left_x, top_left_y), (bottom_right_x, bottom_right_y)]
    img_d.rectangle(shape, fill="white", outline="black")

    center_x = top_left_x + (bottom_right_x - top_left_x) / 2
    center_y = top_left_y + (bottom_right_y - top_left_y) / 2

    print(bottom_right_y, top_left_y, center_y)

    w, h = img_d.textsize(block.name)
    img_d.text((center_x - (w / 2), center_y - (h / 2)), block.name, fill="black")


def placement_visualisation(filename, blocks, connections=None):
    img_size = get_bounds(blocks)
    image = Image.new("RGB", img_size, color=(192, 192, 192))
    img_d = ImageDraw.Draw(image)

    for block in blocks:
        draw_block(block, img_size, img_d)

    image.save(filename)
