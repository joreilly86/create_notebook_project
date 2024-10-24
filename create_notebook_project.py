import json
import os
import shutil
import subprocess
import sys

from cookiecutter.main import cookiecutter

# Template Directory Structure
template = {
    "cookiecutter.json": json.dumps({"project_name": "default_project_name"}),
    "{{cookiecutter.project_name}}": {
        "data": {},  # Data directory
        "src": {},  # Source code directory
        "notebook_01.ipynb": "",  # Jupyter notebook file
        "README.md": "# {{cookiecutter.project_name}}\n\nA Jupyter notebook-based project.",
    },
}


def create_template_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_template_structure(path, content)
        else:
            with open(path, "w") as file:
                file.write(content)


def run_command(command, cwd=None):
    try:
        subprocess.run(command, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(command)}: {e}")
        sys.exit(1)


def initialize_uv_project(project_path):
    if not shutil.which("uv"):
        print("Error: 'uv' is not installed or not in the system PATH.")
        sys.exit(1)

    run_command(["uv", "init"], cwd=project_path)
    # After initializing, add ipykernel which also creates the venv
    run_command(["uv", "add", "ipykernel"], cwd=project_path)


def main():
    base_dir = os.path.abspath("./cookiecutter-template")
    create_template_structure(base_dir, template)
    print(f"Template created at: {base_dir}")

    try:
        project_dir = cookiecutter(base_dir)
        initialize_uv_project(project_dir)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
