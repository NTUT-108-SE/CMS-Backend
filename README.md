# CMS-Backend

![GithubAction](https://github.com/NTUT-108-SE/CMS-Backend/workflows/Python%20package/badge.svg) [![codecov](https://codecov.io/gh/NTUT-108-SE/CMS-Backend/branch/master/graph/badge.svg)](https://codecov.io/gh/NTUT-108-SE/CMS-Backend) [![GitHub](https://img.shields.io/github/license/NTUT-108-SE/CMS-Backend?color=blue)](https://github.com/NTUT-108-SE/CMS-Backend/blob/master/LICENSE) ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/NTUT-108-SE/CMS-Backend)

A project for [Clinic Management System](https://github.com/NTUT-108-SE/SE-CMS) backend

## Setup

```bash
pipenv install --dev
```

## Configuration

```bash
cp .environment.template .environment
vim .enviroment
```

## Run docker

```bash
docker-compose up -d
```

## Run

```bash
pipenv run python run.py
```

## Test

```bash
pipenv run python -m pytest --cov=./ --cov-report term-missing --cov-config=.coveragerc tests/
```

## Coding style

```
pipenv run yapf -i -r .
```

## Contribute

Before commit or PR  
Please pass the **test** and keep the same **coding style**.
