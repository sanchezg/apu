# Yet another python telegram bot to keep expenses save (?)

## Requirements

Install Python 3.10+ with your preferred method. Then pip-install requirements.

```
$ pyenv install 3.10.4
$ pyenv virtualenv apu-dev 3.10.4
$ pyenv local apu-dev

$ pip install -r requirements.txt
```

## Getting started

This was developed using telegram webhooks (connected to an AWS lambda function). Please set up your AWS credentials account and install serverless:

```
npm install -g serverless
```

Copy `env.yml.dist` as `env.yml` and store there your personal keys.

Deploy this project with:

```
sls deploy
```
