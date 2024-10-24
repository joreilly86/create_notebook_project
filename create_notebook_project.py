import argparse
import json
import logging
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Union

from cookiecutter.main import cookiecutter

# Configure logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Template Directory Structure for a basic Jupyter project
TEMPLATE_STRUCTURE: Dict[str, Union[str, dict]] = {
    "cookiecutter.json": json.dumps(
        {
            "project_name": "default_project_name",
            "author_name": "Your Name",
            "description": "A Jupyter notebook-based project.",
        },
        indent=4,
    ),
    "{{cookiecutter.project_name}}": {
        "data": {},  # Data directory
        "src": {},  # Source code directory
        "notebook_01.ipynb": json.dumps(
            {"cells": [], "metadata": {}, "nbformat": 4, "nbformat_minor": 5}, indent=4
        ),  # Blank Jupyter notebook file
        "README.md": (
            "# {{cookiecutter.project_name}}\n\n"
            "{{cookiecutter.description}}\n\n"
            "## Author\n"
            "{{cookiecutter.author_name}}"
        ),
    },
}


def create_template_structure(
    base_path: Path, structure: Dict[str, Union[str, dict]]
) -> None:
    """
    Recursively creates the project structure based on the template dictionary.
    """
    for name, content in structure.items():
        current_path = base_path / name
        if isinstance(content, dict):
            current_path.mkdir(parents=True, exist_ok=True)
            create_template_structure(current_path, content)
        else:
            current_path.parent.mkdir(parents=True, exist_ok=True)
            current_path.write_text(content, encoding="utf-8")


def run_command(command: list, cwd: Path = None) -> None:
    """
    Runs shell commands using subprocess, with error handling.
    """
    logging.info(f"Running command: {' '.join(command)}")
    try:
        subprocess.run(
            command, check=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Error running command {' '.join(command)}: {e.stderr.decode().strip()}"
        )
        sys.exit(1)


def initialize_project_environment(project_path: Path) -> None:
    """
    Initializes a Python project environment using `uv` and installs `ipykernel`.
    """
    if not shutil.which("uv"):
        logging.error("'uv' is not installed or not in the system PATH.")
        sys.exit(1)

    run_command(["uv", "init"], cwd=project_path)
    run_command(["uv", "add", "ipykernel"], cwd=project_path)


def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create a Jupyter project using Cookiecutter."
    )
    parser.add_argument(
        "-t",
        "--template-folder",
        default="jupyter-basic",
        help="Template folder name to use (default: 'jupyter-basic').",
    )
    parser.add_argument("-n", "--name", help="Name of the new project.")
    parser.add_argument(
        "-a",
        "--author",
        default="Your Name",
        help="Author name (default: 'Your Name').",
    )
    parser.add_argument(
        "-d",
        "--description",
        default="A Jupyter notebook-based project.",
        help="Project description.",
    )

    args = parser.parse_args()

    # Prompt for project name if not provided
    if not args.name:
        args.name = input("Enter the project name: ").strip()
        if not args.name:
            parser.error("the following arguments are required: -n/--name")

    return args


def prepare_template_directory(templates_base_dir: Path, template_folder: str) -> Path:
    """
    Ensures the template directory exists and is populated.
    """
    template_path = templates_base_dir / template_folder

    if not template_path.exists():
        logging.info(f"Creating new template at: {template_path}")
        create_template_structure(template_path, TEMPLATE_STRUCTURE)
    else:
        logging.info(f"Using existing template from: {template_path}")

    return template_path


def main():
    """
    Main function to handle the creation of the project template and initialize the project.
    """
    args = parse_arguments()

    # Define the base path where all templates are stored
    templates_base_dir = Path.cwd() / "cookiecutter-project-templates"
    templates_base_dir.mkdir(parents=True, exist_ok=True)

    # Prepare the template directory
    template_path = prepare_template_directory(templates_base_dir, args.template_folder)

    # Use Cookiecutter to create a new project with the provided context
    try:
        project_dir = Path(
            cookiecutter(
                str(template_path),
                no_input=True,
                extra_context={
                    "project_name": args.name,
                    "author_name": args.author,
                    "description": args.description,
                },
            )
        )
        logging.info(f"Project created at: {project_dir}")

        # Initialize the project environment
        initialize_project_environment(project_dir)
        logging.info("Project environment initialized successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
