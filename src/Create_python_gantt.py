"""This file is used to create a Gantt chart using Python code. It is like a
PlantUML API. The reason to use Python instead of directly specifying a Gantt
in a .uml file, is because it is easier to update/modify the Gantt chart.

For example, if you want to add an activity somewhere, in the .uml you
have to manually update all the tag numbers to preserve the order. (And
do that again for the colour specifications etc.) That is tedious work.
In this Python API, you can simply say: start the activity new activity
after activity X, and make activity Y start at the end of the new
activity. Then it automatically updates all the tags, for all
properties, e.g. activity descriptions, colours, order etc.
"""
from src.Activity import Activity
from src.export_data.Milestone import Milestone


# pylint: disable=R0914
def create_python_gantt(
    wages: dict, milestone_font_size=None, start_date=None
):
    """Specifies the data for a Gantt chart."""
    # Create a list to store the parent activities
    parents = []
    date_milestones = [
        Milestone(
            description="Complete CI deployment",
            font_size=milestone_font_size,
            date=start_date,
        )
    ]
    # parent one
    protocol = Activity(
        description="Develop protocol",
        duration=120,
        new_tag=0,
        colour="Green",
        hourly_wage=0,
    )
    # children
    onchain = Activity(
        description="On-chain: Solidty+VRF",
        duration=60,
        new_tag=0,
        parent=protocol,
        hourly_wage=wages["blockchain_dev"],
    )
    git_tellor = Activity(
        description="Git integration: Tellor",
        duration=90,
        new_tag=1,
        parent=protocol,
        starts_at_child_nr_start=0,
        hourly_wage=wages["blockchain_dev"],
    )
    git_chainlink = Activity(
        description="Git integration: Chainlink",
        duration=90,
        new_tag=2,
        parent=protocol,
        starts_at_child_nr_start=0,
        hourly_wage=wages["blockchain_dev"],
        milestone=Milestone(
            description="Support all languages",
            font_size=milestone_font_size,
        ),
    )
    alt_chains = Activity(
        description="Alternative Chains",
        duration=90,
        new_tag=3,
        parent=protocol,
        starts_at_child_nr_start=0,
        hourly_wage=wages["blockchain_dev"],
    )

    # grandchildren
    ci = Activity(
        description="(Decentralised) Continuous integration",
        new_tag=0,
        duration=30,
        parent=git_chainlink,
    )
    # git_chainlink.add_children([ci])
    security = Activity(
        description="Security & Robustness",
        duration=60,
        new_tag=1,
        parent=git_chainlink,
    )
    # ci.add_children([security])

    # merge
    protocol.add_children(
        [onchain, git_tellor, git_chainlink, alt_chains, ci, security]
    )
    parents.append(protocol)

    # parent_two
    platform_eco = Activity(
        description="Platform & ecosystem",
        duration=120,
        new_tag=1,
        colour="DarkOrchid",
        starts_at_child_nr_start=0,
        hourly_wage=wages["front_end_dev"],
    )
    # children
    website = Activity(
        description="Website", duration=50, new_tag=0, parent=platform_eco
    )
    marketing_platf = Activity(
        description="Marketing platform",
        duration=30,
        new_tag=1,
        parent=platform_eco,
    )
    bounties = Activity(
        description="Subsidize bounties",
        duration=10,
        new_tag=2,
        parent=platform_eco,
    )
    platform_buffer = Activity(
        description="Platform Planning Buffer",
        duration=30,
        new_tag=3,
        parent=platform_eco,
        milestone=Milestone(
            description="First Customer Usage",
            font_size=milestone_font_size,
            # TODO: remove date, make it place on the right position.
            date="2023-03-17",
        ),
    )

    # Grandchildren
    api = Activity(description="API", duration=50, new_tag=0, parent=website)
    gui = Activity(
        description="GUI",
        duration=50,
        new_tag=1,
        parent=website,
        starts_at_child_nr_start=0,
    )
    forum = Activity(
        description="Forum",
        duration=10,
        new_tag=2,
        parent=website,
        starts_at_child_nr_start=0,
    )
    website.add_children([api, gui, forum])

    platform_eco.add_children(
        [website, marketing_platf, bounties, platform_buffer]
    )
    parents.append(platform_eco)

    # parent_three
    company = Activity(
        description="Launch company",
        duration=150,
        new_tag=2,
        colour="Yellow",
        starts_at_child_nr_start=0,
        hourly_wage=wages["human_resources"],
    )
    # children
    partners = Activity(
        description="Qualitative partner research",
        duration=20,
        new_tag=0,
        parent=company,
    )
    organisation = Activity(
        description="Establish organisation",
        duration=80,
        new_tag=1,
        parent=company,
    )
    marketing_company = Activity(
        description="Marketing", duration=30, new_tag=2, parent=company
    )
    company_buffer = Activity(
        description="Organisation Planning Buffer ",
        duration=20,
        new_tag=3,
        parent=company,
        milestone=Milestone(
            description="Operational Break Even",
            font_size=milestone_font_size,
            # TODO: remove date, make it place on the right position.
            date="2023-06-09",
        ),
    )

    # Grandchildren
    auditing = Activity(
        description="Auditing", duration=10, new_tag=0, parent=organisation
    )
    hiring = Activity(
        description="Hiring", duration=20, new_tag=1, parent=organisation
    )
    administration = Activity(
        description="Administration",
        duration=10,
        new_tag=2,
        parent=organisation,
    )
    legal = Activity(
        description="Legal", duration=20, new_tag=3, parent=organisation
    )
    financial = Activity(
        description="Financial", duration=20, new_tag=4, parent=organisation
    )
    organisation.add_children(
        [auditing, hiring, administration, legal, financial]
    )

    company.add_children(
        [partners, organisation, marketing_company, company_buffer]
    )
    parents.append(company)

    # Create Milestones

    return parents, date_milestones


def addTwo(x):
    """adds two to the incoming integer and returns the result of the
    computation."""
    return x + 2
