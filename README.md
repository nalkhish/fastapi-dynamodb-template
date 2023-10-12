# Template for FastAPI backend and asynchronous DynamoDB

One of FastAPI's strengths is its design for asynchronous serving. Asynchronous backends can improve
resource utilization by using an asynchronous database. For example, see https://nalkhish.medium.com/should-you-use-django-asynchronous-support-f86ef611d29f

## Features

- An asynchronous DynamoDB ORM
- Some code maintenance opinions

## Installation

- poetry install

OR

- poetry export -f requirements.txt --output requirements.txt --without-hashes
- create and activate a python virtual environment
- pip install -r requirements.txt

## Usage

- Start the server for development: uvicorn template.main:app --reload
  If you use VsCode, this is already in a debug launch
- Modify the example replace_me package/microservice at your discretion
- Deploy how you see fit

## Contributing

Contributions are always welcome!

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
