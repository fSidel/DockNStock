# SYSTEM DESCRIPTION:

DockNStock is a distributed retail platform that connects supermarkets with end customers.  
The system allows customers to register and log in, browse products, like them, comment on them and manage a shopping cart to place orders.  
Supermarkets can register on the platform, receive incoming orders and manage their catalogs by adding products. 
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
24) As a Supermarket, I want to view my products, so that I can manage them  
25) As a Supermarket, I want to view received orders, so that I can process them

# CONTAINERS: 

## CONTAINER_NAME: Customer Interface

### DESCRIPTION:
Manages all functionalities related to customer interaction: registration, login, logout, password recovery via email, browsing products, liking/unliking, posting and reading comments, and managing the shopping cart.

### USER STORIES:
1) As a Customer, I want to register to the site so that I can create my profile  
2) As a Customer, I want to login to the site so that I can access the services  
3) As a Customer, I want to logout so that I can end my session securely  
4) As a Customer, I want to recover my password so that I can regain access if I forget it  
5) As a Customer, I want to view all available products so that I can decide what to buy  
6) As a Customer, I want to view the details of a product so that I can evaluate it  
7) As a Customer, I want to like a product so that I can express my preference  
8) As a Customer, I want to unlike a product so that I can change my mind  
9) As a Customer, I want to view the list of products I liked so that I can access them quickly  
10) As a Customer, I want to comment on a product so that I can share my opinion  
11) As a Customer, I want to view all comments on a product so that I can read other users’ opinions  
12) As a Customer, I want to add products to my cart so that I can prepare for checkout  
13) As a Customer, I want to select the quantity of each product in my cart so that I can customize my purchase  
14) As a Customer, I want to view all products in my cart so that I can review my selection before submitting  
15) As a Customer, I want to submit my cart so that the system places an order and clears the cart  
16) As a Customer, I want to receive a confirmation message so that I know my order was submitted  
17) As a Customer, I want to receive an error message if the product quantity is insufficient  
18) As a Customer, I want to see a notification when the order is correctly placed  

### PORTS:
5000:5000

### PERSISTENCE EVALUATION:
The Customer Interface container does not include persistence. It is stateless and relies on the Database API for storing and retrieving data.

### EXTERNAL SERVICES CONNECTIONS:
The container connects to:
- Database API (REST) for authentication, products, likes, comments, and cart operations  
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
  - Routes defined in `app.py` manage authentication, product interactions, comments, and cart actions.
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
    | POST | /addtocart | Add or toggle product in cart | 12 |
    | GET | /shopping_cart | View cart content | 13, 14 |
    | POST | /remove_from_cart | Remove item from cart | 13 |
    | POST | /cart/submit | Submit the cart and place order | 15, 16, 17, 18 |


## CONTAINER_NAME: Business Interface

### DESCRIPTION:
Manages all functionalities related to supermarket interaction: registration, login, logout, password recovery via email, and product creation through the dashboard.  
It communicates with the Database API for authentication, user presence checks, and product submission.

### USER STORIES:
19) As a Supermarket, I want to register so that I can create my business account  
20) As a Supermarket, I want to login so that I can manage my catalog  
21) As a Supermarket, I want to logout so that I can end my session securely  
22) As a Supermarket, I want to recover my password so that I can regain access if I forget it  
23) As a Supermarket, I want to add new products so that I can expand my catalog 
24) As a Supermarket, I want to view my products, so that I can manage them  
25) As a Supermarket, I want to view received orders, so that I can process them

### PORTS:
5001:5000

### PERSISTENCE EVALUATION:
The Business Interface container does not include persistence. It is stateless and relies on the Database API for storing and retrieving data, and on an SMTP service for password recovery.

### EXTERNAL SERVICES CONNECTIONS:
The container connects to:  
- **Database API (REST)** for supermarket authentication, user presence checks, and product management  
- **SMTP server (port 465)** for password recovery emails  

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
  - Routes defined in `app.py` manage authentication, password recovery, and product creation.  
  - Uses `config.py` for secret key and mail configuration.  
  - Product creation form (`/home`) allows supermarkets to submit product details (name, weight, photo, description, quantity) to the Database API.  
- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
    | ----------- | --- | ----------- | ------------ |
    | GET, POST | /register | Register a new supermarket account | 19 |
    | GET, POST | /login | Authenticate and start a session | 20 |
    | GET | /logout | End session | 21 |
    | GET, POST | /forget | Request password reset via email | 22 |
    | GET, POST | /forget/<token>/confirm | Set new password with token | 22 |
    | GET, POST | /home | Dashboard with product creation form | 23 |
    | GET | / | Redirect to `/home` if authenticated, otherwise to `/register` | - |
    | GET | /<something> | Redirect to main route (catch-all) | - |


## CONTAINER_NAME: Database API

### DESCRIPTION:
Provides the back-end REST API that manages all persistent data and operations: user accounts, supermarket accounts, product catalog, likes, comments, and shopping cart. It serves as the communication layer between the front-end interfaces (Customer and Business) and the PostgreSQL database.

### USER STORIES:
- Supports all customer and supermarket stories (1–25).  
- Responsible for persistence, validation, and retrieval of data.

### PORTS:
5002:5002

### PERSISTENCE EVALUATION:
The container ensures persistence by interfacing directly with the PostgreSQL database (running in a separate container). All CRUD operations for users, supermarkets, products, likes, comments, and cart are stored in relational tables.

### EXTERNAL SERVICES CONNECTIONS:
- PostgreSQL database (port 5432), accessed through SQLAlchemy ORM and psycopg2 driver.

### MICROSERVICES:

#### MICROSERVICE: db-api
- TYPE: backend REST API
- DESCRIPTION: Provides REST endpoints for managing users, supermarkets, products, likes, comments, and cart.
- PORTS: 5002
- TECHNOLOGICAL SPECIFICATION:
  - Python 3
  - Flask (web framework)
  - Flask-SQLAlchemy (ORM)
  - Flask-Login (auth helpers)
  - psycopg2-binary (PostgreSQL driver)
- SERVICE ARCHITECTURE:
  - Routes are organized in blueprints: `user_bp`, `supermarket_bp`, `product_bp`, `like_bp`, `comment_bp`, `cart_bp`.
  - Models defined in `models.py` (Users, Supermarkets, Products, Likes, Comments, Cart).
  - `fill_db.sql` and `seed.py` used for database initialization.
- ENDPOINTS:

    | HTTP METHOD | URL | Description | User Stories |
    | ----------- | --- | ----------- | ------------ |
    | POST | /users/register | Register new customer | 1 |
    | POST | /users/login | Authenticate customer | 2 |
    | POST | /users/present | Check if a user exists | 1–2 |
    | GET | /users/<user_id> | Retrieve user info | 5, 6 |
    | POST | /users/change_password | Change password | 4 |
    | GET | /users/<user_id>/likes | Get all liked products | 7–9 |
    | POST | /supermarkets/register | Register supermarket | 19 |
    | POST | /supermarkets/login | Authenticate supermarket | 20 |
    | GET | /supermarkets/<user_id> | Retrieve supermarket info | 19–20 |
    | POST | /supermarkets/change_password | Change supermarket password | 20 |
    | POST | /products | Create a new product | 21 |
    | GET | /products | Get all products | 5 |
    | GET | /products/<prod_id> | Get product by ID | 6 |
    | PUT | /products/<prod_id> | Update product details | 22 |
    | DELETE | /products/<prod_id> | Delete a product | 23 |
    | GET | /products/like/<user_id> | Get products liked by a user | 7–9 |
    | POST | /like/<user_id>/<product_id> | Toggle like/unlike | 7–8 |
    | POST | /comment | Create new comment | 10 |
    | GET | /get_comments | Get all comments | 11 |
    | GET | /user_comment/<user_id> | Get comments by user | 11 |
    | GET | /product_comments/<product_id> | Get comments for a product | 11 |
    | POST | /cart | Add product to cart (toggle add/remove) | 12, 13 |
    | GET | /cart/<user_id> | View user’s cart | 14 |
    | POST | /cart/remove | Remove product from cart | 13 |
    | POST | /cart/submit | Submit cart and place order | 15–18 |

### DATABASE STRUCTURE:
The relational schema managed by the API (defined in `models.py`) includes:

- **Users**  
  - `id` (PK), `username` (unique), `password` (hashed)
- **Supermarkets**  
  - `id` (PK), `supermarketname` (unique), `password` (hashed)
- **Products**  
  - `id` (PK), `name`, `weight`, `photo`, `description`
- **Likes**  
  - `users_id` (FK → Users.id), `products_id` (FK → Products.id) — composite PK
- **Comments**  
  - `id` (PK), `users_id` (FK), `products_id` (FK), `comment`
- **Cart**  
  - `id` (PK), `users_id` (FK), `products_id` (FK)
- **Orders** *(planned)*  
  - `id` (PK), `users_id` (FK), line items (product, quantity, price snapshot)

---

## CONTAINER_NAME: Database

### DESCRIPTION:
PostgreSQL database used for persistent storage of all system data: users, supermarkets, products, likes, comments, and shopping cart. Planned extensions will include orders and advanced analytics.

### USER STORIES:
Supports all stories that require persistent data (1–25).

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
  - Tables initialized through `fill_db.sql` and optionally `seed.py`
- SERVICE ARCHITECTURE:
  - Exposes standard PostgreSQL protocol on port 5432.
  - No direct exposure to front-end; only accessible by Database API.

### DATABASE STRUCTURE:
- **Users**: id, username, password  
- **Supermarkets**: id, supermarketname, password  
- **Products**: id, name, weight, photo, description  
- **Likes**: users_id, products_id  
- **Comments**: id, users_id, products_id, comment  
- **Cart**: id, users_id, products_id  
- **Orders** (planned): id, users_id, product list, quantities
