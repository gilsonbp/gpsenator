  
# GP Senator  
  
Import the register of Senators currently in practice in Brazil and make the data available in an organized way for consultation.

## Installation 
The system is already configured to use a **SqLite** database. You can add or modify `settings.py` features by creating a `local_settings.py` in the same directory. 

After configure run the `python manange.py migrate` command to create the database.
  
Use the ` python manage.py cretesuperuser` command to create an administrator user.

## Update of Parliamentarians
After accessing the system for the first time, navigate to `Home > Senator > Parliamentarians` and click the button 'Update Parliamentarians' as shown below.

![enter image description here](https://raw.githubusercontent.com/gilsonbp/gpsenator/dev/static/screens/update_parliamentarians.png)