This project is used as a template for an application with the following features:

General:
- Pre-commit hooks for using the linting automatically

Backend:
- FastAPI as the Webserver
- PostgresQL + sqlalchemy on the Backend

- Containerization with Docker and Uvicorn for serving
- Ruff for style checks
- Github Actions as CI/CD for automatic code checking, using Ruff and ESLint

Frontend:
- Usage of React and Next.js
- Custom CSS, no libraries
- Usage of ESLint for linting
- Containerization with Docker and Docker compose

TODO:
- Alembi for Database migrations
- mypy for static type checking 


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

This means every time you're committing, the linters are activated to lint and format your code.

There's a Github action for making sure the code is compliant even if lint were bypassed locally.

# Running 

To run the whole application, run with docker compose.

```
docker compose up
```
