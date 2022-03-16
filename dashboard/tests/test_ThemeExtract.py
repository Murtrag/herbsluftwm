import pytest
from utils import ThemeExtract

def test_wallpaper():
    assert type(ThemeExtract.wallpaper) is str, "Wallpaper should be a string"

def test_colors():
    assert type(ThemeExtract.colors) is dict, "Proporties should be a type of dict"
