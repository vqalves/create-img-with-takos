from PIL import Image # Pillow
import random

def CreateRotatedTako(tako_img, rotation):
    return tako_img.rotate(rotation, expand=True)

def RandomAngle():
    return random.randint(0, 365)

def CreateCanvas(width, height):
    return Image.new('RGBA', (width, height), (255, 255, 255, 0))
    
def AddToCanvas(canvas, img, x, y):
    offset = (x,y)
    # Pillow requires a 3rd parameter to properly work with transparent pixels
    canvas.paste(img, offset, img)

def SaveCanvas(canvas, canvas_path):
    canvas.save(canvas_path)

def Generate():
    tako_img_path = 'Big lone tako.png'
    canvas_path = 'Many takos.png'

    tako_img = Image.open(tako_img_path)
    tako_width, tako_height = tako_img.size

    takos_per_line = 10
    takos_per_column = 10

    # Resize tako to create a smaller canvas
    resize_tako_to = 0.2
    tako_width = int(tako_width * resize_tako_to)
    tako_height = int(tako_height * resize_tako_to)
    tako_img.thumbnail((tako_width, tako_height), Image.ANTIALIAS)

    # How much of the tako should be overlapping. Overlapping helps to avoid blank spots
    # Recommended between 0 and 1. Nearer 0 makes them stack more, bigger than 1 will create distance between them
    visible_tako = 0.45
    visible_tako_width = int(tako_width * visible_tako)
    visible_tako_height = int(tako_height * visible_tako)

    canvas_width = int(takos_per_line * visible_tako_width) + tako_width
    canvas_height = int(takos_per_column * visible_tako_height) + tako_height

    print(f"Creating canvas -> w:{canvas_width} h:{canvas_height}")
    canvas = CreateCanvas(canvas_width, canvas_height)

    # Variable to enumerate any tako placed outside the canvas
    out_of_bound_takos = 0

    # Randomizing which order the takos are placed makes the overlapping look more natural
    coordinate_list = []
    for x in range(0, takos_per_line):
        for y in range(0, takos_per_column):
            coordinate_list.append((x, y))
            
    random.shuffle(coordinate_list)

    for coordinates in coordinate_list:
        x, y = coordinates

        # Specify additional offsets for each tako, for example to exceed the canvas range
        additional_offset_x = 0
        additional_offset_y = 0

        offset_x = int(x * visible_tako_width) + additional_offset_x
        offset_y = int(y * visible_tako_height) + additional_offset_y

        if(offset_x < 0 or offset_y < 0 or offset_x + tako_width > canvas_width or offset_y + tako_height > canvas_height):
            out_of_bound_takos += 1

        angle = RandomAngle()
        rotated_tako = CreateRotatedTako(tako_img, angle)
        AddToCanvas(canvas, rotated_tako, offset_x, offset_y)

    SaveCanvas(canvas, canvas_path)
    print(f"Out of bound: {out_of_bound_takos}")

Generate()