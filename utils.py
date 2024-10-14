import subprocess
import sys
import json
import ast

def install_package(packages):

    package_list = ast.literal_eval(packages)
    
    for package in package_list:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")