from sendgrid.helpers.mail import *


def tachycardic(hr, age):
    """Determine whether patient's heart shows tachycardia

    Parameters
    ----------
    hr: str or int
        heart rate of the patient

    age: int
        age of the patient

    Returns
    -------
    out: str
        "Negative" if heart rate does not show tachycardia
        "Positive" if heart rate shows tachycardia

    """
    out = "Negative"
    age = int(age)
    if age == 1 or age == 2:
        thresh = 151
    elif age == 3 or age == 4:
        thresh = 137
    elif age >= 5 and age <= 7:
        thresh = 133
    elif age >= 8 and age <= 11:
        thresh = 130
    elif age >= 12 and age <= 15:
        thresh = 119
    elif age > 15:
        thresh = 100
    if int(hr) > thresh:
        out = "Positive"
        return out
    else:
        return out


def avg_hr(hr):
    """Calculate average heart rate based on all recorded
    heart rate

    Parameters
    ----------
    hr: list
        list of integer containing all recorded heart rate

    Returns
    -------
    avg: float
        2-decimal-place float indicating average heart rate

    """
    import numpy as np
    avg = round(np.mean(hr), 2)
    return avg


def get_intv_avg(database, time):
    """Determine average heart rate in the interval of specified
    time point to the last recorded heart rate.

    Parameters
    ----------
    database: dict
        Dictionary containing all patients related data. Each entry is
        a dictionary containing all information of a single patient.

    time: str
        String with the standard format of a printed datetime object
        in the form of "year-month-day hour:minute:second.microsecond"

    Returns
    -------
    avg: float
        2-decimal-place float indicating average heart rate

    """
    import numpy as np
    import datetime
    reftime = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
    hr = []
    index = 0
    for i in database["Timestamp"]:
        if i >= reftime:
            hr.append(database["HR_list"][index])
        index += 1
    if len(hr) == 0:
        raise IndexError
    avg = round(np.mean(hr), 2)
    return avg


def send_an_email(info):
    """Send warning email to specified email address

    Parameters
    ----------
    info: dict
        dictionary containing infomation of a single patient

    Returns
    -------
    result: str
        String indicating that email is sent

    """
    import sendgrid
    import os
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("zd32@duke.edu")
    to_email = Email(info["attending_email"])
    subject = "Tachycardic symptom detected in patient {0}!".format(
        info["patient_id"])
    content = Content("text/plain", "An abnormal heart rate: {0} bpm,"
                                    " is observed from patient {1} at"
                                    " time {2}, which conforms with "
                                    "the symptom of tachycardia".format(
                                        info["HR_list"][-1],
                                        info["patient_id"],
                                        info["Timestamp"][-1]
                                    ))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    result = "Email sent"
    return result
