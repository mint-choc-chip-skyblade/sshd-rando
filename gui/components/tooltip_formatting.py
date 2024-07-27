from logic.requirements import (
    TOD,
    Requirement,
    RequirementType,
    evaluate_requirement_at_time,
)
from logic.tooltips.tooltips import pretty_name, sort_requirement
from PySide6.QtGui import QFontMetrics, QTextDocumentFragment
from PySide6.QtWidgets import QToolTip


def get_tooltip_text(tracker_label, req: Requirement) -> str:
    sort_requirement(req)
    match req.type:
        case RequirementType.AND:
            # Computed requirements have a top-level AND requirement
            # We display them as a list of bullet points to the user
            # This fetches a list of the terms ANDed together
            text = [format_requirement(tracker_label, a) for a in req.args]
        case _:
            # The requirement is just one term, so format the requirement
            text = [format_requirement(tracker_label, req)]

    tooltip_font_metrics = QFontMetrics(QToolTip.font())
    # Find the width of the longest requirement description, adding a 16px buffer for the bullet point
    max_line_width = (
        max(
            [
                tooltip_font_metrics.horizontalAdvance(
                    QTextDocumentFragment.fromHtml(line).toPlainText()
                )
                for line in text + ["Item Requirements:"]
            ]
        )
        + 16
    )
    # Set the tooltip's min and max width to ensure the tooltip is the right size and line-breaks properly
    tracker_label.setStyleSheet(
        tracker_label.styleSheet()
        .replace("MINWIDTH", str(min(max_line_width, tracker_label.width() - 3)))
        .replace("MAXWIDTH", str(tracker_label.width() - 3))
    )
    return (
        "Item Requirements:"
        + '<ul style="margin-top: 0px; margin-bottom: 0px; margin-left: 8px; margin-right: 0px; -qt-list-indent:0;"><li>'
        + "</li><li>".join(text)
        + "</li></ul>"
    )


def format_requirement(
    tracker_label,
    req: Requirement,
    is_top_level=True,
) -> str:
    match req.type:
        case RequirementType.IMPOSSIBLE:
            return '<span style="color:red">Impossible (please discover an entrance first)</span>'
        case RequirementType.NOTHING:
            return '<span style="color:dodgerblue">Nothing</span>'
        case RequirementType.ITEM:
            # Determine if the user has marked this item
            color = (
                "dodgerblue"
                if evaluate_requirement_at_time(
                    req, tracker_label.recent_search, TOD.ALL, tracker_label.world
                )
                else "red"
            )
            # Get a pretty name for the item if it is the first stage of a progressive item
            name = pretty_name(req.args[0].name, 1)
            return f'<span style="color:{color}">{name}</span>'
        case RequirementType.COUNT:
            # Determine if the user has enough of this item marked
            color = (
                "dodgerblue"
                if evaluate_requirement_at_time(
                    req, tracker_label.recent_search, TOD.ALL, tracker_label.world
                )
                else "red"
            )
            # Get a pretty name for the progressive item
            name = pretty_name(req.args[1].name, req.args[0])
            return f'<span style="color:{color}">{name}</span>'
        case RequirementType.WALLET_CAPACITY:
            # Determine if the user has enough wallet capacity for this requirement
            color = (
                "dodgerblue"
                if evaluate_requirement_at_time(
                    req, tracker_label.recent_search, TOD.ALL, tracker_label.world
                )
                else "red"
            )
            # TODO: Properly expand into wallet combinations
            return f'<span style="color:{color}">Wallet >= {req.args[0]}</span>'
        case RequirementType.GRATITUDE_CRYSTALS:
            # Determine if the user has enough gratitude crystals marked
            color = (
                "dodgerblue"
                if evaluate_requirement_at_time(
                    req, tracker_label.recent_search, TOD.ALL, tracker_label.world
                )
                else "red"
            )
            return (
                f'<span style="color:{color}">{req.args[0]} Gratitude Crystals</span>'
            )
        case RequirementType.TRACKER_NOTE:
            color = (
                "dodgerblue"
                if evaluate_requirement_at_time(
                    req.args[1],
                    tracker_label.recent_search,
                    TOD.ALL,
                    tracker_label.world,
                )
                else "red"
            )
            return f'<span style="color:{color}">{req.args[2]}</span>'
        case RequirementType.OR:
            # Recursively join requirements with "or"
            # Only include parentheses if not at the top level (where they'd be redundant)
            return (
                ("" if is_top_level else "(")
                + " or ".join(
                    [format_requirement(tracker_label, a, False) for a in req.args]
                )
                + ("" if is_top_level else ")")
            )
        case RequirementType.AND:
            # Recursively join requirements with "and"
            # Only include parentheses if not at the top level (where they'd be redundant)
            return (
                ("" if is_top_level else "(")
                + " and ".join(
                    [format_requirement(tracker_label, a, False) for a in req.args]
                )
                + ("" if is_top_level else ")")
            )
        case _:
            raise ValueError("unreachable")
