Technology City
Electronics store
Powering Your Passion for Electronics


Team <br> 
Mahmoud Elbehery <br> 
Safeya Yasien <br> 




*Architecture


User Interface (UI)
Interface for users to interact with the application. <br> 
Includes web pages for browsing products and viewing details <br> 

Frontend <br> 
Client-side logic  for handling user interactions.
Utilizes HTML, CSS, and JavaScript frameworks like React.js. <br> 
Server <br> 
Backend for processing client requests.<br> 
Implemented using Python and Flask framework.<br> 
Backend API<br> 
Handles requests related to user authentication, product data retrieval, and order processing.<br> 
Implemented using Python and Flask framework.<br> 
Database<br> 
Stores persistent data such as product info, name, description, price, img
Utilizes a relational database management system (RDBMS) like MySQL with SQLAlchemy ORM.<br> 



*APIs and Methods<br> 

For the web client to communicate with the web server:<br> 
/api/products
Returns a list of available products in the store.<br> 
List and describe any API endpoints or function/methods that you will be creating to allow any other clients to use<br> 
class: product<br> 
function: getPorduct(productId)<br> 
description: Retrieves details of a specific product identified by its ID.<br> 
product_id: The unique identifier of the product.<br> 
Returns: Details of the product including its name, description ,price, reviews.<br> 
