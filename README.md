# CMS-Backend

![GithubAction](https://github.com/NTUT-108-SE/CMS-Backend/workflows/Python%20package/badge.svg) [![codecov](https://codecov.io/gh/NTUT-108-SE/CMS-Backend/branch/master/graph/badge.svg)](https://codecov.io/gh/NTUT-108-SE/CMS-Backend) [![license:mit](https://img.shields.io/badge/license-mit-blue.svg)](https://opensource.org/licenses/MIT) ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/NTUT-108-SE/CMS-Backend)

A project for Clinic Management System backend

## Setup

```bash
pipenv install --dev
```

## Run

```bash
pipenv run python run.py
```

## Test

```bash
pipenv run python -m pytest --cov=./ --cov-report xml --cov-config=.coveragerc tests/
```
