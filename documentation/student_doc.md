# SYSTEM DESCRIPTION:

DockNStock is a distributed retail platform that connects supermarkets with end customers.  
The system allows customers to register and log in, browse products, like them, comment on them and manage a shopping cart to place orders.  
Supermarkets can register on the platform, receive incoming orders and manage their catalogs by adding products and updating stock.  
The architecture is based on Dockerized microservices, ensuring scalability, modularity and easy deployment.  
A PostgreSQL database guarantees data persistence, while dedicated API services manage user accounts, products, interactions and orders.  

# USER STORIES:

1) As a Customer, I want to register, so that I can create my profile  
2) As a Customer, I want to login, so that I can access the service  
3) As a Customer, I want to logout, so that I can end my session securely  
4) As a Customer, I want to recover my password, so that I can regain access to my account  
5) As a Customer, I want to view all available products, so that I can choose what to buy  
6) As a Customer, I want to view product details, so that I can evaluate them before buying  
7) As a Customer, I want to like a product, so that I can express my preference  
8) As a Customer, I want to unlike a product, so that I can change my mind  
9) As a Customer, I want to view the list of liked products, so that I can access them quickly  
10) As a Customer, I want to comment on a product, so that I can share my opinion  
11) As a Customer, I want to view product comments, so that I can read other users’ feedback  
12) As a Customer, I want to add products to my cart, so that I can prepare for checkout  
13) As a Customer, I want to remove products from my cart, so that I can adjust my order  
14) As a Customer, I want to view all products in my cart, so that I can review my selection  
15) As a Customer, I want to select the quantity of each product in my cart, so that I can customize my purchase  
16) As a Customer, I want to submit my cart, so that I can place an order  
17) As a Customer, I want to receive a confirmation message when the order is placed, so that I know it was successful  
18) As a Customer, I want to receive an error message if the requested quantity is not available, so that I can adjust my cart  
19) As a Supermarket, I want to register, so that I can create my business account  
20) As a Supermarket, I want to login, so that I can manage my catalog and orders  
21) As a Supermarket, I want to logout, so that I can end my session securely  
22) As a Supermarket, I want to recover my password, so that I can regain access to my account  
23) As a Supermarket, I want to add new products, so that I can expand my catalog  
24) As a Supermarket, I want to view the list of all my products, so that I can manage and monitor my catalog
25) As a Supermarket, I want to view received orders, so that I can process them  
26) As a Supermarket, I want to update the details of my products, so that the catalog is always accurate  
27) As a Supermarket, I want to update only the quantity of a product, so that stock levels are kept accurate  

# CONTAINERS: 

## CONTAINER_NAME: Customer Interface

### DESCRIPTION:
Manages all functionalities related to customer interaction: registration, login, logout, password recovery via email, browsing products, liking/unliking, posting and reading comments, managing the shopping cart, and placing orders.

### USER STORIES:
1–18

### PORTS:
5000:5000

### PERSISTENCE EVALUATION:
The Customer Interface container does not include persistence. It is stateless and relies on the Database API for storing and retrieving data.

### EXTERNAL SERVICES CONNECTIONS:
The container connects to:  
- Database API (REST) for authentication, products, likes, comments, cart and orders  
- SMTP server (port 465) for password recovery emails  

### MICROSERVICES:

#### MICROSERVICE: customer-interface
- TYPE: frontend  
- DESCRIPTION: Provides the front-end web application for customers.  
- PORTS: 5000  
- TECHNOLOGICAL SPECIFICATION:
  - Python 3  
  - Flask (web framework)  
  - Flask-Login (session management)  
  - Flask-Mail (password recovery)  
  - Jinja2 (templating engine)  
  - Requests (HTTP client for communication with Database API)  
- SERVICE ARCHITECTURE:
  - Routes defined in `app.py` manage authentication, product interactions, comments, cart, and orders.
  - Uses `config.py` for secret key and mail configuration.  
- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
    | ----------- | --- | ----------- | ------------ |
    | GET, POST | /register | Register a new account | 1 |
    | GET, POST | /login | Authenticate and start a session | 2 |
    | GET | /logout | End session | 3 |
    | GET, POST | /forget | Request password reset via email | 4 |
    | GET, POST | /forget/<token>/confirm | Set new password with token | 4 |
    | GET | /home | Display customer dashboard | 5, 6 |
    | POST | /leavealike | Like/unlike a product | 7, 8 |
    | GET | /likes | View liked products | 9 |
    | POST | /postcomments | Post a comment on a product | 10 |
    | GET | /comments | View all comments on a product | 11 |
    | POST | /addtocart | Add product to cart | 12 |
    | POST | /remove_from_cart | Remove item from cart | 13 |
    | GET | /shopping_cart | View cart content | 14, 15 |
    | POST | /cart/submit | Submit the cart and place order | 16, 17, 18 |


## CONTAINER_NAME: Business Interface

### DESCRIPTION:
Manages all functionalities related to supermarket interaction: registration, login, logout, password recovery via email, viewing products, adding and updating products, and managing incoming orders.

### USER STORIES:
19–27

### PORTS:
5001:5000

### PERSISTENCE EVALUATION:
The Business Interface container does not include persistence. It is stateless and relies on the Database API for storing and retrieving data, and on an SMTP service for password recovery.

### EXTERNAL SERVICES CONNECTIONS:
The container connects to:  
- Database API (REST) for supermarket authentication, product management and order management  
- SMTP server (port 465) for password recovery emails  

### MICROSERVICES:

#### MICROSERVICE: business-interface
- TYPE: frontend  
- DESCRIPTION: Provides the front-end web application for supermarkets.  
- PORTS: 5000  
- TECHNOLOGICAL SPECIFICATION:
  - Python 3  
  - Flask (web framework)  
  - Flask-Login (session management)  
  - Flask-Mail (password recovery)  
  - Jinja2 (templating engine)  
  - Requests (HTTP client for communication with Database API)  
- SERVICE ARCHITECTURE:
  - Routes defined in `app.py` manage authentication, password recovery, product creation/update, stock management and orders.  
  - Uses `config.py` for secret key and mail configuration.  
- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
    | ----------- | --- | ----------- | ------------ |
    | GET, POST | /register | Register a new supermarket account | 19 |
    | GET, POST | /login | Authenticate and start a session | 20 |
    | GET | /logout | End session | 21 |
    | GET, POST | /forget | Request password reset via email | 22 |
    | GET, POST | /forget/<token>/confirm | Set new password with token | 22 |
    | GET, POST | /home | Dashboard with product management | 23, 26, 27 |
    | GET | /orders | View incoming orders | 25 |
    | GET | /products | View all products in platform | 24 |


## CONTAINER_NAME: Database API

### DESCRIPTION:
Provides the back-end REST API that manages all persistent data and operations: user accounts, supermarket accounts, product catalog, likes, wants, owns, comments, cart and orders.  
It serves as the communication layer between the front-end interfaces (Customer and Business) and the PostgreSQL database.

### USER STORIES:
Supports all customer and supermarket stories (1–27).  

### PORTS:
5002:5002

### PERSISTENCE EVALUATION:
The container ensures persistence by interfacing directly with the PostgreSQL database (running in a separate container).

### EXTERNAL SERVICES CONNECTIONS:
- PostgreSQL database (port 5432), accessed through SQLAlchemy ORM and psycopg2 driver.

### MICROSERVICES:

#### MICROSERVICE: db-api
- TYPE: backend REST API
- DESCRIPTION: Provides REST endpoints for managing users, supermarkets, products, likes, wants, owns, comments, cart and orders.
- PORTS: 5002
- TECHNOLOGICAL SPECIFICATION:
  - Python 3  
  - Flask (web framework)  
  - Flask-SQLAlchemy (ORM)  
  - Flask-Login (auth helpers)  
  - psycopg2-binary (PostgreSQL driver)  
- SERVICE ARCHITECTURE:
  - Routes are organized in blueprints: `user_bp`, `supermarket_bp`, `product_bp`, `like_bp`, `comment_bp`, `cart_bp`, `owns_bp`, `wants_bp`, `orders_bp`.
  - Models defined in `models.py` (Users, Supermarkets, Products, Likes, Owns, Wants, Comments, Orders).
- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
    | ----------- | --- | ----------- | ------------ |
    | POST | /users/register | Register new customer | 1 |
    | POST | /users/login | Authenticate customer | 2 |
    | GET | /users/<user_id> | Retrieve user info | 5, 6 |
    | POST | /users/change_password | Change password | 4 |
    | GET | /users/<user_id>/likes | Get all liked products | 7–9 |
    | POST | /supermarkets/register | Register supermarket | 19 |
    | POST | /supermarkets/login | Authenticate supermarket | 20 |
    | GET | /supermarkets/<supermarket_id> | Retrieve supermarket info | 19–20 |
    | POST | /supermarkets/change_password | Change supermarket password | 22 |
    | POST | /products | Create a new product | 23 |
    | GET | /products | Get all products | 5, 24 |
    | GET | /products/<prod_id> | Get product by ID | 6 |
    | PUT | /products/<prod_id> | Update product details | 26 |
    | DELETE | /products/<prod_id> | Delete a product | - |
    | PUT | /products/<prod_id>/quantity | Update product quantity | 27 |
    | POST | /like/<user_id>/<product_id> | Toggle like/unlike | 7, 8 |
    | POST | /comment | Create new comment | 10 |
    | GET | /product_comments/<product_id> | Get comments for a product | 11 |
    | POST | /wants | Add product to wants | 12, 15 |
    | PUT | /wants | Update wanted quantity | 15 |
    | GET | /wants/<user_id> | Retrieve wants by user | 14 |
    | POST | /wants/remove | Remove product from wants | 13 |
    | POST | /orders | Create order | 16–18 |
    | GET | /orders/<user_id> | Retrieve all orders for a user | 16, 17 |
    | GET | /supermarket_orders/<supermarket_id> | Retrieve supermarket orders | 25 |
    | GET | /supermarket_orders/grouped/<supermarket_id> | Retrieve supermarket orders grouped by user | 25 |

### DATABASE STRUCTURE:
The relational schema managed by the API (defined in `models.py`) includes:

- **Users**  
  - `id` (PK), `username` (unique), `password` (hashed)
- **Supermarkets**  
  - `id` (PK), `supermarketname` (unique), `password` (hashed)
- **Products**  
  - `id` (PK), `name`, `weight`, `photo`, `description`
- **Likes**  
  - `users_id` (FK → Users.id), `products_id` (FK → Products.id)
- **Owns**  
  - `market_id` (FK → Supermarkets.id), `products_id` (FK → Products.id), `quantity`
- **Wants**  
  - `user_id` (FK → Users.id), `products_id` (FK → Products.id), `quantity`
- **Comments**  
  - `id` (PK), `users_id` (FK), `products_id` (FK), `comment`
- **Orders**  
  - `id` (PK), `user_id` (FK), `supermarket_id` (FK), `product_id` (FK), `order_quantity`


## CONTAINER_NAME: Database

### DESCRIPTION:
PostgreSQL database used for persistent storage of all system data: users, supermarkets, products, likes, owns, wants, comments and orders.

### USER STORIES:
Supports all stories that require persistent data (1–27).

### PORTS:
5432:5432

### PERSISTENCE EVALUATION:
Ensures full persistence by maintaining relational tables with mounted volumes for durability across container restarts.

### EXTERNAL SERVICES CONNECTIONS:
- Accessed exclusively by the Database API container through SQLAlchemy and psycopg2.

### MICROSERVICES:

#### MICROSERVICE: postgres-db
- TYPE: database  
- DESCRIPTION: PostgreSQL instance providing relational persistence.  
- PORTS: 5432  
- TECHNOLOGICAL SPECIFICATION:
  - PostgreSQL 13+  
- SERVICE ARCHITECTURE:
  - Exposes standard PostgreSQL protocol on port 5432.
  - No direct exposure to front-end; only accessible by Database API.  
- DATABASE STRUCTURE:
  - As described in Database API.  