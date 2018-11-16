import numpy


def validtype(data):
    if type(data) == str or type(data) == int:
        return True
    else:
        return False


def validpatient(info, database):
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
                    return 1
                else:
                    raise IndexError("patient already exist in the server")
        raise ValueError("One or more entries"
                         " contain unexpected value")
    else:
        raise NameError("One or more essential entries missing")


def validhr(info, database):
    if ("patient_id" in info and
            "heart_rate" in info):
        if validtype(info["patient_id"]) and validtype(info["heart_rate"]):
            if (str(info["patient_id"]).strip().isdigit() and
                    str(info["heart_rate"]).strip().isdigit()):
                return 1
        raise ValueError("One or more entries"
                         " contain unexpected value")
    else:
        raise NameError("One or more essential entries missing")


def validtime(info, database):
    import datetime
    key = str(info["patient_id"])
    if ("heart_rate_average_since" not in info or
            type(info["heart_rate_average_since"]) != str):
        raise NameError
    datetime.datetime.strptime(info["heart_rate_average_since"],
                               "%Y-%m-%d %H:%M:%S.%f")
    if len(database[key]["HR_list"]) == 0:
        raise ValueError
    return 1


def validid(id, database):
    if not (validtype(id) and str(id).isdigit()):
        raise NameError("Invalid ID input")
    if str(id) not in database:
        raise IndexError("Patient ID does not exist")
    if len(database[str(id)]["HR_list"]) < 1:
        raise ValueError("Patient has no heart rate record")
    return 1
