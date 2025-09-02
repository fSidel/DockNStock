# Student Documentation - StockNDock

## System Description

StockNDock is a distributed retail platform that connects supermarkets with end customers.  
Customers can register, log in, browse products, like and comment on them and manage a shopping cart to place orders.  
Supermarkets can register, manage their catalogs by adding, updating and removing products, and receive incoming orders.  
The architecture is based on Dockerized microservices, ensuring scalability, modularity and easy deployment.  
A PostgreSQL database guarantees data persistence, while dedicated API services manage user accounts, products, interactions and orders.  

---

## User Stories

// ** to check

1) As a customer, I want to register to the site so that I can create my profile.  
2) As a customer, I want to login to the site so that I can access the services.  
3) As a customer, I want to logout so that I can end my session securely.  
4) As a customer, I want to recover my password so that I can regain access to my account if I forget it.  
5) As a customer, I want to view all available products so that I can decide what to buy.  
6) As a customer, I want to view the details of a product so that I can evaluate it.  
7) As a customer, I want to like a product so that I can express my preference.  
**8) As a customer, I want to unlike a product so that I can change my mind.  
9) As a customer, I want to view the list of products I liked so that I can access them quickly.  
10) As a customer, I want to comment on a product so that I can share my opinion.  
**11) As a customer, I want to view all comments on a product so that I can read other users’ opinions.  
12) As a customer, I want to add products to my cart from the homepage so that I can prepare for checkout.  
13) As a customer, I want to select the quantity of each product in my cart so that I can customize my purchase.  
14) As a customer, I want to view all products in my cart so that I can review my selection before submitting.  
15) As a customer, I want to submit my cart so that the system places an order and clears the cart.  
16) As a customer, I want to receive a confirmation message (“order correctly placed”) so that I know my order was submitted.  

17) As a supermarket, I want to register to the site so that I can start managing my store online.  
18) As a supermarket, I want to login so that I can manage my catalog and orders. 
19) As a supermarket, I want to logout so that I can end my session securely.  
20) As a supermarket, I want to recover my password so that I can regain access to my account if I forget it.  

// rivedere quando si implementa lato supermarket 
**20) As a supermarket, I want to add new products so that I can expand my catalog.  
**21) As a supermarket, I want to update products so that I can modify price, description, or availability.  
**22) As a supermarket, I want to remove products so that I can keep my catalog up to date.  
**23) As a supermarket, I want to view orders so that I can process purchases made by customers.  
**24) As a supermarket, I want to see statistics about sold products so that I can analyze performance.  
**25) As a supermarket, I want to receive suggestions for inventory restocking so that I can anticipate demand.  

---

## Containers

### 1. Customer Interface
- **Description**:  
  Front-end web application for customers. It allows users to register, log in, view products, like/unlike products, comment and manage a shopping cart.  
- **User stories implemented**: 1–16  
- **Port exposed**: 5000  
- **Persistence**: No (stateless, relies on Database API).  
- **External connections**: Connects to the Database API to fetch products, authenticate users and manage actions (likes, comments, cart).  
- **Microservices**:  
  - Customer session manager  
  - Product viewer  
  - Cart manager  
- **Endpoints** (internal routes):  
  - `/register`  
  - `/login`  
  - `/logout`  
  - `/home`  
  - `/cart`  

---

### 2. Business Interface (placeholder)
- **Description**:    
- **User stories planned**:   
- **Port exposed**: 5001  
- **Persistence**: No (stateless, relies on Database API).  
- **External connections**:   
- **Microservices**:  
  - 
  - 
- **Endpoints**:  
    

---

### 3. Database API
- **Description**:  
  Back-end service exposing REST APIs to handle users, products, likes, comments, cart and orders.  
- **User stories implemented**: All core stories.  
- **Port exposed**: 5002  
- **Persistence**: Yes (via PostgreSQL).  
- **External connections**: Connects to the PostgreSQL database.  
- **Microservices**:  
  - User management service  
  - Product management service  
  - Like and comment service  
  - Cart and order service  

#### Endpoints

**User Management**
- `POST /users/register` → Register a new user.  
- `POST /users/login` → Authenticate a user.  
- `POST /users/present` → Check if a user exists by username.  
- `GET /users/<user_id>` → Get user info by ID.  
- `POST /users/change_password` → Change password.  
- `GET /users/<user_id>/likes` → Get all products liked by a user.  

**Product Management**
- `POST /products` → Create a new product.  
- `GET /products` → Get all products.  
- `GET /products/<prod_id>` → Get a product by ID.  
- `PUT /products/<prod_id>` → Update a product.  
- `DELETE /products/<prod_id>` → Delete a product.  
- `GET /products/like/<user_id>` → Get all products liked by a user.  

**Likes**
- `POST /like/<user_id>/<product_id>` → Toggle like/unlike for a product.  

**Comments**
- `POST /comment` → Create a new comment.  
- `GET /get_comments` → Get all comments.  
- `GET /user_comment/<user_id>` → Get all comments made by a user.  

// TO CHECK
**Cart/Orders (planned)**
- `POST /cart/add` → Add a product to the cart.  
- `POST /cart/remove` → Remove a product from the cart.  
- `POST /cart/submit` → Submit the cart and place an order.  

// TO CHECK
#### Database Structure
- **Users**: id, username, password (hashed)  
- **Products**: id, name, weight, description, photo  
- **Likes**: users_id, products_id  
- **Comments**: id, users_id, products_id, comment  
- **Orders** (planned): id, users_id, list of products, quantities  

---

### 4. Database
- **Description**:  
  PostgreSQL database for persistent storage.  
- **User stories implemented**: Supports all stories requiring persistent data.  
- **Port exposed**: 5432  
- **Persistence**: Yes (volume mounted for data durability).  
- **External connections**: Connected only to the Database API.  

// TO CHECK
- **Database structure**:  
  - Users  
  - Products  
  - Likes  
  - Comments  
  - Orders (planned)  

---


