"""
Simple script for creating animated sprites in pygame
"""

__author__ = 'Joshua Akangah'

import pygame
from os import path
# from main import screen

working_dir = path.dirname(__file__)

class Animation():
    """
    Class animation
    """
    def __init__(self, sprites, scale, frame_duration=0.1):
        """
        __init__ method of animation class
        :param sprites: A list of all images to be included in the animation
        eg. ['assets/player/Move1.png', 'assets/player/Move2.png', 'assets/player/Move3.png']
        :param frame_duration: The amount of time (in seconds) between each frame.  By default it is set to 0.1
        :param scale: Scale factor to use to scale sprites
        eg. A scale of 0.5 scales the image to half its size
        """
        self.images = []
        for i in sprites:
            image = pygame.image.load(i).convert_alpha()
            images = pygame.transform.scale(image, (int(image.get_rect().width * scale), int(image.get_rect().height * scale)))
            self.images.append(images)

        self.animation_time = frame_duration
        self.current_time = 0
        self.animation_frames = len(self.images)
        self.current_frame = 0
        self.index = 0

    def animate(self, dt):
        """
        Method to update sprites to make an animation
        :param dt: deltatime to update animaton from
        :return: None
        """
        self.current_time += dt

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

    def get_current_image(self):
        """
        Method to return the current image in the animation
        :return: pygame.image
        """
        return self.images[self.index]

    def get_rect(self):
        """
        Method to return the rect of the current image in the animation
        :return: pygame.Rect
        """
        return self.get_current_image().get_rect()

    def is_last_image(self):
        """
        Method to check is if current image is the last in the list
        :return: bool
        """

        if self.images.index(self.get_current_image()) == len(self.images) - 1:
            self.index
            return True
        return False
