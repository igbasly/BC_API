from threading import Thread, Lock
from typing import List


class Worker(Thread):

    def __init__(self, target_function, args):
        super().__init__(daemon=True)
        self.target_function = target_function
        self.function_args = args
        self.ready = False
        self.response = None

    def run(self):
        try:
            self.response = self.target_function(*self.function_args)
        except Exception:
            self.response = None
        self.ready = True


class MultithreadJob(Thread):
    max_workers = 10

    def __init__(self, jobs: List[List] = []):
        super().__init__(daemon=True)
        self.my_workers_lock = Lock()
        self.active_workers = []
        self.workers = []
        for job in jobs:
            worker = Worker(job[0], job[1])
            self.workers.append(worker)
            self.active_workers.append(False)

    def add_job(self, function, args):
        self.workers.append(Worker(function, args))
        self.active_workers.append(False)

    def run(self):
        while self.completed_workers() < len(self.workers):
            for i in range(len(self.workers)):
                worker = self.workers[i]
                if worker.ready or self.active_workers[i]:
                    continue
                if len(list(filter(lambda x: x, self.active_workers))) <\
                        self.max_workers:
                    worker.start()
                    self.active_workers[i] = True
                else:
                    for j in range(len(self.workers)):
                        if self.active_workers[j]:
                            self.workers[j].join()
                            self.active_workers[j] = False

            for i in range(len(self.workers)):
                worker = self.workers[i]
                if worker.ready:
                    self.active_workers[i] = False

    def completed_workers(self):
        return len(list(filter(lambda w: w.ready, self.workers)))

    def get_results(self):
        return list(map(lambda w: w.response, self.workers))
