import os

# Step 1: Create a folder where your project will reside
project_folder = 'MyPythonProject'
if not os.path.exists(project_folder):
    os.makedirs(project_folder)

# Step 2: Create a Python file in that folder
python_filename = 'main.py'
with open(os.path.join(project_folder, python_filename), 'w') as file:
    file.write('print "Hello, VS Code!"')

# Step 3: Create a virtual environment
os.system(f'python -m venv {os.path.join(project_folder, "venv")}')

# Step 4: Write a requirements.txt (though empty here, typically would include needed packages)
requirements_file = 'requirements.txt'
with open(os.path.join(project_folder, requirements_file), 'w') as file:
    file.write('# Add your dependencies here, e.g.,numpy==1.18.5')

# Step 5: Add a .gitignore file
gitignore_content = '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
'''
with open(os.path.join(project_folder, '.gitignore'), 'w') as file:
    file.write(gitignore_content)