import threading
import time
import uuid

class JobManager:
    def __init__(self):
        self.jobs = {}

    def create_job(self):
        job_id = str(uuid.uuid4())
        self.jobs[job_id] = {
            "status": "pending",
            "result": None
        }
        return job_id

    def update_job(self, job_id, result):
        self.jobs[job_id]["status"] = "completed"
        self.jobs[job_id]["result"] = result

    def get_job(self, job_id):
        return self.jobs.get(job_id)


job_manager = JobManager()