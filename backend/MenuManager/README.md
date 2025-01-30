# MenuManager

MenuManager is a simple API designed to manage restaurants menus. It comes with a webpage that allows users to read, create, update, add, and delete parts of each resteraunts menu. The idea is to evetualy replace this with a database but for the imediate future this will be the solution.

You can access the API using either:
- http://localhost:8080/
- http://127.0.0.1:8080/

## TODO

- [x] Add a webpage for viewing and managing data
- [x] Add the other API endpoints
- [x] Add styling for the webpage
- [ ] Add more information about menu items
- [X] Add better documentation for this API

## How to Use

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/BUAdvDev2024/MenuManager.git
    cd MenuManager
    ```

2. **Build the Container**:
    ```sh
    docker build -t menumanager .
    ```

3. **Compose**:
    ```sh
    docker compose up
    ```

4. **API Endpoints**:
    - **GET /api/get_data**: Retrieve all menu items.
    - **GET /api/get_data/search?area=&option=&name=** : or : **/api/get_data/search?reward_eligible=** : or : **/api/get_data/search?dietary_requiremnts=** (see documentation)
    - **POST /api/add_data**:
    - **PUT /api/update_data**:
    - **DELETE /api/delete_data**:
