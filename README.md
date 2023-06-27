# Record Control
This project is a system of records where the client can make an
appointment with the employee and vice versa. This kind of
platform can be useful for services, who will benefit from
appointment creation and client interaction online. Employees and
clients can be notified respectively when appointments are created,
edited or deleted. Also every employee has their own schedule/calendar.


##### Table of Contents
- [Installation](#installation)<br />
- [Usage](#usage)<br />
- [Used Technologies](#used-technologies)<br />
- [Third Party Packages](#third-party-packages)<br /> 
- [Contacts](#contacts)


## Installation
To install and run Record Control, follow these steps:
1. Clone the repository:
   ```
   git clone https://github.com/alex23090/record_control.git
   ```
2. Navigate to the project directory:
   ```
   cd record_control
   ```
3. Create a virtual environment:
   ```
   python3 -m venv env
   ```
4. Activate the virtual environment:
   * For Windows:
     ```
     .\env\Scripts\activate
     ```
   * For macOS/Linux:
     ```
     source env/bin/activate
     ```
5. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Perform database migrations:
   ```
   python manage.py migrate
   ```
7. Run tests:
   ```
   python manage.py test
   ```
8. Start the development server:
   ```
   python manage.py runserver
   ```
9. Open your web browser and navigate to http://localhost:8000 to access the application.


## Usage


https://github.com/alex23090/record_control/assets/71777924/bec32b99-7fb9-4ad4-a1a1-360c95eaa365


On this video I'm demonstrating step by step functionality of the project. Firstly we see the "Home" page with bunch of specialists, we can use the search, pagination etc. I'm moving on "Login/Sign up" page to create new account, we have opportunity to make client/worker account. I'm creating the first one filling up the whole form, if your email exist, you gonna get a message after creating an account. Than I just moving on my account page to edit my account, to add profile photo, I have successfully added it and got the success message above. Moving on "Home" page again, using search to find necessary specialist, moving on his profile, than hitting link "Appointment schedule",  where we have like an infinite calendar where can pick a day to schedule an appointment. I choose a day, filled out the form. Than I signed out, in order to demonstrate how is it gonna look like from worker perspective I'm logging in worker account with which I just created an appointment. Moving on "Inbox" page, worker got some notifications and of course the one about appointment we just created. After reading I just deleted notification. Moving to "All Events" page, seeing our appointment is here, moving on "Events to approve" page, searching for our appointment by the name of the client and approving it. Also we can update already created appointment and the other party will definitely receive a notification of any changes. Moving on API page  where we have API documentation for this particular project and a bunch of available endpoints.


## Used Technologies
  * Django
  * Django-Rest-Framework
  * Postgresql
  * Docker
  * HTML
  * CSS
  * BOOTSTRAP 5
  * JavaScript

## Third Party Packages
  * django-allauth
  * django-crispy-forms
  * python-dotenv
  * requests
  * pillow
  * whitenoise


## Contacts
If you have any questions, suggestions, or feedback, please feel free to contact me:
* Email: alex2003199604@gmail.com
* Telegram: t.me/here_was_dymytrov
