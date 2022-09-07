"""Object that is used to store the activities that compose a Gantt chart."""
import copy


# pylint: disable=R0902
class Activity:
    """Used to create an activity in a Gantt chart."""

    # pylint: disable=R0913
    def __init__(
        self,
        description,
        duration,
        new_tag,
        colour=None,
        parent=None,
        starts_at_child_nr_start=None,
        starts_at_child_nr_end=None,
        font_size=None,
        hourly_wage=None,
        hours_per_day=None,
        min_parallel_workers=1,
        max_parallel_workers=1,
        milestone=None,
    ):
        self.parent = parent
        self.description = description
        self.duration = duration
        self.children = []
        self.font_size = font_size
        self.starts_at_child_nr_start = starts_at_child_nr_start
        self.starts_at_child_nr_end = starts_at_child_nr_end
        self.hourly_wage = hourly_wage
        self.min_parallel_workers = min_parallel_workers
        self.max_parallel_workers = max_parallel_workers
        self.milestone = milestone

        if hours_per_day is None:
            self.hours_per_day = 8
        else:
            self.hours_per_day = hours_per_day
        if self.parent is None:
            if colour is None:
                raise Exception("Parent activity needs a colour")
            self.colour = colour
            self.tag = []
        else:
            if (self.parent.hourly_wage is not None) and (hourly_wage is None):
                self.hourly_wage = self.parent.hourly_wage
            self.colour = parent.colour
            self.tag = copy.deepcopy(self.parent.tag)

        # create tag
        self.tag.append(new_tag)

    def add_children(self, children):
        """Stores the child activities in an activity.

        :param children:
        """
        self.children = children

    def get_tag(self):
        """Converts the tags of an activity into a string, with the activity
        indexes separated by underscores."""
        return "_".join([str(tag) for tag in self.tag])

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the
        computation.

        :param x:
        """
        return x + 2
