"""Rpresents a milestone object that can be added to the end of an activity."""


import re


# pylint: disable=R0903
class Milestone:
    """Used to create a milestone at the end or start of an activity in a Gantt
    chart."""

    # pylint: disable=R0913
    def __init__(
        self,
        description,
        font_size,
        at_end=True,
        date=None,
    ):
        self.font_size = font_size
        if font_size is None:
            raise Exception("Error, milestone fontsize not set.")
        self.description = description
        self.at_end = at_end
        self.date = date

        # Create an alphanumeric tag with underscores.
        self.tag = re.sub(r"[^A-Za-z0-9_]+", "_", self.description).lower()
        # Specify milestone stile.


def get_milestone_style(colour, fontsize, backgroundcolour, linecolour):
    """Returns the UML style specification of a milestone.

    :param colour:
    :param fontsize:
    :param backgroundcolour:
    :param linecolour:
    """
    left = """
    <style>
    ganttDiagram {
    milestone {
"""
    middle = f"""
        FontColor {colour}
        FontSize {fontsize}
        FontStyle italic
        BackGroundColor {backgroundcolour}
        LineColor {linecolour}
"""
    end = """
    }
}
</style>
    """
    return left + middle + end


def get_milestone_uml_line(milestone, activity_tag):
    """Returns the uml line for a milestone.

    :param milestone: param activity_tag:
    :param activity_tag:
    """
    if milestone.date is not None:
        milestone = get_milestone_for_date(milestone)
    else:
        milestone = get_milestone_for_activity(milestone, activity_tag)
    print(f"milestone={milestone}")
    return milestone


def get_milestone_for_activity(milestone, activity_tag):
    """returns a milestone for a certain activity.

    :param milestone: param activity_tag:
    :param activity_tag:
    """
    left = get_milestone_left(milestone)
    right = get_milestone_right(milestone, activity_tag)
    return left + right


def get_milestone_for_date(milestone):
    """Return milestone for a certain date.

    :param milestone:
    """
    left = get_milestone_left(milestone)
    if milestone.date is not None:
        # TODO: verify date format is valid yyyy-mm-dd
        right = f" {milestone.date}"
    milestone = left + right
    print(f"milestone={milestone}")
    return milestone


def get_milestone_left(milestone):
    """Returns the left part of a milestone description.

    :param milestone:
    """
    left = (
        f"[<size:{milestone.font_size}>{milestone.description} - "
        + f"{milestone.tag}] as [{milestone.tag}] happens "
    )
    return left


def get_milestone_right(milestone, activity_tag):
    """Returns the right part of a milestone description.

    :param milestone: param activity_tag:
    :param activity_tag:
    """
    if milestone.at_end:
        right = "at [" + activity_tag + "]'s end"
    elif not milestone.at_end:
        right = "at [" + activity_tag + "]'s start"
    return right
