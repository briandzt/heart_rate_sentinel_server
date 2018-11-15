import numpy


def validpatient(info):
    if ("patient_id" in info and
            "attending_email" in info and
            "user_age" in info):
        if (str(info["patient_id"]).strip().isdigit() and
                type(info["attending_email"]) == str and
                str(info["user_age"]).strip().isdigit()):
            return 1
        else:
            raise ValueError("One or more entries"
                             " contain unexpected value")
    else:
        raise NameError("One or more essential entries missing")


def validhr(info, database):
    if ("patient_id" in info and
            "heart_rate" in info):
        if (str(info["patient_id"]).strip().isdigit() and
                str(info["heart_rate"]).strip().isdigit()):
            return 1
        else:
            raise ValueError("One or more entries"
                             " contain unexpected value")
    else:
        raise NameError("One or more essential entries missing")


def validtime(info, database):
    key = str(info["patient_id"])
    if ("heart_rate_average_since" not in info or
            type(info["heart_rate_average_since"]) != str):
        raise KeyError
    if len(database[key]["HR_list"]) == 0:
        raise ValueError
    return 1


def validid(id, database):
    if id not in database:
        raise IndexError("Patient ID does not exist")
    if len(database[id]["HR_list"]) < 1:
        raise ValueError("Patient has no heart rate record")
    return 1
