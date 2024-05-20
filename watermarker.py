import sys
import os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_image_size(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height


def add_watermark(in_path: str, out_path: str, logo_path: str, position='center', width_percent=50):
    """
    logo is a transparent png image
    add watermark to the center of the image, so that the watermark is 50% of the width of the image
    vertically centered
    """

    img = Image.open(in_path)

    # rotate image based on exif (we don't preserve exif data in the output image)
    width, height = get_image_size(in_path)
    try:
        exif = img._getexif()
        orientation_key = 274
        if exif and orientation_key in exif:
            orientation = exif[orientation_key]

            rotate_values = {
                3: 180,
                6: 270,
                8: 90
            }

            if orientation in rotate_values:
                img = img.rotate(rotate_values[orientation], expand=True)

            if orientation in [6, 8]:
                width, height = height, width
    except:
        print('Error reading exif data')
        pass


    logo = Image.open(logo_path)
    logo = logo.convert('RGBA')
    logo_width = width * (width_percent / 100)
    logo_height = logo_width * logo.height / logo.width
    logo = logo.resize((int(logo_width), int(logo_height)))


    if position == 'center':
        img.paste(logo, (int((width - logo_width) / 2), int((height - logo_height) / 2)), logo)
    elif position == 'bottom_right':
        img.paste(logo, (width - int(logo_width), height - int(logo_height)), logo)
    elif position == 'bottom_left':
        img.paste(logo, (0, height - int(logo_height)), logo)
    elif position == 'top_right':
        img.paste(logo, (width - int(logo_width), 0), logo)
    elif position == 'top_left':
        img.paste(logo, (0, 0), logo)
    else:
        print('Invalid position')
    img.save(out_path, "JPEG", quality=90)  # exif data is removed


def main():
    # drag and drop files on the script
    files = sys.argv[1:]
    for filepath in files:
        if os.path.isfile(filepath):
            if filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.tif', '.webp')):
                print(f'Processing image: {filepath}')
                add_watermark(filepath, filepath, 'logo.png')
            else:
                print(f'File not supported: {filepath}')
        else:
            print(f'File not found: {filepath}')

    print('Done')

    # input('Press Enter to exit')  # uncomment to keep the window open to debug


if __name__ == '__main__':
    main()