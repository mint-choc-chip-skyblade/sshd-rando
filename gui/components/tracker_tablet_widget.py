from PySide6.QtGui import QPaintEvent
from PySide6.QtWidgets import QWidget, QSizePolicy

from gui.components.tracker_inventory_button import TrackerInventoryButton

from constants.itemconstants import EMERALD_TABLET, RUBY_TABLET, AMBER_TABLET


class TrackerTabletWidget(QWidget):

    TABLET_ASPECT_RATIO = 1.29

    def __init__(self):
        super().__init__()
        # Delcare amber tablet first so it placed below the ruby and emerald tablets.
        # Due to how the pictures are arranged, it makes more sense for the ruby and
        # emerald tablets to be above the amber tablet.
        self.amber_tablet_button = TrackerInventoryButton(
            ["Nothing", AMBER_TABLET],
            ["tablets/amber_tablet_gray.png", "tablets/amber_tablet.png"],
            self,
        )
        self.emerald_tablet_button = TrackerInventoryButton(
            ["Nothing", EMERALD_TABLET],
            ["tablets/emerald_tablet_gray.png", "tablets/emerald_tablet.png"],
            self,
        )
        self.ruby_tablet_button = TrackerInventoryButton(
            ["Nothing", RUBY_TABLET],
            ["tablets/ruby_tablet_gray.png", "tablets/ruby_tablet.png"],
            self,
        )
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.amber_tablet_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.emerald_tablet_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.ruby_tablet_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def update_buttons(self) -> None:
        amber = self.amber_tablet_button
        ruby = self.ruby_tablet_button
        emerald = self.emerald_tablet_button

        total_tablet_width = 0
        total_tablet_height = 0
        tablet_x = 0
        tablet_y = 0
        # Change the size and position of the buttons to be where they should
        # be within the widget
        current_aspect_ratio = self.width() / self.height()

        # If the widget is taller than the tablets, scale based on width
        if current_aspect_ratio < TrackerTabletWidget.TABLET_ASPECT_RATIO:
            total_tablet_width = self.width() - 5
            total_tablet_height = int(
                total_tablet_width / TrackerTabletWidget.TABLET_ASPECT_RATIO
            )
            tablet_x = 5
            tablet_y = int((self.height() - total_tablet_height) / 2)
        # Otherwise, scale based on height
        else:
            total_tablet_height = self.height()
            total_tablet_width = int(
                total_tablet_height * TrackerTabletWidget.TABLET_ASPECT_RATIO
            )
            tablet_x = int((self.width() - total_tablet_width) / 2)
            tablet_y = 0

        amber_aspect_ratio = amber.pixmap.width() / amber.pixmap.height()
        amber_height = total_tablet_height
        amber_width = amber_height * amber_aspect_ratio
        amber.setFixedSize(amber_width, amber_height)

        # We can pull the size modifier from the amber tablet
        # since its height should always match the total tablet height
        size_modifier = amber_height / amber.pixmap.height()

        ruby_width = ruby.pixmap.width() * size_modifier
        ruby_height = ruby.pixmap.height() * size_modifier
        ruby.setFixedSize(ruby_width, ruby_height)

        emerald_width = emerald.pixmap.width() * size_modifier
        emerald_height = emerald.pixmap.height() * size_modifier
        emerald.setFixedSize(emerald_width, emerald_height)

        amber.move(tablet_x, tablet_y)
        ruby.move(tablet_x + total_tablet_width - ruby.width() - 1, tablet_y)
        emerald.move(
            tablet_x + total_tablet_width - emerald.width() - 1,
            tablet_y + total_tablet_height - emerald.height() - 1,
        )

    def paintEvent(self, event: QPaintEvent) -> None:

        self.update_buttons()

        return super().paintEvent(event)
