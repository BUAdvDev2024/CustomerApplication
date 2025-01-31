# API Documentation

## Endpoints

### 1. Home
- **URL:** `/`
- **Method:** `GET`
- **Description:** Loads the home page.
- **Response:**
    - `200 OK`: Returns the home page HTML.

### 2. Get All Data
- **URL:** `/api/get_data`
- **Method:** `GET`
- **Description:** Retrieves all data from the `menus.json` file.
- **Response:**
    - `200 OK`: Returns a JSON object containing all data.

### 3. Search Data
- **URL:** `/api/get_data/search`
- **Method:** `GET`
- **Description:** Searches data based on type and name.
- **Parameters:**
    - `area` (required, string): The area of search (`restaurants`, `menus`, `categories`, `items`).
    - `option` (required, string) Determines whether you search for name or to check if an area contains a value (`name`, `contains`)
    e.g To check if the Drinks menu contains Pepsi
    - `name` (required, string): The name to search for. (Use `*` to return all values)

    **Or**

    - `reward_eligible` (required, boolean): Whether an item is eligible as a reward (`true`, `false`)

    **Or**

    - `dietary_requirements` (required, string): The dietary requirement to search for. (Use `*` to return all values)

    - `id` (required, string): The id to search for. (Use `*` to return all values)
- **Response:**
    - `200 OK`: Returns a JSON array of search results.
    - `400 Bad Request`: Returns error message and response code if search parameters are invalid.
    - `404 Not found`: Returns error message and response code if no data is found.
- **Example URLs:** 
`/api/get_data/search?area=restaurants&option=name&name=RestaurantA`
`/api/get_data/search?reward_eligible=true`

### 4. Update Data
- **URL:** `/api/update_data`
- **Method:** `PUT`
- **Description:** Updates data in the `menus.json` file.
- **Request Body:**
    - `path` (required, array): The path to the data to be updated.
    - `newData` (required): The new data to update.
- **Response:**
    - `200 OK`: Returns the message `Data updated`.
    - `400 Bad Request`: Returns error message and response code if the request body is invalid or if an error is thrown.

### 5. Add Data
- **URL:** `/api/add_data`
- **Method:** `POST`
- **Description:** Adds new data to the `menus.json` file.
- **Request Body:**
    - `path` (required, array): The path to where the new data should be added.
    - `newData` (required): The new data to add.
- **Response:**
    - `200 OK`: Returns the message `Data added`.
    - `400 Bad Request`: Returns error message and response code if the request body is invalid or if an error is thrown.

### 6. Delete Data
- **URL:** `/api/delete_data`
- **Method:** `DELETE`
- **Description:** Deletes data from the `menus.json` file.
- **Request Body:**
    - `path` (required, array): The path to the data to be deleted.
- **Response:**
    - `200 OK`: Returns the message `Data deleted`.
    - `400 Bad Request`: Returns error message and response code if the request body is invalid or if an error is thrown.