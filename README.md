## Useful Docker Compose Commands

#### `docker-compose up -d --build`
* **Builds and runs in detached mode:**
  * **--build:** Forces rebuilding the services' images, even if they already exist locally.
  * **-d:** Runs the containers in detached mode, allowing you to free up the terminal for other tasks.
* **Usage:**  If you install new dependencies or if you change the `.env` file

#### `docker-compose up -d`
* **Runs in detached mode:**
  * **-d:** Same as the previous command, runs the containers in detached mode.
* **Usage:** Used when the images have already been built and you want to quickly start the services.

#### `docker-compose down`
* **Stops and removes containers:**
  * Stops all containers and removes networks created by Docker Compose.
* **Usage:** To stop and clean up a development or production environment.

### Other Useful Commands

#### `docker-compose ps`
* **List containers:** Shows a list of running containers defined in the `docker-compose.yml` file.

#### `docker-compose start`
* **Start containers:** Starts containers that are stopped.

#### `docker-compose stop`
* **Stop containers:** Stops running containers without removing them.

#### `docker-compose restart`
* **Restart containers:** Restarts running containers.

#### `docker-compose logs <service>`
* **View logs:** Shows the logs of a specific service.

#### `docker-compose exec <service> <command>`
* **Execute command in container:** Executes a command inside a running container.
