from PySide6.QtCore import Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QPushButton, QColorDialog

from enum import Enum, auto


class ColorFormat(Enum):
    RGB = auto()
    RGBA = auto()
    ARGB = auto()


class ColorButton(QPushButton):
    colorChanged = Signal(str, str)

    def __init__(self, color: str, name: str, showAlpha: bool = True):
        super().__init__()
        self.color = self.color_int_from_str(color)
        self.name = name
        self.showAlpha = showAlpha

        self.setMinimumHeight(32)
        self.update()

        self.clicked.connect(self.change_color)

    def change_color(self):
        # Should the setOption function handle this? Yes. Does it? No.
        color_dialog_options = QColorDialog.ColorDialogOption(0)
        if self.showAlpha:
            color_dialog_options = QColorDialog.ColorDialogOption.ShowAlphaChannel

        new_color = QColorDialog.getColor(
            self.color_str_from_int(self.color, ColorFormat.ARGB),
            options=color_dialog_options,
        )

        if new_color.isValid():
            self.color = self.color_int_from_str(self.color_str_from_qcolor(new_color))
            self.update()
            self.colorChanged.emit(self.color_str_from_int(self.color), self.name)

    def update(self):
        r, g, b, a = self.color_parts_from_int(self.color)
        # https://en.wikipedia.org/wiki/Relative_luminance
        luminance = (0.2126 * r) + (0.7152 * g) + (0.0722 * b)
        textColor = "white"
        if luminance > 128:
            textColor = "black"

        rgba = self.color_str_from_int(self.color)
        self.setText(rgba)
        self.setStyleSheet(
            "QPushButton {background-color: "
            + rgba[:-2]
            + "; color: "
            + textColor
            + "; }"
        )

    def color_str_from_qcolor(
        self, color: QColor, format: ColorFormat = ColorFormat.RGBA
    ) -> str:
        match format:
            case ColorFormat.RGB:
                return color.name(QColor.HexRgb)
            case ColorFormat.RGBA:
                argb = color.name(QColor.HexArgb)
                return argb[0] + argb[3:] + argb[1:3]
            case ColorFormat.ARGB:
                return color.name(QColor.HexArgb)

    def color_str_from_int(
        self, color_int: int, format: ColorFormat = ColorFormat.RGBA
    ) -> str:
        color = QColor(*self.color_parts_from_int(color_int))

        return self.color_str_from_qcolor(color, format)

    def color_int_from_str(self, color: str) -> int:
        return int(color[1:], 16)

    def color_parts_from_int(self, color_int: int) -> tuple:
        r = color_int >> 24
        g = color_int >> 16 & 0xFF
        b = color_int >> 8 & 0xFF
        a = color_int & 0xFF
        return (r, g, b, a)
