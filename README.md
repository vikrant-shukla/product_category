# Product and Categories

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)


## About <a name = "about"></a>

Assignment:  Project is built over Django Rest Framework and used Sqlite3 as a database. In the project there are lots of point that need to be covered which are mentioned below:
1. Category can be subcategory of other category & possibly N number of depth.
2. API's to create product(name, price) & assign multiple categories to it.
3. Hundred users will be created in system using django managememnt command.
4. API which will dump an excel file which containes data - id, name (first name , lastname ) and is_active  of hundres user created.
5. Excel file sent using celery on the provided email in the body.
6. API which Lists all the products available in the system.
7. API which schedule a task which sends email after 2 mins of api call.


## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing. See 

### Functionalities
Project having numbers of functionalities which are stated below:

1. Created table to hold the categories and its subcategories. In this we can store various categories because i used recursive model and we can perform crud oprations on it.
2. Created table to hold the product name and price and can assign multiple category to it and we can perform crud oprations on it.
3. Created 100 Users in User Table of django using management command.
4. Dumping the data includes Id, Name (Consist of first_name and last_name) and is_active status to excel file.
5. Fetching the file from local directory and attaching the file on mail body and sending the email on background to sigle user email or list of emails of users getting from frontend (postman).
6. Fetching the list of products created in product table and sending the data in response and again if data requested, data will come from cache memory.
7. Implemented update cache scenario i.e. when the data is updated,newly created or deleted then the cache is updated automatically and send the response from cache to frontend(Postman).
8. Create one functionality that when the api call the mail will be send to user or a list of user's emails from body after 2 minutes of api call with the excel file dumped earlier. 


### Prerequisites

What things do you need to install the software and how to install them?

```
Python
Pandas
Django Rest Framework
Celery
Redis
```

### Installing

A step-by-step series of examples that tell you how to get a development environment running.

Install the requirements.txt file for dependencies. run the below command: 
```
create virtual env : virtualenv venv

activate the env : 
For macOS and Linux: source venv/bin/activate
For Windows:  venv/Scripts/activate

pip3 install -r requirements.txt
```
## Further Steps

Start the django,celery and redis server by running the below command in different terminal (ensure the env is activated and dependencies were installed).

```
python3 manage.py runserver
celery -A categories_product.celery worker -l info
redis-server
```
Created API's for all functionalities mentioned above and are as follows:

Base_url = 'http://127.0.0.1:8000'

1. To Create and Read the Categories and Sub-Categories.

```
GET, POST : Base_url/categories
Body:
    GET: No Body
    POST:
        super category:
              {
                "name":"super_category_name"
                }
        category:
              {
                "name":"category_name",
                "parent_category": 1 # id of super category
                }
        sub category:
              {
                "name":"sub_category_name",
                "parent_category": 1 # id of category
                }
        and so on...
```

2. TO Update and Delete the Categories and Sub-Categories.

```
PATCH, PUT, DELETE : Base_url/categories/pk #pk for the record which need to be modified
Body:
    PATCH :  which partial column needs to be modified
          {
            "name":"category",
            "parent_category": 1 # id of parent category if needs to be modified
          }
    PUT: all columns to be modified
          {
            "name":"category",  
            "parent_category": 1 # id of parent category if needs to be modified
          }
    DELETE:
          No Body

```

3. To Create and Read the Products.

```
GET, POST : Base_url/products
Body:
    GET: {
      "cache":"disable" # if you want to check the data from database itself.
    }
    POST: 
        {
        "name":"Product_name",
        "price":Product_price,
        "category": [category_id]  # list of categories which is to be assigned
          }
```

4. TO Update and Delete the Products.

```
PATCH, PUT, DELETE : Base_url/products/pk
Body: 
    PATCH: Which partial column needs to be modified
        {
          "name":"Product_name",
          "price":Product_price,
          "category": [category_id]  # list of categories which is to be assigned
          }
    PUT: When all columns to be modified
        {
          "name":"Product_name",
          "price":Product_price,
          "category": [category_id]  # list of categories which is to be assigned
          }
    DELETE: No Body
```

5. For Dumping the excel file in directory.
```
GET Base_url/excel
Body : No Body
```
6. To mail the excel to users or list of users.
```
GET Base_url/mail
Body:
    GET: 
      {
        "email":["xyz@gmail.com", "abc@gmail.com"] # Provide the lists of working emails 
       }

```
7. To mail the excel to users or list of users after 2 mins of api call.
```
GET Base_url/mail_after
Body:
    GET: 
      {
        "email":["xyz@gmail.com", "abc@gmail.com"] # Provide the lists of working emails 
       }
```