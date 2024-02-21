# AI Email Tools

This project is an experimental playground for using LLMs to do interesting things with my inbox

## Installation

This project utilizes Poetry

```shell
curl -sSL https://install.python-poetry.org | python -
poetry new my_project
cd my_project
poetry install
```

## Configuration

### OpenAI

Create a .env file and provide your OpenAI API key

### Gmail

This tool assumes that email is coming from Gmail accounts.
This requires you to setup a Google cloud project and download a credentials file.
Google is your friend here, more documentation is to come.

## Usage

```shell
poetry run aitools --help
```


## TODO

- I'd like to refactor the aitools.py module to inject differenet LLMS so I can experiments with local LLMs w/o having
to keep changing the summarizer and classifier
- Move the prompts into external config files

