import pytest


@pytest.fixture
def data():
    import datetime
    database = {"1": {"patient_id": "1",
                "Timestamp": [datetime.datetime(2018, 3, 9, 11, 0, 36, 372339),
                              datetime.datetime(2018, 3, 9, 11, 0, 36, 372340),
                              datetime.datetime(2018, 3, 9, 11, 0, 37, 372339)
                              ],
                      "HR_list": [50, 60, 70]},
                "5": {"patient_id": "5",
                      "Timestamp": [],
                      "HR_list": []}}
    return database


@pytest.mark.parametrize('new_patient', [({"patient_id": 2,
                                          "attending_email": "zd32@duke.edu",
                                           "user_age": 50}), (
                                          {"patient_id": " 2",
                                           "attending_email": "zd32@duke.edu",
                                           "user_age": 50}), (
                                          {"patient_id": 2,
                                           "attending_email": "zd32@duke.edu",
                                           "user_age":  ' 50'}
                                          )])
@pytest.mark.parametrize("index", [({"patient_id": 1,
                                   "attending_email": "zd32@duke.edu",
                                    "user_age": 50
                                     }), ({"patient_id": "1",
                                           "attending_email": "zd32@duke.edu",
                                           "user_age": 50})])
@pytest.mark.parametrize("value", [({"patient_id": 2.5,
                                    "attending_email": "zd32@duke.edu",
                                     "user_age": 50}), (
                                   {"patient_id": 1,
                                    "attending_email": 25,
                                    "user_age": 50}), (
                                   {"patient_id": 1,
                                    "attending_email": "zd32@duke.edu",
                                    "user_age": []}), (
                                   {"patient_id": 'asdf',
                                    "attending_email": "zd32@duke.edu",
                                    "user_age": 50})
                                   ])
@pytest.mark.parametrize("name", [({"patient_id": 1,
                                    "attending_email": "zd32@duke.edu"}), (
                                  {"attending_email": "zd32@duke.edu",
                                   "user_age": 50}),
                                  ({"patient_id": 1,
                                    "user_age": 50})])
def test_validpatient(new_patient, data, index, value, name):
    from request_validation import validpatient
    result = validpatient(new_patient, data)
    assert result == 1
    with pytest.raises(IndexError):
        validpatient(index, data)
    with pytest.raises(ValueError):
        validpatient(value, data)
    with pytest.raises(NameError):
        validpatient(name, data)


@pytest.mark.parametrize("heartrate", [({"patient_id": 1,
                                         "heart_rate": 50}), (
                                   {"patient_id": "1 ",
                                    "heart_rate": 50}), (
                                   {"patient_id": '1',
                                    "heart_rate": '50'})])
@pytest.mark.parametrize("value", [({"patient_id": 2.5,
                                     "heart_rate": 50}), (
                                   {"patient_id": 1,
                                    "heart_rate": []}), (
                                   {"patient_id": 'asdf',
                                    "heart_rate": 50})])
@pytest.mark.parametrize("name", [({"patient_id": 1}), (
                                  {"heart_rate": 50})])
def test_validhr(heartrate, value, name):
    from request_validation import validhr
    result = validhr(heartrate, data)
    assert result == 1
    with pytest.raises(ValueError):
        validhr(value, data)
    with pytest.raises(NameError):
        validhr(name, data)


@pytest.mark.parametrize("time", [{"patient_id": 1,
                                  "heart_rate_average_since":
                                      "2018-03-09 11:00:36.372339"}])
@pytest.mark.parametrize("name", [({"patient_id": 1}),
                                  ({"patient_id": 1,
                                   "heart_rate_average_since": 2334})])
@pytest.mark.parametrize("value", [({"patient_id": 5,
                                     "heart_rate_average_since":
                                         "2018-03-09 11:00:36.372339"}),
                                   ({"patient_id": 1,
                                     "heart_rate_average_since": "234"})
                                   ])
def test_validtime(time, name, value, data):
    from request_validation import validtime
    result = validtime(time, data)
    assert result == 1
    with pytest.raises(NameError):
        validtime(name, data)
    with pytest.raises(ValueError):
        validtime(value, data)


def test_validid(data):
    from request_validation import validid
    result = validid(1, data)
    assert result == 1
    with pytest.raises(NameError):
        validid('s', data)
    with pytest.raises(IndexError):
        validid(2, data)
    with pytest.raises(ValueError):
        validid(5, data)


@pytest.mark.parametrize('dtype', [('str', True),
                                   (123, True),
                                   ([234], False),
                                   ({"asdf": 2}, False)])
def test_validtype(dtype):
    from request_validation import validtype
    result = validtype(dtype[0])
    assert result == dtype[1]
