from datetime import datetime


def validate_request(request):
    if not isinstance(request, dict):
        return False
    if not all(key in request for key in ["dt_from", "dt_upto", "group_type"]):
        return False

    try:
        datetime.strptime(request["dt_from"], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False

    try:
        datetime.strptime(request["dt_upto"], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return False

    if request["group_type"] not in ("month", "hour", "day"):
        return False

    return True


if __name__ == "__main__":

    some = {
        "dt_from": "2022-09-01T00:00:00",
        "dt_upto": "2022-12-31T23:59:00",
        "group_type": "hour"
    }
    print(validate_request(some))
