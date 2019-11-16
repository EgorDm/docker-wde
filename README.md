# Dockerized Valet
It is more targetted as web dev environment which allows you freely change your environment do work on projects with different php version and plugin requirements. It also provides a few tools to manage the projects between the host and container. It is meant to reduce the annoyance of configuring your dev environment and switching between different configurations. 

# Installation
* Clone the repo `git clone git@github.com:EgorDm/docker-wde.git`
* Add environment variable ROOT_FOLDER linking to the cloned repo root
  ```
  cd docker-wde && export ROOT_FOLDER="$(pwd)"
  ```
* Install tools `cd docker-wde/tools && pip install .`
* Run `wde install`

# Usage
```
Usage: wde [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  db         Database commands
  down       Stops the wde environment
  exec       Executes given command in the container
  info       Shows information about the running containers
  install    Starts the wde environment
  restart    Restarts the wde environment
  secure     Secures given domain and adds self signed certificate as...
  switchphp  Changes the containers php version
  unsecure   Unecures given domain and removes self signed certificate from...
  up         Starts the wde environment
```

# Todo
* Automatic build
