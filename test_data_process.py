import pytest


@pytest.fixture
def data():
    import datetime
    database = {"patient_id": 1,
                "Timestamp": [datetime.datetime(2018, 3, 9, 11, 0, 36, 372339),
                              datetime.datetime(2018, 3, 9, 11, 0, 36, 372340),
                              datetime.datetime(2018, 3, 9, 11, 0, 37, 372339),
                              datetime.datetime(2018, 3, 9, 11, 1, 36, 372339),
                              datetime.datetime(2018, 3, 9, 12, 0, 36, 372339),
                              datetime.datetime(2018, 3, 10, 11, 0, 36,
                                                372339),
                              datetime.datetime(2018, 4, 9, 11, 0, 36, 372339),
                              datetime.datetime(2019, 3, 9, 11, 0, 36,
                                                372339)],
                "HR_list": [50, 60, 70, 80, 90, 100, 110, 120]}
    return database


@pytest.mark.parametrize('tachycardia', [(150, 1, "Negative"),
                                         (150, "1", "Negative"),
                                         (152, 2, "Positive"),
                                         (137, 3, "Negative"),
                                         (138, 4, "Positive"),
                                         (133, 5, "Negative"),
                                         (135, 7, "Positive"),
                                         (119, 12, "Negative"),
                                         (120, 14, "Positive"),
                                         (110, 16, "Positive"),
                                         (99, 30, "Negative")
                                         ])
def test_tachycardia(tachycardia):
    from data_process import tachycardic
    result = tachycardic(tachycardia[0], tachycardia[1])
    assert result == tachycardia[2]


@pytest.mark.parametrize('avg', [
    ([100], 100),
    ([100, 110], 105),
    ([100, 101], 100.5),
    ([100, 101, 101], 100.67),
    ([90, 90, 90, 90, 91, 90], 90.17)
])
def test_avg_hr(avg):
    from data_process import avg_hr
    result = avg_hr(avg[0])
    assert result == pytest.approx(avg[1])


@pytest.mark.parametrize("intv_avg", [("2018-03-09 11:00:36.372339", 85),
                                      ("2018-03-09 11:00:36.372340", 90),
                                      ("2018-03-09 11:00:37.372330", 95),
                                      ("2018-03-09 11:01:36.372339", 100),
                                      ("2018-03-09 12:00:36.372339", 105),
                                      ("2018-03-10 11:00:36.372339", 110),
                                      ("2018-04-09 11:00:36.372339", 115),
                                      ("2019-03-09 11:00:36.372339", 120)
                                      ])
@pytest.mark.parametrize("exceptions", ["2020-03-09 11:00:36.372339"])
def test_get_intv_avg(intv_avg, data, exceptions):
    from data_process import get_intv_avg
    import datetime
    result = get_intv_avg(data, intv_avg[0])
    assert result == pytest.approx(intv_avg[1])
    with pytest.raises(IndexError):
        get_intv_avg(data, exceptions)
