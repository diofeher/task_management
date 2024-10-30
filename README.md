This project is used as a template for an application with the following features:

General:
- Pre-commit hooks for using the linting automatically

Backend:
- FastAPI as the Webserver
- PostgresQL + sqlalchemy on the Backend
- Alembi for Database migrations
- Containerization with Docker and Uvicorn for serving
- Ruff for style checks


# Installation

First, we will need to install the dependencies and pre-commit hooks.
For convenience, I added the setup file for Mac OS. If you don't use homebrew, you need to install it from https://brew.sh/.

```
brew bundle
```

After that, you need to install the pre-commit hooks:

```
pre-commit install
```
