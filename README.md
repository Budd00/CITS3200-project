# Unigames Webapp

A web application for storing and managing a library of assets using a DAG-based tagging system

## Getting Started

Firstly, ensure you have the most recent version of Python (3.8.2) and have a virtual environment installed on the root folder of your local repository. Otherwise, the following command can be used to create a virtual environment called 'venv':
```
python -m venv venv
```

The virtual environment must then be activated. In Linux/OSX,
```
source venv/bin/activate
```

In Windows,
```
venv/Scripts/Activate.ps1
```
### Installing

While still in the virtual environment, use the package manager pip to install all the plugins contained in requirements.txt

```
pip install -r requirements.txt
```
Then to run the Django web app
```
python manage.py runserver
```

This will run the web application on localhost. This can be accessed through navigating to your favourite browser and entering 127.0.0.1:8000 or localhost:8000 on the address bar.

The application can then be freely browsed through as long as the Django app is running.
