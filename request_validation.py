import numpy


def validtype(data):
    """Verify whether input has str or int type

    Parameters
    ----------
    data: free term
        variable whose type is to be determined

    Returns
    -------
    out: bool
        Indicate whether input has int or str type

    """
    if type(data) == str or type(data) == int:
        out = True
        return out
    else:
        out = False
        return out


def validpatient(info, database):
    """Verify whether input to add new patient is valid

    Parameters
    ----------
    info: dict
        Contains information of the new patient to be added

    database: dict
        Patient database. Contains dictionary of each patients

    Returns
    -------
    out: int
        indicating the verification process is done, and no errors
        are raised.

    """
    if ("patient_id" in info and
            "attending_email" in info and
            "user_age" in info):
        if (validtype(info["patient_id"]) and
                validtype(info["attending_email"]) and
                validtype(info["user_age"])):
            if (str(info["patient_id"]).strip().isdigit() and
                    type(info["attending_email"]) == str and
                    str(info["user_age"]).strip().isdigit()):
                if str(info["patient_id"]) not in database:
                    out = 1
                    return out
                else:
                    raise IndexError("patient already exist in the server")
            else:
                raise ValueError("One or more entries"
                                 " contain unexpected value")
        else:
            raise ValueError("One or more entries"
                             " contain unexpected value")
    else:
        raise NameError("One or more essential entries missing")


def validhr(info, database):
    """Verify whether input for new heart rate record is valid

    Parameters
    ----------
    info: dict
        Contains information of the new heart rate to be added

    database: dict
        Patient database. Contains dictionary of each patients

    Returns
    -------
    out: int
        indicating the verification process is done, and no errors
        are raised.

    """
    if ("patient_id" in info and
            "heart_rate" in info):
        if validtype(info["patient_id"]) and validtype(info["heart_rate"]):
            if (str(info["patient_id"]).strip().isdigit() and
                    str(info["heart_rate"]).strip().isdigit()):
                return 1
            else:
                raise ValueError("One or more entries"
                                 " contain unexpected value")
        else:
            raise ValueError("One or more entries"
                         " contain unexpected value")
    else:
        raise NameError("One or more essential entries missing")


def validtime(info, database):
    """Verify whether specified time point for interval average
    is valid

    Parameters
    ----------
    info: dict
        Contains information of the new patient to be added

    database: dict
        Patient database. Contains dictionary of each patients

    Returns
    -------
    out: int
        indicating the verification process is done, and no errors
        are raised.

    """
    import datetime
    key = str(info["patient_id"])
    if ("heart_rate_average_since" not in info or
            type(info["heart_rate_average_since"]) != str):
        raise NameError
    datetime.datetime.strptime(info["heart_rate_average_since"],
                               "%Y-%m-%d %H:%M:%S.%f")
    if len(database[key]["HR_list"]) == 0:
        raise ValueError
    out = 1
    return out


def validid(id, database):
    """Verify whether input patient id is valid for get requests

    Parameters
    ----------
    id: free term
        User input patient_id whose type is to be determined

    database: dict
        Patient database. Contains dictionary of each patients

    Returns
    -------
    out: int
        indicating the verification process is done, and no errors
        are raised.

    """
    if not (validtype(id) and str(id).isdigit()):
        raise NameError("Invalid ID input")
    if str(id) not in database:
        raise IndexError("Patient ID does not exist")
    if len(database[str(id)]["HR_list"]) < 1:
        raise ValueError("Patient has no heart rate record")
    out = 1
    return out
