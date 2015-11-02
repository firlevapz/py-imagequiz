# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#  Copyright (c) 2013, 2015, Corey Goldberg
#
#  Dev: https://github.com/cgoldberg/py-slideshow
#  License: GPLv3

import argparse
import random
import os

import pyglet
from pyglet.window import key

img_path = ''


def update_zoom(dz, zoom_speed, landscape):
    if (sprite.width > window.width or
            sprite.height > window.height):
        sprite.scale -= dz * zoom_speed
    else:
        pyglet.clock.unschedule(update_zoom)

    while (sprite.x + sprite.width < window.width and
               ((sprite.x < 0 and sprite.width > window.width) or
               (sprite.x < (window.width-sprite.width)/2 and sprite.width < window.width))
           ):
        sprite.x += 1
    while sprite.y + sprite.height < window.height and sprite.y < 0:
        sprite.y += 1


def update_image():
    global img_path
    global image_paths

    if len(image_paths) < 1:
        return
    img_path = random.choice(image_paths)
    image_paths.remove(img_path)

    img = pyglet.image.load(img_path)
    sprite.image = img
    sprite.scale = get_scale(window, img)
    if sprite.width < sprite.height:
        sprite.x = (window.width-sprite.width)/2
    else:
        sprite.x = 0
    sprite.y = 0

    # zoom_speed = random.uniform(sprite.scale/3, sprite.scale/2)
    zoom_speed = sprite.scale
    sprite.scale *= 5

    # set random start point of image
    sprite.x = random.uniform(window.width-sprite.width, 0)
    sprite.y = random.uniform(window.height-sprite.height, 0)

    pyglet.clock.schedule_interval(update_zoom, 1/60.0, zoom_speed, sprite.width > sprite.height)

    window.clear()


def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.lower().endswith(('jpg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale

window = pyglet.window.Window(fullscreen=False)

label = pyglet.text.Label('',
                          font_name='Arial',
                          font_size=42,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

check = pyglet.text.Label('',
                          font_name='Times New Roman',
                          font_size=20,
                          x=10, y=0,
                          anchor_x='left', anchor_y='bottom')

total_cnt = 0
check_cnt = 0
new_image = False


@window.event
def on_key_press(symbol, modifiers):
    global total_cnt
    global check_cnt
    global new_image

    if symbol == key.ENTER:
        label.text = os.path.splitext(os.path.basename(img_path))[0]
    elif symbol == key.SPACE and not new_image:
        label.text = ''
        update_image()
        new_image = True
    elif symbol == key.J and new_image:
        check_cnt += 1
        total_cnt += 1
        check.text = '{}/{}'.format(check_cnt, total_cnt)
        label.text = 'Jauhau!'
        new_image = False
    elif symbol == key.N and new_image:
        total_cnt += 1
        check.text = '{}/{}'.format(check_cnt, total_cnt)
        label.text = 'Na geeeh...'
        new_image = False
    else:
        return
    window.clear()
    sprite.draw()


@window.event
def on_draw():
    window.clear()
    if new_image:
        sprite.draw()
    label.draw()
    check.draw()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='directory of images',
                        nargs='?', default=os.getcwd())
    args = parser.parse_args()

    image_paths = get_image_paths(args.dir)
    img = pyglet.image.load(random.choice(image_paths))
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)

    label.text = 'Gät Räddäääy, STÄFFÄÄÄÄÄ...'

    pyglet.app.run()
