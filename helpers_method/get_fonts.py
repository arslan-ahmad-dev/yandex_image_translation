import math
from PIL import ImageFont

def get_text_color(background_color):
    text_color = get_contrast_color(background_color)
    return text_color

def calculate_contrast_ratio(luminance1, luminance2):
    brighter = max(luminance1, luminance2)
    darker = min(luminance1, luminance2)
    contrast_ratio = (brighter + 0.05) / (darker + 0.05)
    return contrast_ratio


def gamma_correction(color):
    corrected_color = color / 255
    if corrected_color <= 0.03928:
        return corrected_color / 12.92
    else:
        return ((corrected_color + 0.055) / 1.055) ** 2.4


def calculate_relative_luminance(red, green, blue):
    red_linear = gamma_correction(red)
    green_linear = gamma_correction(green)
    blue_linear = gamma_correction(blue)

    luminance = 0.2126 * red_linear + 0.7152 * green_linear + 0.0722 * blue_linear
    return luminance


def get_box_size(box):
    box_height = int(math.sqrt((box[0][0] - box[3][0]) ** 2 + (box[0][1] - box[3][1]) ** 2))
    box_width = int(math.sqrt((box[0][0] - box[1][0]) ** 2 + (box[0][1] - box[1][1]) ** 2))
    if box_height > 2 * box_width and box_height > 30:
        return (box_height, box_width)
    else:
        return (box_width, box_height)


def create_font(text, desired_size, font_path):
    font_size = int(desired_size[1] * 0.99)
    font = ImageFont.truetype(font_path, font_size, encoding="utf-8")
    
    bounding_box = font.getbbox(text)
    text_width = bounding_box[2] - bounding_box[0]
    
    if text_width > desired_size[0]:
        font_size = int((font_size * desired_size[0]) / text_width)
        font = ImageFont.truetype(font_path, font_size, encoding="utf-8")

    return font


def get_contrast_color(rgb_color):
    red = rgb_color[0]
    green = rgb_color[1]
    blue = rgb_color[2]

    luminance = calculate_relative_luminance(red, green, blue)

    contrast_white = calculate_contrast_ratio(luminance, 1.0)
    contrast_black = calculate_contrast_ratio(luminance, 0.0)

    text_color = "white" if contrast_white > contrast_black else "black"

    return text_color
