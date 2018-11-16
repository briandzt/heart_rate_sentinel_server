# heart_rate_sentinel_server
A server to receive data from mock patient heart rate monitors and send warning emails to physician if tachycardic heart rate is observed.

The function of the program mainly depends on three files:
* main.py contains all functions that will be called as a server
* data_process.py contains all functions used for calculation 
* request_validation.py contains all functions used to check whether
the user input is valid
** data_process.py and request_validation.py each has a test file for unit
testing on all functions in the two files.
 
The server is initiated by running main.py. The functions in the rest two files will be calld
when being used.

* Functions within main.py functions as described in the requirements
* For functions in data_process:
    **tachycardic* takes in the heart rate and age to determine where the patient
    has tachycardia
    **avg_hr* takes in all heart rate of a patient and returns their average
    **get_intv_avg* first convert user input to datetime object, and then compare
    it with all stored datetime object. For those with time points larger than the 
    user defined time points, their corresponding heart rates are added together to
    calculate average heart rate in specified time interval
    **Send_an_email* takes in patients information and send out warning to their
    attending email.

Additional features:
* The program is designed to be able to tolerate input numbers
to be in both string or int format. It is also able to tolerate accidental spaces
if the input is in string.

