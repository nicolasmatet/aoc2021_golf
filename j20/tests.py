import unittest

from j20.solve import Image


class Tests(unittest.TestCase):

    def test_get_pixel_value34(self):
        image = Image({(1, 0): 1, (2, 1): 1})
        image.set_bounds(0, 2, 0, 2)
        pixel_value = image.get_pixel_patch_value(1, 1)
        self.assertEqual(34, pixel_value)

    def test_get_pixel_value512(self):
        image = Image(
            {(0, 0): 1, (0, 1): 1, (0, 2): 1, (1, 0): 1, (1, 1): 1, (1, 2): 1, (2, 0): 1, (2, 1): 1, (2, 2): 1})
        image.set_bounds(0, 2, 0, 2)
        pixel_value = image.get_pixel_patch_value(1, 1)
        self.assertEqual(511, pixel_value)

    def test_get_pixel_value0(self):
        image = Image({})
        image.set_bounds(0, 2, 0, 2)
        pixel_value = image.get_pixel_patch_value(1, 1)
        self.assertEqual(0, pixel_value)

    def test_get_pixel_value1_out_of_bounds(self):
        image = Image({(1, 1): 1, (1, 0): 1})
        image.set_bounds(0, 2, 0, 2)
        image.print_image()
        pixel_value = image.get_pixel_patch_value(0, 0)
        self.assertEqual(3, pixel_value)
