"""Creates the Gantt chart specified in create_python_gantt."""

from src.Create_python_gantt import create_python_gantt
from src.export_data.Milestone import (
    get_milestone_for_date,
    get_milestone_style,
    get_milestone_uml_line,
)


# pylint: disable=R0902
class Gantt:
    """Creates the Gantt chart specified in create_python_gantt."""

    def __init__(self, filepath: str, params: dict):
        self.start_line = "@startgantt"
        self.project_start_date = "2022/10-01"
        self.closed_days = ["saturday", "sunday"]
        self.gantt_font_size = 100
        self.gantt_font_size_line = (
            f"skinparam classFontSize {self.gantt_font_size}"
        )
        self.box_font_size = "30"

        # self.font_size="skinparam defaultFontSize  100"
        self.parents, self.date_milestones = create_python_gantt(
            params["wages"], self.box_font_size, self.project_start_date
        )
        self.end_line = "@endgantt"
        self.lines, self.parent_costs = self.get_plantuml_gantt_lines()
        self.write_gantt(filepath, self.lines)

        self.costs = None

    def get_plantuml_gantt_lines(self):
        """Gets the list of lines of the UML file to create a Gantt chart."""
        lines = []
        lines.append(self.start_line)
        lines.append(f"project starts the {self.project_start_date}")
        lines = self.add_closed_dates(lines)
        lines.append(self.gantt_font_size_line)
        # Add milestone style here
        lines.append(get_milestone_style("blue", 100, "red", "yellow"))

        # Include date milestones
        for date_milestone in self.date_milestones:
            lines.append(get_milestone_for_date(date_milestone))

        # Writes acitivity line, appends milestone line below activity.
        lines, parent_costs = self.loop_through_parents_printing(lines)
        lines.append(self.end_line)
        return lines, parent_costs

    def loop_through_parents_printing(self, lines):
        """Prints all relevant data of the parent activities.

        :param lines:
        """
        # print descriptions
        for i, _ in enumerate(self.parents):
            lines = self.print_parent_descriptions(lines, self.parents[i])

        # print order
        for i, _ in enumerate(self.parents):
            if i > 0:
                if not self.parents[i].starts_at_child_nr_start is None:
                    lines.append(
                        f"[{self.parents[i].get_tag()}] starts at ["
                        + f"{self.parents[i].starts_at_child_nr_start}]"
                        + "'s start"
                    )
                else:
                    print(
                        f"parent_descr={self.parents[i].description}, and "
                        + "starts at: "
                        f"{self.parents[i].starts_at_child_nr_start}"
                        + " and  tag="
                        + f"{self.parents[i].get_tag()}, writing end"
                    )
                    lines.append(
                        f"[{self.parents[i].get_tag()}] starts at ["
                        + f"{self.parents[i-1].get_tag()}]'s end"
                    )
            lines = self.print_parent_order(lines, self.parents[i])

        # print colour
        for i, _ in enumerate(self.parents):
            lines = self.print_parent_colour(lines, self.parents[i])

        # compute costs
        total_costs = 0
        parent_costs = {}
        for i, _ in enumerate(self.parents):
            parent, total_costs, lines = self.print_parent_costs(
                total_costs, lines, self.parents[i]
            )
            parent_costs[parent] = total_costs
        return lines, parent_costs

    def print_parent_descriptions(self, lines, parent):
        """Creates the lines with the descriptions of the parents.

        :param lines:
        :param parent:
        """
        lines.append("")
        lines = self.print_descriptions(parent, lines)
        return lines

    def print_parent_order(self, lines, parent):
        """Creates the lines that specify the order of the parent activities.

        :param lines:
        :param parent:
        """
        lines.append("")
        lines = self.print_order(parent, lines)
        return lines

    def print_parent_colour(self, lines, parent):
        """Creates the line that specifies the colour of the parent.

        :param lines:
        :param parent:
        """
        lines.append("")
        lines = self.print_colour(parent, lines)
        lines.append("")
        return lines

    def print_parent_costs(self, total_costs, lines, parent):
        """Computes the costs of a parent activity based on the costs of its
        children.

        :param total_costs:
        :param lines:
        :param parent:
        """
        lines.append("")
        total_costs, lines = self.print_costs(total_costs, parent, lines)
        if isinstance(total_costs, tuple):
            total_costs = total_costs[0]
        print(f"parent={parent.description},total_costs={total_costs}")

        lines.append("")
        return parent, total_costs, lines

    def print_descriptions(self, activity, lines):
        """Creates the UML lines that specify the activity description.

        :param activity:
        :param lines:
        """

        if activity.font_size is not None:
            font_size = activity.font_size
        else:
            font_size = self.box_font_size
        lines.append(
            f"[<size:{font_size}>{activity.description}] as ["
            + f"{activity.get_tag()}] lasts {activity.duration} days"
        )

        # If activity has milestone, include it here.
        if activity.milestone is not None:
            lines.append(
                get_milestone_uml_line(activity.milestone, activity.get_tag())
            )
        for child in activity.children:
            lines = self.print_descriptions(child, lines)
        return lines

    def print_order(self, activity, lines):
        """Creates the order in which the activities are performed. The orders
        are stored relatively to eachother. E.g. activity y starts at the end
        of activity x.

        :param activity:
        :param lines:
        """
        # Write order for all children in an activity
        for i, _ in enumerate(activity.children):
            if i == 0:
                lines.append(
                    f"[{activity.children[i].get_tag()}] starts at ["
                    + f"{activity.get_tag()}]'s start"
                )
            else:
                # check if it starts at the start or end of some activity
                if not activity.children[i].starts_at_child_nr_start is None:
                    lines.append(
                        f"[{activity.children[i].get_tag()}] starts at ["
                        + f"{activity.children[i].starts_at_child_nr_start}"
                        + "]'s start"
                    )
                else:
                    lines.append(
                        f"[{activity.children[i].get_tag()}] starts at ["
                        + f"{activity.children[i-1].get_tag()}]'s end"
                    )

        # start recursive loop to write order of each of the childeren
        for child in activity.children:
            lines = self.print_order(child, lines)
        return lines

    def print_colour(self, activity, lines):
        """Creates the colours of the activities.

        :param activity:
        :param lines:
        """
        lines.append(
            f"[{activity.get_tag()}]  is colored in {activity.colour}"
        )
        for child in activity.children:
            lines = self.print_colour(child, lines)
        return lines

    def print_costs(self, total_costs, activity, lines):
        """Creates the lines that specify the costs of the activities.

        # TODO: output to LaTex variables.

        :param total_costs:
        :param activity:
        :param lines:
        """
        activity_costs = (
            activity.duration * activity.hours_per_day * activity.hourly_wage
        )
        lines.append(
            f"'[{activity.description}]  takes: {activity.duration}[days] "
            + f"equating to:{activity.duration*activity.hours_per_day}[hours]"
            + f" and costs:{activity.hourly_wage} per hour, yielding activity"
            + " costs:"
            + f"{activity_costs}"
            + " Euros."
        )
        total_costs = (
            total_costs
            + activity.duration * activity.hours_per_day * activity.hourly_wage
        )
        for child in activity.children:
            total_costs, lines = self.print_costs(total_costs, child, lines)
        return total_costs, lines

    def add_closed_dates(self, lines):
        """Adds the recurring days on which no work is performed in the Gantt.

        :param lines:
        """
        for closed_day in self.closed_days:
            lines.append(f"{closed_day} are closed")
        return lines

    def write_gantt(self, filepath, some_list):
        """Writes the lines of a gant to an output file.

        :param filepath:
        :param some_list:
        """
        with open(filepath, "w", encoding="utf-8") as f:
            for item in some_list:
                # pylint: disable=C0209
                f.write("%s\n" % item)
        f.close()

    def addTwo(self, x):
        """adds two to the incoming integer and returns the result of the
        computation.

        :param x:
        """
        return x + 2
