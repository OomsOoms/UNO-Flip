from PIL import Image


def get_sprite_coordinates(x, y, gap):
    sprite_width = 331
    sprite_height = 512
    left = x * (sprite_width + gap)
    top = y * (sprite_height + gap)
    right = left + sprite_width
    bottom = top + sprite_height
    return (left, top, right, bottom)


# Left, Top, Right, Bottom
light_side = Image.open("Textures\Light-side.png")


light_side = light_side.crop(get_sprite_coordinates(0, 5, 5))

light_side.save("Textures/Single-card.png")
