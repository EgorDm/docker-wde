# Dockerized Valet
It is more targetted as web dev environment which allows you freely change your environment do work on projects with different php version and plugin requirements. It also provides a few tools to manage the projects between the host and container. It is meant to reduce the annoyance of configuring your dev environment and switching between different configurations. 

# Usage
* Clone the git
* Run the setup.sh
* Run source commands.sh and/or add this command to start of your shell.
* Call command wde_up to build and start the container
* Call wde_down to stop it.

# Todo
* Move commands to python
* Remove a few hardcoded values in startup script
* Opcache and xdebug configuration
* Automatic build
