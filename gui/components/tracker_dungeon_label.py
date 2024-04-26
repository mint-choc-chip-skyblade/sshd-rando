from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QFontDatabase, QCursor, QMouseEvent
from PySide6 import QtCore
from PySide6.QtCore import Signal

from filepathconstants import TRACKER_ASSETS_PATH

from logic.world import World


class TrackerDungeonLabel(QLabel):

    hylia_font_id: int = -1
    default_style = f"color: COLOR; font-size: 24pt; font-family: Hylia Serif Beta; text-align: center; qproperty-alignment: {int(QtCore.Qt.AlignCenter) | int(QtCore.Qt.AlignBottom)};"

    clicked = Signal(str)

    def __init__(self, abbreviation_: str, dungeon_name_: str) -> None:

        if TrackerDungeonLabel.hylia_font_id == -1:
            TrackerDungeonLabel.hylia_font_id = QFontDatabase.addApplicationFont(
                (TRACKER_ASSETS_PATH / "HyliaSerifBeta-Regular.otf").as_posix()
            )
            if TrackerDungeonLabel.hylia_font_id == -1:
                print("Could not load Hylia Serif Font")

        super().__init__()
        self.abbreviation = abbreviation_
        self.dungeon_name = dungeon_name_
        self.world: World = None
        self.setText(abbreviation_)
        self.setStyleSheet(TrackerDungeonLabel.default_style)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.active: bool = False
        self.setStyleSheet(TrackerDungeonLabel.default_style.replace("COLOR", "gray"))
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        if ev.button() in [QtCore.Qt.LeftButton, QtCore.Qt.RightButton]:
            self.on_clicked()
        return super().mouseReleaseEvent(ev)

    def on_clicked(self) -> None:
        self.active = not self.active
        self.update_style()
        self.clicked.emit(self.dungeon_name)

    def update_style(self) -> None:
        if self.active:
            self.setStyleSheet(
                TrackerDungeonLabel.default_style.replace("COLOR", "dodgerblue")
            )
            # Add a strikethrough if the dungeon has been completed
            if self.world:
                dungeon = self.world.get_dungeon(self.dungeon_name)
                if dungeon.goal_location.marked:
                    self.setStyleSheet(
                        f"{self.styleSheet()} text-decoration: line-through;"
                    )
        else:
            self.setStyleSheet(
                TrackerDungeonLabel.default_style.replace("COLOR", "gray")
            )

    def reset(self) -> None:
        self.active = False
        self.setStyleSheet(TrackerDungeonLabel.default_style.replace("COLOR", "gray"))
