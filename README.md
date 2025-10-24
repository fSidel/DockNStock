# StockNDock

## How to Run the Project

### Prerequisites
1. Install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/).

2. Clone the repository:
    ```bash
   git clone https://github.com/your-username/StockDock.git
   

3. Compose with Docker
    ```bash
   docker-compose up

5. The services will be available at the following ports:
    - service_interface: http://localhost:5001
    - service_flask: http://localhost:5002
    - PostgreSQL Database: Port 5432
    Ensure they are not in use by other applications when running
    the project. To stop the services use
