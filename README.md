
# Project-X

File storing and sharing cloud based solution
## Authors

- [@sidd6p](https://github.com/sidd6p)


## Directory stracture
app

    │   auth2.py
    │   database.py
    │   main.py
    │   models.py
    │   schemas.py
    │   utils.py
    │   __init__.py
    │
    ├───routes
    │   │   file.py
    │   │   user.py
    │   │
    │   └───__pycache__
    ├───static
    │   └───files
    └───templates
        │   display-file.html
        │   file.html
        │   home.html
        │   layout.html
        │   login.html
        │   register.html
        │   show-file.html
        │   upload-file.html
        │
        └───includes
                meta.html
                nav.html

## Run Locally

Clone the project

```bash
  git clone https://github.com/sidd6p/Project-X.git
```

Go to the project directory

```bash
  cd Project-X
```

Install dependencies

```bash
  pip install -r requirements.txt
```

build the project

```bash
  uvicorn app.main:app 
```


## Feature

- User Login and Registration
- Files Storage service
- Client application (web based) for file upload, download
- Access Control(currently owner can view file only)


## Upcoming Feature

- User based access control on who can access the files 
- Client application with rename, access control and delete
