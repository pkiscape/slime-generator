"""
=========================================================
Slime
Slime Image Creator
Actions for creating the Slime Image
=========================================================

Slime image details:
768 x 768
"""
import io
import random
import json
from PIL import Image, ImageDraw, ImageFont

def draw_slime(uid, version, name, color, template, accessories, no_images):
    """
    Creates a slime image based on its attributes
    """

    def get_color():
        """Chooses a color code from random"""
        r, g, b = random.choices(range(256), k=3)
        hexadecimal = f"#{r:02X}{g:02X}{b:02X}"
        return hexadecimal

    big_font = ImageFont.truetype("etc/LiberationMono-Regular.ttf", 34)
    medium_font = ImageFont.truetype("etc/LiberationMono-Regular.ttf", 16)
    small_font = ImageFont.truetype("etc/LiberationMono-Regular.ttf", 14)
    # tiny_font = ImageFont.truetype("etc/LiberationMono-Regular.ttf", 11)
    # -------------Image-------------

    # Set Template
    template_image = Image.open(f"etc/templates/template{template}.png")

    # Put Color on the template
    slime_image = Image.new("RGBA", template_image.size, color)
    slime_image.paste(template_image, (0, 0), template_image)
    text_select = ImageDraw.Draw(slime_image)

    """
	Choose accessories:
	Hat slot: "sunhat","top hat","wizard hat","robin hood hat", "santa hat", "crown", "golden top hat", "helmet"
	Other slot: "sunglasses","long beard","mustache","golden sunglasses","mustache+"
	"""
    # Hats

    if accessories:
        accessory_position_x = 392
        accessory_position_y = 668
        accessory_text_list = []

        with open("src/accessories.json") as accessory_json_file:
            accessory_json = json.load(accessory_json_file)

        for accessory in accessories:
            # Paste accessory on image
            item = accessory_json["Accessories"][accessory]
            open_image = Image.open(item["Location"])

            if "Custom" in accessory:
                print("Custom")
                hat_color = get_color()
                custom_image = Image.new("RGBA", open_image.size, hat_color)
                slime_image.paste(custom_image, (0, 0), custom_image)

            else:
                slime_image.paste(open_image, open_image)

            # Get text
            rarity = accessory_json["Accessories"][accessory]["Rarity"]
            accessory_text_list.append(f"{accessory} ({rarity})")

        # Write Accessories
        text_select.text(
            (accessory_position_x, accessory_position_y),
            "Items",
            fill=(0, 0, 0),
            font=medium_font,
            anchor="mm"
            )

        for accessory_text in accessory_text_list:
            accessory_position_y = accessory_position_y + 16
            text_select.text(
                (accessory_position_x, accessory_position_y),
                accessory_text,
                fill=(0, 0, 0),
                font=small_font,
                anchor="mm"
                )

    # Write Attributes to Image
    text_select.text((392, 620), name, fill=(0, 0, 0), font=big_font, anchor="mm")
    text_select.text((392, 648), uid, fill=(0, 0, 0), font=medium_font, anchor="mm")
    text_select.text((146, 720), "Version: " + str(version), fill=(0, 0, 0), font=medium_font, anchor="mm")
    text_select.text((600, 720), "Color: " + color, fill=(0, 0, 0), font=medium_font, anchor="mm")

    # Save slime to JPG
    if not no_images:
        slime_image.convert("RGB").save("img/" + uid + ".jpg", "JPEG")

    # Save slime to in-memory Buffer
    buffer = io.BytesIO()
    slime_image = slime_image.convert("RGB")  # Cannot write mode RGBA as JPEG
    slime_image.save(buffer, format="JPEG")

    return buffer.getvalue()
