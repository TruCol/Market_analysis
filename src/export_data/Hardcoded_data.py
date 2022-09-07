"""Specify hardcoded output data."""


# pylint: disable=R0902
# pylint: disable=R0903
class Hardcoded_data:
    """Contains a list of parameters that are used in this project that
    combines Python code with a LaTex document."""

    def __init__(self):

        # Specify code configuration details
        # TODO: include as optional arguments.
        self.await_compilation = True
        self.verbose = True
        self.gantt_extension = ".uml"
        self.diagram_extension = ".png"

        # Filenames.
        self.main_latex_filename = "main.tex"
        self.export_data_dirname = "export_data"
        self.diagram_dir = "Diagrams"
        self.plant_uml_java_filename = "plantuml.jar"

        # Appendix manager filenames
        self.export_code_appendices_filename = "export_code_appendices.tex"
        self.export_code_appendices_filename_from_root = (
            "export_code_appendices_from_root.tex"
        )
        self.project_code_appendices_filename = "project_code_appendices.tex"
        self.project_code_appendices_filename_from_root = (
            "project_code_appendices_from_root.tex"
        )
        self.automatic_appendices_manager_filenames = [
            self.export_code_appendices_filename,
            self.export_code_appendices_filename_from_root,
            self.project_code_appendices_filename,
            self.project_code_appendices_filename_from_root,
        ]

        self.manual_appendices_filename = "manual_appendices.tex"
        self.manual_appendices_filename_from_root = (
            "manual_appendices_from_root.tex"
        )
        self.manual_appendices_manager_filenames = [
            self.manual_appendices_filename,
            self.manual_appendices_filename_from_root,
        ]
        self.appendix_dir_from_root = "latex/Appendices/"

        # Folder names.
        self.dynamic_diagram_dir = "Dynamic_diagrams"
        self.static_diagram_dir = "Static_diagrams"

        # Specify paths relative to root.
        self.path_to_export_data_from_root = f"src/{self.export_data_dirname}"
        self.jar_path_relative_from_root = (
            f"{self.path_to_export_data_from_root}"
            + f"/{self.plant_uml_java_filename}"
        )
        self.diagram_output_dir_relative_to_root = (
            f"latex/Images/{self.diagram_dir}"
        )

        # Path related variables
        self.append_export_code_to_latex = True
        self.path_to_dynamic_gantts = (
            f"{self.path_to_export_data_from_root}/"
            + f"{self.diagram_dir}/{self.dynamic_diagram_dir}"
        )
        self.path_to_static_gantts = (
            f"{self.path_to_export_data_from_root}/"
            + f"{self.diagram_dir}/{self.static_diagram_dir}"
        )
