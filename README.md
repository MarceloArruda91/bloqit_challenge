# Bloqit API

Bloqit is a company that builds software to assist first, middle, and last-mile deliveries. This API facilitates the management of Bloqs, Lockers, and Rents to support the delivery process.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/bloqit_api.git
    cd bloqit_api
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

1. Start the Flask server:
    ```bash
    export FLASK_APP=run.py
    flask run
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`. This will redirect you to the Swagger documentation at `http://127.0.0.1:5000/apidocs`.

## API Endpoints

### Bloqs

- **GET /api/bloqs**: Retrieve a list of all Bloqs.
- **POST /api/bloqs**: Create a new Bloq.
- **GET /api/bloqs/{bloq_id}**: Retrieve a specific Bloq by its ID.

### Lockers

- **GET /api/lockers**: Retrieve a list of all Lockers.
- **POST /api/lockers**: Create a new Locker.
- **GET /api/lockers/{locker_id}**: Retrieve a specific Locker by its ID.
- **PUT /api/lockers/{locker_id}/status**: Update the status of a Locker.

### Rents

- **GET /api/rents**: Retrieve a list of all Rents.
- **POST /api/rents/rent**: Create a new Rent.
- **GET /api/rents/{rent_id}**: Retrieve a specific Rent by its ID.
- **PUT /api/rents/{rent_id}/status**: Update the status of a Rent.
- **PUT /api/rents/{rent_id}/assign**: Assign a locker to a rent.

## Testing

Run the tests using:
```bash
python -m unittest discover tests