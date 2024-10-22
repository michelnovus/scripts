from math import sqrt, ceil
from io import BytesIO
from pathlib import Path
from importlib import resources

from PIL import Image, ImageDraw, ImageFont


class WatermarkGenerator(object):
    def __init__(
        self,
        text: str,
        font: str = "JetBrainsMono",
        size: int = 50,
        xpad: int = 100,
        ypad: int = 80,
        color: tuple[int, int, int] = (200, 200, 200),
        opacity: int = 127,
        rotation: int = 30,
    ) -> None:
        self.text = text.strip()
        self.font = ImageFont.truetype(
            BytesIO(
                resources.files("watermark.fonts")
                .joinpath(f"{font}.ttf")
                .read_bytes()
            ),
            size,
        )
        self.xpad = xpad
        self.ypad = ypad
        self.color = (*color, opacity)
        self.rotation = rotation

    def _text_size(self) -> tuple[int, int]:
        """Calcula y devuelve el ancho y el alto del texto según la fuente."""
        p0_x, p0_y, p1_x, p1_y = self.font.getbbox(self.text)
        return (int(p1_x - p0_x), int(p1_y - p0_y))

    @staticmethod
    def _center_point(size: tuple[int, int]) -> tuple[int, int]:
        """Calcula el punto central del cuadrilátero definido en P(0,0) y P_size(x,y)."""
        return (size[0] // 2, size[1] // 2)

    def generate_everywhere(self, image: Path | BytesIO) -> Image.Image:
        with Image.open(image).convert("RGBA") as img:
            square_width = ceil(sqrt(img.width**2 + img.height**2))
            square_img = Image.new(
                "RGBA", (square_width, square_width), (255, 255, 255, 0)
            )
            draw = ImageDraw.Draw(square_img)
            text_width, text_height = self._text_size()
            _row_width = 0
            _col_height = 0
            _indent = False
            while _col_height < square_width:
                while _row_width < square_width:
                    draw.text(
                        (_row_width, _col_height),
                        self.text,
                        self.color,
                        self.font,
                    )
                    _row_width += self.xpad + text_width
                _indent = not _indent
                if _indent:
                    _row_width = (text_width + self.xpad) // 2
                else:
                    _row_width = 0
                _col_height += self.ypad + text_height
            square_img = square_img.rotate(self.rotation)
            watermark_img_center_point = self._center_point(square_img.size)
            square_img = square_img.crop(
                (
                    watermark_img_center_point[0] - img.width // 2,
                    watermark_img_center_point[1] - img.height // 2,
                    watermark_img_center_point[0] + img.width // 2,
                    watermark_img_center_point[1] + img.height // 2,
                )
            )
            img.alpha_composite(square_img)
            return img
