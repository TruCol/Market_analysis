"""Generates .uml PlantUML files based on Python code.

Typically used for Gantt charts.
"""
from src.export_data.plantuml_compile import (
    compile_diagrams_in_dir_relative_to_root,
)
from src.export_data.plantuml_generate import generate_all_dynamic_diagrams
from src.export_data.plantuml_to_tex import export_diagrams_to_latex


def create_dynamic_diagrams(args, hd):
    """Generates the dynamic diagrams."""
    # Generate PlantUML diagrams dynamically (using code).
    if args.dd:
        generate_all_dynamic_diagrams(
            f"{hd.path_to_export_data_from_root}/Diagrams/Dynamic_diagrams"
        )

        # Compile dynamically generated PlantUML diagrams to images.
        compile_diagrams_in_dir_relative_to_root(
            hd.await_compilation,
            hd.gantt_extension,
            hd.jar_path_relative_from_root,
            hd.path_to_dynamic_gantts,
            hd.verbose,
        )

        # Export dynamic PlantUML text files to LaTex.
        export_diagrams_to_latex(
            hd.path_to_dynamic_gantts,
            hd.gantt_extension,
            hd.diagram_output_dir_relative_to_root,
        )

        # Export dynamic PlantUML diagram images to LaTex.
        export_diagrams_to_latex(
            hd.path_to_dynamic_gantts,
            hd.diagram_extension,
            hd.diagram_output_dir_relative_to_root,
        )
