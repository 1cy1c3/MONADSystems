import cairo
import math
import json
import random
from io import BytesIO
from PIL import Image, ImageEnhance

# MONAD Colours from: https://monad-xyz.notion.site/skilly/Monad-Media-Kit-0554df533a10449d8dbbf960fd0c52a7
list_of_colors = [(181, 168, 250), (204, 196, 252), (95, 237, 223), (28, 94, 87), (32, 0, 82), (13, 0, 33), (74, 0, 43),
                  (96, 0, 78), (38, 0, 31), (158, 245, 237), (199, 105, 158), (204, 196, 252),
                  (128, 51, 112), (248, 237, 231), (191, 247, 242), (217, 156, 191)]

main_r, main_g, main_b = .514, .431, .976

# float generator
float_gen = lambda a, b: random.uniform(a, b)


def add_watermark(image, watermark_path, position, x, y):
    # Open the watermark
    watermark = Image.open(watermark_path)

    # Ensure the watermark has an alpha channel
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')
    # Resize the watermark
    watermark = watermark.resize((x, y))
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(0.6)
    watermark.putalpha(alpha)

    # Paste the watermark onto the image at the specified position
    image.paste(watermark, position, watermark)

    # Paste the watermark onto the image at the specified position
    image.paste(watermark, position, watermark)  # Assuming the watermark has transparency
    return image


def draw_ellipse(cr, x, y, width, height, r, g, b):
    cr.save()
    cr.translate(x + width, y + height)
    cr.scale(width, height)
    cr.arc(r, g, b, 0., 2 * math.pi)
    cr.restore()


def draw_orbit(cr, line, x, y, radius, r, g, b, a=1.0):
    cr.set_source_rgba(r, g, b, a)
    cr.set_line_width(line)
    cr.arc(x, y, radius, 0, 2 * math.pi)
    cr.stroke()


def draw_circle_fill(cr, x, y, radius, r, g, b):
    cr.set_source_rgb(r, g, b)
    cr.arc(x, y, radius, 0, 2 * math.pi)
    cr.fill()


def draw_border(cr, size, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, size, height)
    cr.rectangle(0, 0, width, size)
    cr.rectangle(0, height - size, width, size)
    cr.rectangle(width - size, 0, size, height)
    cr.fill()


def draw_background(cr, r, g, b, width, height):
    cr.set_source_rgb(r, g, b)
    cr.rectangle(0, 0, width, height)
    cr.fill()


def draw_shadow(cr, x, y, radius, angle):
    cr.set_source_rgba(0.0, 0.0, 0.0, .2)
    cr.arc(x, y, radius, angle, angle + math.pi)
    cr.fill()


def main(number: int):
    # Canvas
    width, height = 1000, 1000
    border_size = 10

    # Sun
    sun_size_min, sun_size_max = 25, 40
    sun_size = random.randint(sun_size_min, sun_size_max)
    sun_center = (height / 2)
    sun_color = random.choice(list_of_colors)
    sun_r, sun_g, sun_b = sun_color[0] / 255.0, sun_color[1] / 255.0, sun_color[2] / 255.0

    # Stars
    x_star_min, x_star_max = 12, 988
    y_star_min, y_star_max = 12, 988
    stars_count_min, stars_count_max = 300, 500
    star_pos = []

    # Planets
    planet_details = []
    distance_between_planets_min, distance_between_planets_max = 50, 251
    distance_between_planets_old = 0
    last_center = sun_center
    last_size = sun_size
    last_color = sun_color
    pos_orb_min, pos_orb_max = 0, 360
    speed_min, speed_max = -15, 15
    min_size, max_size = 5, 15

    # Moon
    distance_moon_min, distance_moon_max = 40, 50
    moon_chance_min, moon_chance_max = 1, 10
    moon_speed_min, moon_speed_max = -20, 20
    moon_size_min, moon_size_max = 2, 4

    # Rings
    ring_chance_min, ring_chance_max = 1, 10
    ring_amount_min, ring_amount_max = 1, 3
    ring_width_min, ring_width_max = 2, 4
    ring_radius_min, ring_radius_max = 15, 20

    # Initiate image
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    # Draw background and sun
    draw_background(cr, main_r, main_g, main_b, width, height)
    draw_border(cr, border_size, sun_r, sun_g, sun_b, width, height)
    stars_count = random.randint(stars_count_min, stars_count_max)

    print("Calculating Stars")
    for _ in range(1, stars_count):
        x_star = random.randint(x_star_min, x_star_max)
        y_star = random.randint(y_star_min, y_star_max)
        star_pos.append([x_star, y_star])

    print("Draw Background")
    draw_background(cr, main_r, main_g, main_b, width, height)
    draw_border(cr, border_size, sun_r, sun_g, sun_b, width, height)
    for pos in star_pos:
        draw_circle_fill(cr, pos[0], pos[1], 1, .973, .929, .906)

    draw_circle_fill(cr, width / 2, sun_center, sun_size, sun_r, sun_g, sun_b)

    print("Calculating Planets")
    for x in range(1, 10):
        speed = 0
        next_size = random.randint(min_size, max_size)
        distance_between_planets = random.randint(distance_between_planets_min, distance_between_planets_max)
        next_center = last_center - last_size / 2 - next_size / 2 - distance_between_planets
        rand_color = random.choice(list_of_colors)
        pos_orb = random.randint(pos_orb_min, pos_orb_max)
        ring_chance = random.randint(ring_chance_min, ring_chance_max)

        # Avoid speed 0
        while speed == 0:
            speed = random.randint(speed_min, speed_max)
        # Avoid double colours
        while rand_color is last_color:
            rand_color = random.choice(list_of_colors)

        last_color = rand_color
        # Color to float
        r, g, b = rand_color[0] / 255.0, rand_color[1] / 255.0, rand_color[2] / 255.0

        moon_chance = random.randint(moon_chance_min, moon_chance_max)
        # Check for room of orbit and planet
        if (not (next_center - (next_size * 1.5) / 2 < border_size) or not
        (next_center - (next_size * 1.5) / 2 < last_center - (last_size * 1.5) / 2 - distance_between_planets)):
            # Check for room of moon
            distance_moon = random.randint(distance_moon_min, distance_moon_max)
            if (next_center - border_size * 2 > distance_moon and moon_chance > 3
                    and distance_between_planets >= (distance_moon_max + distance_moon)
                    and distance_between_planets_old >= (distance_moon_max + distance_moon)):
                moon_size = random.randint(moon_size_min, moon_size_max)
                moon_speed = random.randint(moon_speed_min, moon_speed_max)
                # Avoid speed 0
                while moon_speed == 0:
                    moon_speed = random.randint(moon_speed_min, moon_speed_max)

                moon_details = [{
                    'size': moon_size,
                    'center': next_center - distance_moon,
                    'speed': moon_speed,
                    'orbit': distance_moon
                }]

                planet_detail = {
                    'pos_orb': pos_orb,
                    'speed': speed,
                    'size': next_size,
                    'center': next_center,
                    'r': r,
                    'g': g,
                    'b': b,
                    'moon': moon_details
                }

                planet_details.append(planet_detail)

            # Rings
            elif ring_chance > 7:
                ring_details = []
                ring_amount = random.randint(ring_amount_min, ring_amount_max)
                trigger = False

                for ring in range(ring_amount):
                    ring_radius = random.randint(ring_radius_min, ring_radius_max)
                    ring_width = random.randint(ring_width_min, ring_width_max)
                    if next_size > 11:
                        ring_radius += 5

                    if next_center - border_size * 2 > ring_radius + ring_width:
                        print("ring")
                        ring_detail = {
                            "width": ring_width,
                            "radius": ring_radius,
                        }

                        trigger = True
                        ring_radius_max += 5
                        ring_radius_min += 5
                        ring_details.append(ring_detail)

                if trigger:
                    planet_detail = {
                        'pos_orb': pos_orb,
                        'speed': speed,
                        'size': next_size,
                        'center': next_center,
                        'r': r,
                        'g': g,
                        'b': b,
                        'rings': ring_details
                    }

                else:
                    planet_detail = {
                        'pos_orb': pos_orb,
                        'speed': speed,
                        'size': next_size,
                        'center': next_center,
                        'r': r,
                        'g': g,
                        'b': b
                    }

                planet_details.append(planet_detail)
            # No moon
            else:
                planet_detail = {
                    'pos_orb': pos_orb,
                    'speed': speed,
                    'size': next_size,
                    'center': next_center,
                    'r': r,
                    'g': g,
                    'b': b
                }

                planet_details.append(planet_detail)

            last_size = next_size
            last_center = next_center
            speed_max -= 3
            speed_min -= 2
            distance_between_planets_old = distance_between_planets
            distance_between_planets_min += 5

    collected_frames = []
    # For 360 degrees revolution draw planets and moon
    print("Calculating Rotation")
    for d in range(0, 360):
        for i, planet in enumerate(planet_details):
            if i == 0:
                draw_orbit(cr, 1, width / 2, sun_center, (height / 2) - planet['center']
                           - border_size, sun_r, sun_g, sun_b)
            else:
                draw_orbit(cr, 1, width / 2, sun_center, (height / 2) - planet['center']
                           - border_size, planet_details[i - 1]['r'], planet_details[i - 1]['g'],
                           planet_details[i - 1]['b'])

            # Using formula x = xm + r * sin(phi) and y = ym + r * cos(phi); adding d to increase the radius by 1
            # degree each frame
            x = int((width / 2) + ((height / 2) - planet['center'] - border_size)
                    * math.sin((planet['pos_orb'] + d * planet['speed'] / 10) * (math.pi / 180)))
            y = int((height / 2) + ((height / 2) - planet['center'] - border_size)
                    * math.cos((planet['pos_orb'] + d * planet['speed'] / 10) * (math.pi / 180)))

            # draw bigger outer circle to make the orbit lin not connect with planet, optical hack
            draw_circle_fill(cr, x, y, planet['size'] * 1.5, main_r, main_g, main_b)
            draw_circle_fill(cr, x, y, planet['size'], planet['r'], planet['g'], planet['b'])

            if x - width / 2 < 0:
                draw_shadow(cr, x, y, planet['size'], math.atan((y - height / 2) / (x - width / 2)) + .5 * math.pi)
            elif x - width / 2 > 0:
                draw_shadow(cr, x, y, planet['size'], math.atan((y - height / 2) / (x - width / 2)) - .5 * math.pi)
            else:
                if y - height / 2 > 0:
                    draw_shadow(cr, x, y, planet['size'],
                                .5 * math.pi - .5 * math.pi)
                elif y - height / 2 < 0:
                    draw_shadow(cr, x, y, planet['size'],
                                .5 * math.pi + .5 * math.pi)
            if 'moon' in planet:
                moon = planet['moon']
                # same logic for moon, but use transformed values
                x_moon = int(x + (moon[0]['orbit']) * math.sin((planet['pos_orb'] +
                                                                    d * 2 * moon[0]['speed'] / 10) * (
                                                                           math.pi / 180)))
                y_moon = int(y + (moon[0]['orbit']) * math.cos((planet['pos_orb'] +
                                                                    d * 2 * moon[0]['speed'] / 10) * (
                                                                           math.pi / 180)))

                draw_circle_fill(cr, x_moon, y_moon, moon[0]['size'], planet['r'], planet['g'], planet['b'])

                if x_moon - width / 2 < 0:
                    draw_shadow(cr, x_moon, y_moon, moon[0]['size'],
                                math.atan((y_moon - height / 2) / (x_moon - width / 2)) + .5 * math.pi)
                elif x_moon - width / 2 > 0:
                    draw_shadow(cr, x_moon, y_moon, moon[0]['size'],
                                math.atan((y_moon - height / 2) / (x_moon - width / 2)) - .5 * math.pi)
                else:
                    if y_moon - height / 2 > 0:
                        draw_shadow(cr, x_moon, y_moon, moon[0]['size'],
                                    .5 * math.pi - .5 * math.pi)
                    elif y_moon - height / 2 < 0:
                        draw_shadow(cr, x_moon, y_moon, moon[0]['size'],
                                    .5 * math.pi + .5 * math.pi)
            elif 'rings' in planet:
                for item in planet['rings']:
                    x_ring = int((width / 2) + ((height / 2) - planet['center'] - border_size)
                                 * math.sin((planet['pos_orb'] + d * planet['speed'] / 10) * (math.pi / 180)))
                    y_ring = int((height / 2) + ((height / 2) - planet['center'] - border_size)
                                 * math.cos((planet['pos_orb'] + d * planet['speed'] / 10) * (math.pi / 180)))
                    draw_orbit(
                        cr, item['width'], x_ring, y_ring, item['radius'], planet['r'], planet['g'], planet['b'], a=.4)

        # save the frame
        buf = BytesIO()
        ims.write_to_png(buf)
        buf.seek(0)
        frame_image = Image.open(buf)
        collected_frames.append(frame_image)
        # Cleanup loop to delete previous objects
        # skip last frame to get perfect loop if value is a full number
        if d < 359:
            draw_background(cr, main_r, main_g, main_b, width, height)
            draw_border(cr, border_size, sun_r, sun_g, sun_b, width, height)
            for pos in star_pos:
                draw_circle_fill(cr, pos[0], pos[1], 1, .973, .929, .906)

            draw_circle_fill(cr, width / 2, sun_center, sun_size, sun_r, sun_g, sun_b)

        # Add watermark
    # watermark_path = 'assets/media/watermark.png'
    # watermark_position = (width - 256 - 20, 20)  # 10 pixels padding from right and top
    # x, y = 256, 50
    # print("Add Watermark")
    # for pil_image in collected_frames:
    #    # Save the image to a BytesIO object
    #    image_io = BytesIO()
    #
    #       pil_image.load()
    #      pil_image = add_watermark(pil_image, watermark_path, watermark_position, x, y)
    #     pil_image.save(image_io, format='PNG')

    collected_frames[0].save(f'nft/gifs/System_{number}.gif', format='GIF', save_all=True,
                             append_images=collected_frames,
                             optimize=False, duration=33, loop=0)

    with open(f'nft/metadata/metadata.txt', 'a') as file:
        json.dump(planet_details, file, indent=4)
        file.write("\n")


if __name__ == "__main__":
    i = 0
    n = input("Iteratinos: ")
    while i < int(n):
        i += 1
        print(f"{i} / {n}")
        main(i)
