"""This file creates the diagrams that are written directly in plain .uml
files."""
from src.export_data.plantuml_compile import (
    compile_diagrams_in_dir_relative_to_root,
)
from src.export_data.plantuml_to_tex import export_diagrams_to_latex


def create_static_diagrams(args, hd):
    """Generates .png images of the static diagram .uml files.

    :param args:
    :param hd:
    """
    # PlantUML
    if args.sd:
        # Compile statically generated PlantUML diagrams to images.
        compile_diagrams_in_dir_relative_to_root(
            hd.await_compilation,
            hd.gantt_extension,
            hd.jar_path_relative_from_root,
            hd.path_to_static_gantts,
            hd.verbose,
        )

        # Export static PlantUML text files to LaTex.
        export_diagrams_to_latex(
            hd.path_to_static_gantts,
            hd.gantt_extension,
            hd.diagram_output_dir_relative_to_root,
        )

        # Export static PlantUML diagram images to LaTex.
        export_diagrams_to_latex(
            hd.path_to_static_gantts,
            hd.diagram_extension,
            hd.diagram_output_dir_relative_to_root,
        )
