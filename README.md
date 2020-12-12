# Setup 

1. Clone the repository. 
2. _cd_ into _Stripe_Subscription/_
3. Make sure you have Python 3.9. I recommend using _pyenv_. More info on installing pyenv can be found here: https://realpython.com/intro-to-pyenv/#installing-pyenv
   
   a) Get Python 3.9 for pyenv - > ***pyenv install -v 3.9.0***
   
   b) Create a new virtual environment - ***pyenv virtualenv 3.9.0 test_environment***
   
   c) Activate virtual environment - ***pyenv local test_environment***  (you will see (test_environment) on the beginning of each line on your terminal)
   
4. Install pipenv using ***pip install pipenv***.
5. Install dependencies using ***pipenv install***.
6. Create an empty file in _Stripe_Subscriptions/_ (should be the directory you are in currently) called .env and insert the following lines in the file and save:
   ```
   SECRET_KEY=(stripe_secret_key refer to email)
   ACCESS_KEY=(can be any string eg: test_access_key)
    ```
7. Migrate by using the command ***python manage.py migrate --settings=settings_local***.
8. Run the server using ***python manage.py runserver --settings=settings_local***.
9. Navigate to http://localhost:8000/stripe_api/ on your browser. You can see the browsable API views here for payment method, customer and subscription. You can navigate to the links for each and add a payment method, customer or subscription from here. 

Example payload for payment method:

    Card type -> card (string)
    Card number -> 4242424242424242 (test card for stripe)
    Card exp month year -> 10/10/2023 (pick a year that is > 2020)
    Card cvc -> 234 
    Key -> (ACCESS_KEY from your .env file)

Example payload for customer: 

    Username -> test_user 
    Payment method -> (Choose from a list of existing payment methods)
    Key -> (ACCESS_KEY from your .env file)

Example payload for subscription:

    Customer -> (Choose from a list of existing customers)
    Key -> (ACCESS_KEY from your .env file)

# API documentation 
### Create a payment method 

***POST /stripe_api/paymentmethod/***

Parameters:

    card_type (str): input "card" here
    card_number (int): payment card number
    card_exp_month_year (str): payment card expiry month and year in the format mm/yyyy
    card_cvc (int): payment card cvc number
    key (str): access key 

Sample response:

    Success!


### Create a customer 

***POST /stripe_api/customer/***

Parameters:

    username (str): Customer's name
    payment_method (int): id of a previously added payment method
    key (str): access key 

Sample response:

    Success!

### Create a subscription

***POST /stripe_api/subscription/***

Parameters:

    customer (int): id of a previously added customer 
    key (str): access key

Sample response:

    Success!
