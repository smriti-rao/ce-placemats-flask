## Get the code
`git clone https://github.com/guerard/ce-placemats-flask.git && cd ce-placemats-flask` The directory you're
in now is what's considered the project root.

## Running the code locally
### Dependencies
#### MongoDB
[Install MongoDB](https://docs.mongodb.com/manual/installation/) and run a local instance.

#### python3, virtualenv
[Install python3](https://www.python.org/downloads/)

[Install virtualenv](https://virtualenv.pypa.io/en/stable/installation/)

#### IDE: PyCharm
[PyCharm](https://www.jetbrains.com/pycharm/download/#) is the best IDE for writing python.

### Set up
#### Set up virtual environment
In python projects we isolate our dependencies to a given project using a tool called `virtualenv`.
Inside the project root you should create your virtual environment by running:
`virtualenv -p python3 .venv`

To actually use the virtual environment you'll need to prepare your shell so that all python-related
commands take effect there (and only there).
[The docs for how to 'activate' your shell](https://virtualenv.pypa.io/en/stable/userguide/#activate-script)
All commands should be entered from a shell that has been actived.

#### Install dependencies
`pip install -r requirements.txt` from the project root. If there are errors you may be missing
some system dependencies; Google the error message, package that's failing, and OS to figure out
what you need to install.

#### Import root directory into PyCharm as 'New Project'
Open PyCharm and then choose to import a project. Select the project root directory. PyCharm should detect
your virtual environment, but if not you should select the python interpreter (it's a binary) from within
the `.venv` directory.

### Running the code
#### PyCharm run commands
PyCharm should detect the runConfigurations from within the `.idea` directory. These contain the commands
needed to run both the http server ('flask run') and the task consumer ('consumer'). The run commands are
selected in the top-right of the IDE near the Play and Debug buttons. After choosing a run command from the
drop down, run it using the Play button.

`flask run` runs the HTTP server on [127.0.0.1:5000](http://127.0.0.1:5000)

`consumer` starts the task consumer

#### PyCharm REPL
Best thing about python is being able to run code in a shell-like environment a.k.a. "the REPL".
PyCharm's 'Python Console' will open a python shell associated with the project's virtual environment.
From there you can import code just as you would in source code e.g.
`from app.placemats.data.ncbi_client import *` would run the code in that package, and import all the defined
classes and functions into the current shell's scope (similar to how importing a package works when writing
python source files). To test it out, run `configure_client()` and then run a search on pubmed using
`pubmed_search('alopecia areata treatment')`. The REPL is a useful tool whenever you need to double-check
the value of an expression or explore an API.

#### CLI
To run the HTTP server you'll need to first `cd app`.
Then run `FLASK_ENV=development PYTHONPATH=../ FLASK_APP=main.py python3 -m flask run`

The task consumer should be run from the project root using the command:
`python3 -m app.placemats.consumer.widgets_task_consumer`


## Running as a docker image
### Building and running
Run `docker-compose build && docker-compose up` from the project root directory.
The API will be served on [127.0.0.1:8080](http://127.0.0.1:8080)

## API's
### Pagination
All list endpoints support pagination via the `limit` and `skip` query parameters. `limit` is
the max. count to return, and `skip` determines the starting index.

#### Create/get a layout
`GET /layouts/<search terms>`

#### List all layouts
`GET /layouts/` -- Max. limit: 50

#### Get widget
`GET /widgets/<widget_id>`

#### List widgets
`GET /widgets/` -- Max. limit: 10
