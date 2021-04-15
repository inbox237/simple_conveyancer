# Simple Conveyancer

## Description

Simple Conveyancer is designed to assist with the property conveyancing process by allowing a user to enter details of an upcoming property sale and have the application calculate the required settlement adjustments for Brisbane City Council property rates.

A user can sign up using a username and password and after logging in, may create new settlements by entering the details into a form. Upon clicking each individual settlement, the calculations of the settlement figures will be completed automatically.

The application is made using Flask, Python, Html and PostgreSQL. 

The GitHub repository for this can be found here: https://github.com/inbox237/Simple_Conveyancer

This application will be hosted live at http://3.106.129.206:5000/ , but in the event that this isn't the case, please follow the instructions below:

![erd](/docs/New_Settlement.png)

## Instructions

The instructions for Ubuntu 20:

Update repositories on Ubuntu: ```sudo apt-get update```

Clone GitHub repository: ```git clone https://github.com/inbox237/Simple_Conveyancer ```

CD: ```cd Simple_Conveyancer```

Install python virtual environment: ```sudo apt-get install python3-venv```

Create virtual environment: ```python3 -m venv venv```

Activate the virtual environment ```source venv/bin/activate```

Install pip: ```python -m pip install --upgrade pip```

Install modules from requirements.txt: ```pip install -r requirements.txt```

To connect to the database locally, please fill in the "exampleenv" file like this example, then rename the file to ".env":
DB_URI="postgresql+psycopg2://postgres:coder@13.211.86.126/simple_conveyancer"
DB_URI_TESTING="postgresql+psycopg2://postgres:coder@13.211.86.126/simple_conveyancer_testing"
FLASK_APP=main.py
FLASK_ENV=development
JWT_SECRET_KEY = "duck"
AWS_ACCESS_KEY_ID=1
AWS_SECRET_ACCESS_KEY=1
AWS_S3_BUCKET=1


**To create the database and seed all values with one command, run ONLY the following command:**
Note: This will complete all steps required to run the program including starting flask and opening a local browser.

```flask db-custom start``` (to complete all steps in order)

**Alternatively the following commands can be run separately:**

```flask db-custom drop``` (If there are any tables in the database previously)

```flask db upgrade``` (to add the tables in the migrations directory)

```flask db-custom seed``` (to seed the database)


Note: seeding includes populating these tables:
1. 4 users in Users, 
2. 4 settlements in Settlements





**ReadMe from Part A:**
**CCC – Assessment – T4A2 – Conveyancing - Simple Conveyancer (BCC Rates Calculator)
### R1 - Description of your website, including:
##### Purpose
##### Functionality / features
##### Target audience
##### Tech stack

The purpose of this application is to create a basic web portal through which a law or conveyancing firm may use their firm username to log in, then be able to use the application to enter their clients’ details regarding an upcoming property sale within the Brisbane City Council area in order to automatically calculate the rates either owing by or owed to the client (sale-side) at time of settlement.

The details provided by the user will produce a web-based table of figures similar to an earlier python terminal version of this application:

![](docs/terminal.jpg)

In terms of functionality, the application will allow the firm to firstly create a username for which they may then log in to the portal, after which they will be taken to an input page. At this input page the user will then enter details (excluding client number):

- Client Number (Auto Generated)
- Client Name
- Property Address
- Sale Price
- Deposit Paid
- Settlement Date
- Rates Paid/Payable
- Rates Paid Status

The user will then be shown a web-based table showing the results. The results will be saved into the PostgreSQL database, linked to the firm username. In addition to the results and input pages there will also be a historical record in the database of all previous results the firm has input in the past. The firm may also delete records of previous results.

The target audience for this application is law firms, conveyancing firms, or other indivuiduals interested in the conveyancing process.

The application will utilise a PostgreSQL database in conjunction with AWS, Python and Flask with a Jinja template incorporating HTML/CSS. AWS EC2s will be utilised and deployed using AWS ECR Docker deployment.


https://inbox237.000webhostapp.com/


### R2 - Dataflow Diagram:
![](docs/dfd.png)

### R3 - Application Architecture Diagram:
![](docs/ad.png)

### R4 - User Stories:
"As a user, I want to be able to have a reliable portal for which I can log into remotely from any location and calculate the amount of Brisbane City Council Rates due or owed at time of Settlement for my own or my client's upcoming property Settlement."

#### Persona 1:
- Fictional Name: David Justice
- Photo: Stock Photo
- Job Title: Conveyancing & Property Lawyer
- Demographics:
-- 50 years old
-- Married
-- Father of two children
-- Has an LLB
- Goals and tasks:
-- David is very efficiency and precision orientated, he has no time for applications or business processes that slow down the conveyancing process or produce errors for his clients. He wants a reliable portal that can be used quickly to calculate the conveyancing settlement figures and have them stored historically.
-- He spends his time completing numerous property sale and purchase conveyancing transactions for his clients.
- Environment: David is comfortable using technology generally but needs needs his software to be clear, simple and precise.

#### Persona 2:
- Fictional Name: Gladys Numbers
- Photo: Stock Photo
- Job Title: Retiree, property investor
- Demographics:
-- 72 years old
-- Married
-- Mother of four children

- Goals and tasks:
-- Gladys is very profit focused and has successfully sold a number of investment properties over the last two decades. She does not always do the conveyancing process herself but does wish to understand the calculations of figures for her own knowledge and to ensure she is not being shortchanged.
-- She wants a reliable portal that can be used quickly to calculate the conveyancing settlement figures and have them stored historically.
-- She spends her time mostly retired but does spend evenings review documents for her investment properties.
- Environment: Gladys is not overly proficient in IT software but does have good background knowledge in accounting and is comfortable doing much of the conveyancing process herself.




### R5 - Wireframes:
![](docs/Login_signup.png)

![](docs/New_Settlement.png)

![](docs/Home.png)

![](docs/Settings.png)

![](docs/Login_signup_Mobile.png)

![](docs/New_Settlement_Mobile.png)

![](docs/Home_Mobile.png)

![](docs/Settings_Mobile.png)

### R6 - Trello Board:
![](docs/T4A2_trello_1.jpg)

![](docs/T4A2_trello_2.jpg)

![](docs/T4A2_trello_3.jpg)

![](docs/T4A2_trello_4.jpg)
