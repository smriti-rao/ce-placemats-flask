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
[Here is how to 'activate' your shell](https://virtualenv.pypa.io/en/stable/userguide/#activate-script).
All commands should be entered from a shell that has been activated.

#### Install dependencies
`pip install -r requirements.txt` from the project root. If there are errors you may be missing
some system dependencies; Google the error message, package that's failing, and OS to figure out
what you need to install.

#### Import root directory into PyCharm as 'New Project'
Open PyCharm and then choose to import a project. Select the project root directory. PyCharm should detect
your virtual environment, but if not you should select the python interpreter (it's a binary) from within
the `.venv` directory.

#### Fix GeoText for Windows
[Fix GeoText](https://github.com/elyase/geotext/issues/3)
In geotext.py (one of our library dependencies), line 45, add `encoding='utf-8'` as a kwarg to `open`
e.g. change that line to:
```python
with open(filename, 'r', encoding='utf-8') as f:
```

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
python source files). Try running the previous command in the REPL during setup.
To test that it worked, run `configure_client()` and then run a search on pubmed using
`pubmed_search('alopecia areata treatment')`. The REPL is a useful tool whenever you need to double-check
the value of an expression or explore an API.

#### CLI (optional)
Both commands are run from the project root:

To run the HTTP server:
`FLASK_ENV=development FLASK_APP=app/main.py python3 -m flask run`

And the consumer:
`python3 -m app.placemats.consumer.widgets_task_consumer`

### Adding new dependencies
Whenever you add a new dependency, you have to make sure you update both `requirements.txt`
and re-run the docker image locally before deploying to make sure the container runs OK
still. To update `requirements.txt`, first `pip install` whatever packages you want to add
and then run `pip freeze > requirements.txt`. Caution: b.c.o. the way pip works, this will
snapshot all packages currently installed in your virtual environment. Be sure not to add
packages that are not actually used in code.


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

## Deploying the image as a VM
### Deploy MongoDB
You can choose how to host the MongoDB instance. In this case, I've chosen to deploy it as a docker container
similar to the steps outlined below except using a mongo image instead. You'll just need to make sure that
instance is accessible to the ce-placemats-flask app, and know the IP address/hostname to reach it.

### Deploy ce-placemats-flask app (Dockerfile)
The app is packaged as a minimal alpine image with only the necessary dependencies installed.
Supervisor is used to run two daemon processes: the flask http server and the queue consumer.

The below commands (bash script aliases) are what I use to deploy the docker
image. They should be run from the project's root directory, and do not require you to be in
an activated virtual environment shell. You'll need to make sure you're running relatively recent
versions of gcloud and docker, and that you're authorized to push to the conceptualeyes-169807 project's
image repository (gcr).
```bash
alias gcpDeploy='buildCePlacemats && gcpTagCePlacemats && gcpCePush'
alias gcpCePush='gcloud docker -- push us.gcr.io/conceptualeyes-169807/ce-placemats-flask:latest'
alias gcpTagCePlacemats='docker tag ce-placemats us.gcr.io/conceptualeyes-169807/ce-placemats-flask:latest'
alias buildCePlacemats='docker build -t ce-placemats .'
alias runCePlacemats='docker run -p 8080:80 -e NCBI_EMAIL=robot@gmail.com -e MONGO_URL=mongodb://host.docker.internal:27017 -e SKIP_AUTH0=TRUE ce-placemats'
alias buildAndRunCePlacemats='buildCePlacemats && runCePlacemats'
```
Once the image is uploaded, then go to the GCP console and set up a new VM. Select the container-optimized
VM image, and select the ce-placemats-flaks image. You'll need to make sure you're passing the correct value
of `MONGO_URL` and `NCBI_EMAIL` as environment variables to the VM (configurable via the console). This can
also be done via CLI too; here are
[the docs](https://cloud.google.com/compute/docs/containers/deploying-containers)

Currently there's a VM already running the placemats image, and it's configured to pull the latest, default
image (`:latest`). Check out
[the docs](https://cloud.google.com/compute/docs/containers/deploying-containers) for more details on
updating or changing the image the container is running.

### Deploy ce-placemats-flask app (Dockerfile) to GCP load balancer
Once you build, tag and push the local image to google cloud repository, you will need to 'bounce' (restart) all the instances in the instance group 'ce-placemats-2'.
