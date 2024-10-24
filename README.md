# create_notebook_project
A simple Python project setup template using Cookiecutter to automate directory structure creation and environment management. This template includes folders for data and source code, a Jupyter notebook, and integrates with uv for easy virtual environment setup and package management.

## Instructions

1. **Clone or download the repository**: Place the files in the root folder where you want to set up your new project.

2. **Install dependencies**: 
   - Make sure you have `cookiecutter` and `uv` installed.
   - If not, you can install them via pip:
     ```bash
     pip install cookiecutter uv
     ```

3. **Run the script**:
   Navigate to the directory where you placed the files and run the script:
   ```bash
   python create_notebook_project.py
   ```
4. **Customize the project name**: The script will prompt you for a project name. Provide your preferred name, and it will generate the project structure based on the template.

5. **Environment Setup**: Once the project structure is created, the script will initialize a uv virtual environment and set up Jupyter notebook integration automatically.

6. **Start working**: Your project is now ready! Navigate to the generated project directory and start adding your code and data.

Fore more Python for Engineering content, check out [flocode.substack.com](https://flocode.substack.com/)
