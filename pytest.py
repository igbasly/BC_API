from app import app
from flask import request
from json import load, loads

with open("tests.json", "r") as file:
    TESTS = load(file)

url = "/api/v1?"
print("\n---- Starting Tests ----\n")
for test in TESTS:
    print(f"Running {test}")
    data = TESTS[test]
    req = data[0]
    res = data[1]
    url_test = url + "&".join(
        [f"{t[0]}={'+'.join(t[1].split(' '))}" for t in req])
    with app.test_client() as C:
        resp_test = C.get(url_test)
        for r in req:
            assert request.args[r[0]] == r[1]
        #print(resp_test.get_json())
        assert resp_test.get_json() == res

print("\n---- Tests finished successfully ----\n")