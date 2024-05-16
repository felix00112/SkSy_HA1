## How to get started
### Clone or fetch the repository
#### Clone
```
git clone https://github.com/felix00112/SkSy_HA1.git
cd SkSy_HA1
```
#### Fetch
```
git fetch --all
```
### Create virtual environment
`python -m venv venv`
### Activate virtual environment
- Linux/MacOs:
  `source venv/bin/activate`
- Windows:
  `venv\Scripts\activate`
### Install dependencies
- requirements.txt contains a list with all packages needed for the project
- to install all dependencies in your venv use:
  `pip install -r requirements.txt`
### Using VSCode
- Using VSCode instead of an IDE like PyCharm could cause some issues.
- Run code and get following error:
  ```
  from website import create_app
  ModuleNotFoundError: No module named 'website'
  ```
  Try this:
  **Add project folder as source for modules** *(in app.py)*
  ```
  import sys
  import os

  sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

  from website import create_app

  # Restlicher Code
  ```
- Sometimes python intepreter can't find module *flask*
  ```
  from flask import Flask
  ModuleNotFoundError: No module named 'flask'
  ```
  Try this:
  **Make sure you are running and have selected your virtual environment**
  1. Go to the directory where /website is located
  2. Activate the virtual environment
     ```
     source venv/bin/activate  # Linux/MacOS
      # or
     venv\Scripts\activate  # Windows
     ```
  3. Run app.py
