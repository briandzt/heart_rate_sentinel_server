from sendgrid.helpers.mail import *


def tachycardic(hr, age):
    """

    Parameters
    ----------
    hr
    age

    Returns
    -------

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
    """

    Parameters
    ----------
    hr

    Returns
    -------

    """
    import numpy as np
    avg = round(np.mean(hr), 2)
    return avg


def get_intv_avg(database, time):
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
