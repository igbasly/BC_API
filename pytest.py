from app import app
from flask import request
from json import load

with open("tests.json", "r") as file:
    TESTS = load(file)

errors = []

print("\n---- Starting Tests ----\n")
for test in TESTS:
    print(f"Running {test}")
    data = TESTS[test]
    url = data[0]
    req = data[1]
    res = data[2]
    url_test = url + \
        "&".join([f"{t[0]}={'+'.join(t[1].split(' '))}" for t in req])
    with app.test_client() as C:
        resp_test = C.get(url_test).get_json()
        if resp_test["code"] == 200:
            for c in resp_test["data"]:
                for s in resp_test["data"][c]:
                    for key in resp_test["data"][c][s].copy():
                        if type(key) is str and "vacantes" in key.lower():
                            resp_test["data"][c][s].pop(key)
        failed = False
        for r in req:
            try:
                assert request.args[r[0]] == r[1]
            except AssertionError as err:
                print(f"FAILED")
                errors.append((test, data, url, err))
                failed = True
                break
        if not failed:
            try:
                assert resp_test == res
                print(f"SUCCEEDED")
            except AssertionError as err:
                print(f"FAILED")
                errors.append((test, data, url, err))
                failed = True
if not errors:
    print("\n---- Tests finished successfully ----\n")
else:
    print("\n---- Tests finished with errors -----\n")
    raise AssertionError(f"{len(errors)} Falied Tests")
