from enum import Enum

WATERMARK_SUFFIX = "-watermark"

# ** The position of watermark into image.
Position = Enum("Position", "ALL CENTER N S E W NE SE SW NW")


# TODO: Implementar objeto Color
class Color(object):
    def __init__(self, value: str) -> None:
        self.hex = value

    def __str__(self) -> str:
        return self.hex
