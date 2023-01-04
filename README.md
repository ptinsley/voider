# voider

A lot of modern online banks don't issue checks, especially ones like Qube, One Finance etc... that work on the idea of bank accounts for each vendor/bill. I've found that some utility providers still expect to get a voided check to establish or update auto draft. The goal of this project is to make arbitrary void checks as needed to setup auto draft for different providers.

## Local Development

Loading dependencies
```bash
pip3 install -r requirements.txt
```

Running the app with automatic reload as code is changed
```bash
FLASK_APP=voider flask --debug run
```

## Deploying the application

The repo has the configuration for my specific deployment on fly.io, that is what I'm talking about here.

```bash
flyctl deploy
```