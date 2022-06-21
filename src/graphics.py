from PIL import Image, ImageDraw, ImageFont

base_font_size = 12


def get_bounds(blocks, scale=1.0):
    max_y = int(max([block.positionY + block.height for block in blocks]) * scale)
    max_x = int(max([block.positionX + block.width for block in blocks]) * scale)
    return (max_x, max_y)


def draw_block(block, img_size, img_d, scale=1.0, fontscale=1.0):
    # Invert Y coordinate, because for pil 0,0 is top left corner of screen,
    top_left_x = int(block.positionX * scale)
    top_left_y = int(img_size[1] - (block.positionY + block.height) * scale)
    bottom_right_y = int(img_size[1] - block.positionY * scale)
    bottom_right_x = int((block.positionX + block.width) * scale)
    shape = [(top_left_x, top_left_y), (bottom_right_x, bottom_right_y)]
    img_d.rectangle(shape, fill="white", outline="black")

    center_x = top_left_x + (bottom_right_x - top_left_x) / 2
    center_y = top_left_y + (bottom_right_y - top_left_y) / 2

    fnt = ImageFont.truetype("Keyboard.ttf", int(base_font_size * fontscale))

    w, h = img_d.textsize(block.name, font=fnt)
    img_d.text((center_x - (w / 2), center_y - (h / 2)), block.name, fill="black", font=fnt)


def placement_visualisation(filename, blocks, connections=None, scale=1.0, fontscale=1.0):
    img_size = get_bounds(blocks, scale)
    image = Image.new("RGB", img_size, color=(192, 192, 192))
    img_d = ImageDraw.Draw(image)

    for block in blocks:
        draw_block(block, img_size, img_d, scale, fontscale)

    image.save(filename)


def get_eval(blocks):
    x, y = get_bounds(blocks, 1.0)
    return x * y


# return sum of blocks areas
def get_ideal_eval(blocks):
    area = 0
    for block in blocks:
        area += block.width * block.height
    return area
