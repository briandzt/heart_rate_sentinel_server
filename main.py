from flask import Flask
from flask import jsonify
from flask import request
import datetime

app = Flask(__name__)
database = {}


@app.route("/api/new_patient", methods=["POST"])
def new_patient():
    """
    Function that stores a new patient into the system based on user input

    Returns
    -------
    flag: int
        Integer that indicates whether a new patient is added
        1 means added, 0 means not added
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
        return "Submission Accepted"
    except NameError:
        return jsonify({"NameError":
                        "One or more essential entry missing"})
    except ValueError:
        return jsonify({"ValueError":
                        "One or more entries"
                        " contain unexpected value"})
    except IndexError:
        return jsonify({"IndexError":
                        "patient already exist in the server"})


@app.route("/api/heart_rate", methods=["POST"])
def new_hr():
    """

    Returns
    -------

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
        return "Submission Accepted"
    except NameError:
        return jsonify({"NameError":
                        "One or more essential entry missing"})
    except ValueError:
        return jsonify({"ValueError":
                        "One or more entries"
                        " contain unexpected value"})


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def avg_interval():
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
            return jsonify({"avg_HR": avg,
                            "since": info["heart_rate_average_since"]})
        except IndexError:
            return jsonify({
                "Error": "Specified time is larger "
                         "than all timestamps of this patient",
            })
        except NameError:
            return jsonify({
                 "NameError": "Invalid time entry"
            })
        except ValueError:
            return jsonify({
                "ValueError": "Patient does not have any record"
            })
    except IndexError:
        return jsonify({
            "IndexError": "Patient does not exist"
        })
    except ValueError:
        return jsonify({
            "ValueError": "Patient does not have any record"
        })
    except NameError:
        return jsonify({
            "Error": "Invalid ID input"
        })


@app.route("/api/status/<patient_id>", methods=["GET"])
def get_stat(patient_id):
    """

    Parameters
    ----------
    patient_id

    Returns
    -------

    """
    from request_validation import validid
    from data_process import tachycardic
    try:
        validid(patient_id, database)
        patient_id = str(patient_id)
        state = tachycardic(database[patient_id]["HR_list"][-1],
                            database[patient_id]["user_age"])
        return jsonify({
            "state": state,
            "Timestamp": database[patient_id]["Timestamp"][-1],
        })
    except IndexError:
        return jsonify({
            "Error": "Patient does not exist"
        })
    except ValueError:
        return jsonify({
            "Error": "Patient does not have any record"
        })
    except NameError:
        return jsonify({
            "Error": "Invalid ID input"
        })


@app.route("/api/heart_rate/<patient_id>", methods=["GET"])
def get_hr(patient_id):
    from request_validation import validid
    try:
        validid(patient_id, database)
        patient_id = str(patient_id)
        return jsonify({
            "HR_list": database[str(patient_id)]["HR_list"],
        })
    except IndexError:
        return jsonify({
            "Error": "Patient does not exist"
        })
    except ValueError:
        return jsonify({
            "Error": "Patient does not have any record"
        })
    except NameError:
        return jsonify({
            "Error": "Invalid ID input"
        })


@app.route("/api/heart_rate/average/<patient_id>", methods=["GET"])
def get_avg_hr(patient_id):
    from request_validation import validid
    from data_process import avg_hr
    try:
        validid(patient_id, database)
        patient_id = str(patient_id)
        result = avg_hr(database[patient_id]["HR_list"])
        return jsonify({
            "avg_HR": result,
        })
    except IndexError:
        return jsonify({
            "Error": "Patient does not exist"
        })
    except ValueError:
        return jsonify({
            "Error": "Patient does not have any record"
        })
    except NameError:
        return jsonify({
            "Error": "Invalid ID input"
        })


if __name__ == "__main__":
    app.run(host="127.0.0.1")
