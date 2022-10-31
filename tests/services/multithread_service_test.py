from time import sleep
from app.services.multithread import MultithreadJob


def test_multithread_execution():
    def test_function(a, b):
        sleep(0.5)
        return a + b

    jobs_info = [
        [test_function, [1, 1]],
        [test_function, [2, 2]],
        [test_function, [0, 0]]
    ]
    job = MultithreadJob(jobs_info)
    job.start()
    job.join()

    responses = job.get_results()

    assert len(responses) == 3
    assert len(list(filter(lambda r: r > 2, responses))) == 1
    assert len(list(filter(lambda r: r < 3, responses))) == 2


def test_multithread_execution_with_errors():
    def test_function(*args):
        sleep(0.5)
        return "Hello World!"

    def test_function_exception(*args):
        sleep(0.5)
        raise Exception

    jobs_info = [
        [test_function, ["a", "b"]],
        [test_function_exception, [1, 2]],
        [test_function, ["a", "b"]],
        [test_function_exception, [1, 2]],
        [test_function, ["a", "b"]],
        [test_function_exception, [1, 2]],
    ]
    job = MultithreadJob(jobs_info)
    job.start()
    job.join()

    responses = job.get_results()

    assert len(responses) == 6
    assert len(list(filter(lambda r: r is None, responses))) == 3
    assert len(list(filter(lambda r: r == "Hello World!", responses))) == 3
