from flask import Flask
from flask import jsonify
from flask import request
import datetime

app = Flask(__name__)
database = {}


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """Stores a new patient into the system based on user input

    Returns
    -------
    out: str
        Indicate the completion or errors of the action.

    """
    from request_validation import validpatient
    info = request.get_json()
    try:
        validpatient(info, database)
        info["patient_id"] = str(info["patient_id"]).strip()
        info["user_age"] = int(info["user_age"])
        info["attending_email"] = info["attending_email"].strip()
        key = info["patient_id"]
        info["HR_list"] = []
        info["Timestamp"] = []
        database[key] = info
        out = "Submission Accepted"
        return out
    except NameError:
        out = "NameError One or more essential entry missing"
        return out
    except ValueError:
        out = "ValueError One or more entries contain unexpected value"
        return out
    except IndexError:
        out = "IndexError patient already exist in the server"
        return out


@app.route("/api/heart_rate", methods=["POST"])
def new_hr():
    """Stores a new heart rate into specified patient, a related time
    stamp will be added to patient profile as well.

    Returns
    -------
    out: str
        Indicate the completion or errors of the action.
    """
    from request_validation import validhr
    from data_process import tachycardic
    from data_process import send_an_email
    info = request.get_json()
    try:
        validhr(info, database)
        time = datetime.datetime.now()
        key = str(info["patient_id"])
        if type(info["heart_rate"]) == str:
            info["heart_rate"] = info["heart_rate"].strip()
        database[key]["HR_list"].append(int(info["heart_rate"]))
        database[key]["Timestamp"].append(time)
        status = tachycardic(info["heart_rate"], database[key]["user_age"])
        if status == "Positive":
            send_an_email(database[key])
        out = "Submission Accepted"
        return out
    except NameError:
        out = "NameError One or more essential entry missing"
        return out
    except ValueError:
        out = "ValueError One or more entries contain unexpected value"
        return out


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def avg_interval():
    """Returns average heart rate based on user specified interval
    Interval goes from specified time point to the latest time point

    Returns
    -------
    out: json obj
        Contains calculated average heart rate. May instead contain error
        message if user input is invalid.

    """
    from request_validation import validtime
    from request_validation import validid
    from data_process import get_intv_avg
    info = request.get_json()
    try:
        validid(info["patient_id"], database)
        key = str(info["patient_id"])
        try:
            validtime(info, database)
            avg = get_intv_avg(database[key], info["heart_rate_average_since"])
            out = jsonify({"avg_HR": avg,
                           "since": info["heart_rate_average_since"]})
            return out
        except IndexError:
            out = jsonify({
                "Error": "Specified time is larger "
                         "than all timestamps of this patient",
            })
            return out
        except NameError:
            out = jsonify({
                 "NameError": "Invalid time entry"
            })
            return out
        except ValueError:
            out = jsonify({
                "ValueError": "Patient does not have any record"
            })
            return out
    except IndexError:
        out = jsonify({
            "IndexError": "Patient does not exist"
        })
        return out
    except ValueError:
        out = jsonify({
            "ValueError": "Patient does not have any record"
        })
        return out
    except NameError:
        out = jsonify({
            "Error": "Invalid ID input"
        })
        return out


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_stat(patient_id):
    """Return whether patient's heart rate shows tachycardia

    Parameters
    ----------
    patient_id: str or int
        user input indicating the patient to be inspected

    Returns
    -------
    out: json obj
        Contains status of patient. May instead contain error
        message if user input is invalid.

    """
    from request_validation import validid
    from data_process import tachycardic
    try:
        validid(patient_id, database)
        patient_id = str(patient_id)
        state = tachycardic(database[patient_id]["HR_list"][-1],
                            database[patient_id]["user_age"])
        out = jsonify({
            "state": state,
            "Timestamp": database[patient_id]["Timestamp"][-1],
        })
        return out
    except IndexError:
        out = jsonify({
            "Error": "Patient does not exist"
        })
        return out
    except ValueError:
        out = jsonify({
            "Error": "Patient does not have any record"
        })
        return out
    except NameError:
        out = jsonify({
            "Error": "Invalid ID input"
        })
        return out


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_hr(patient_id):
    """Return all stored heart rate of specified patient

    Parameters
    ----------
    patient_id: str or int
        user input indicating the patient to be inspected

    Returns
    -------
    out: json obj
        Contains list of stored heart rate of patient in integer.
        May instead contain error message if user input is invalid.

    """
    from request_validation import validid
    try:
        validid(patient_id, database)
        patient_id = str(patient_id)
        out = jsonify({
            "HR_list": database[str(patient_id)]["HR_list"],
        })
        return out
    except IndexError:
        out = jsonify({
            "Error": "Patient does not exist"
        })
        return out
    except ValueError:
        out = jsonify({
            "Error": "Patient does not have any record"
        })
        return out
    except NameError:
        out = jsonify({
            "Error": "Invalid ID input"
        })
        return out


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_avg_hr(patient_id):
    """Return average heart rate based on all stored heart rate
    of the specified patient

    Parameters
    ----------
    patient_id: str or int
        user input indicating the patient to be inspected

    Returns
    -------
    out: json obj
        Contains calculated average heart rate. May
        instead contain error message if user input is invalid.

    """
    from request_validation import validid
    from data_process import avg_hr
    try:
        validid(patient_id, database)
        patient_id = str(patient_id)
        result = avg_hr(database[patient_id]["HR_list"])
        out = jsonify({
            "avg_HR": result,
        })
        return out
    except IndexError:
        out = jsonify({
            "Error": "Patient does not exist"
        })
        return out
    except ValueError:
        out = jsonify({
            "Error": "Patient does not have any record"
        })
        return out
    except NameError:
        out = jsonify({
            "Error": "Invalid ID input"
        })
        return out


if __name__ == "__main__":
    app.run(host="127.0.0.1")
