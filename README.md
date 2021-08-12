# ZTP-technical-test

Technical test for ZTP full stack Junior Developer role.

## Setup

This technical test is created on Python 3.9.6 and django with CSS and HTML.

-  This test was performed in a virtual environment with specific user customisations and preferences, so please be aware of any differences which can occur in your environment.

-  To install all required libraries, enter `pip3 installs -r requirements.txt` and all necessary libraries will be installs.

## Design

The design was specificed for one table for the customer details and consumption details (derived as their meter readings from the terminology used in the technical brief) and another for the calculated results when a form button is clicked.

The button was added as part of a form element as the technical brief requested a Django form be used to create the table. This was chosen as a suitable completion of this criteria because:

-  No information is required to be sent to the back end, only calculations formed from data already present, adding a true Django form does not seem to make sense for the unusual wording given.
-  The form method attribute allows for the logic to be encapsulated in the same view method where the information is already present.
-  The use of javascript for the activation of the button, possible use of AJAX for information and showing of the secondary table seemed unneccesary to achieve the goal.

## Technologies

Javascript was not during this test as it was not necessary to achieve the goal and its requirement was not expressing demanded. Post request seems to reduce the amount of repetition and complexity required for the same result and interactivity was not highlighted as important.

## Bugs/Decisions

-  There is a possible issue with Customer 3 sheet cell A6 where the rate name does not match any existing rates offered in the relevant excel sheet. This meant it was impossible to calculate or display the readings correctly on the table.
-  Since it was not known if this was purposeful or an error, I assumed in the situation that changing the backend data was not ideal and created my scope to account for correctly given information. If this was error I assume the data displayed and calculations may have changed.
-  I selected to use a class builder for customer to allow easy dot notation when selecting information in the HTML and allow for expansion on the number of customers with minimal code change.
-  Equally, the HTML uses a list of rate names to allow for a responsive table depending on whether there are more of less rates available (assuming that the rates in the "Rate Price" sheet are the correct options).
-  The project was left in DEBUG mode as this is not a production app and is purely for technical reasons.

## Other

-  All three of the highest values seem to belong to Joe, while I have re-calculated and checked the values using the excel spreadsheet itself, I am welcome to any corrections in logic which may have this to occur by error.
-  The use of dictionaries for the users rate details was to allow for key values to be compared easily and then accessed, this does make a slightly daunting layer of statements in the front end. I would be curious to know whether a better data storage or set of conditions would achieve the same result easier.
-  The end of the post request uses variables to check for highest scores and assess which information should override the original values. I chose this option as the sorting functions often edited the original code and thought lambda arguments would be more complicated for such basic use data, I do now know whether this could have been an easier alternative in the end.
-  No javascript has been used in this project as I felt the results were the same to the user using HTMl post methods to the back end and rendering the updated sheet. The specification does not state that a table could be hidden again on a button click, where Javascript would of been much better.
   -  I would have been interested in using an AJAX request to assess and retrieve the information had I not used a form to send the results.

*  If this was a larger scaled project, the use of models to create and store the data would have been a smart move. I did not use this though as my assumption was the excel sheet functioned as the database, therefore not requiring proper use of SQLite3 or models to hold and read this information.
