from queues.worker import process_query
from queues.client import queue

from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
@app.post("/chat")
def chat(
        query: str = Query(..., description="The query to process"),
):

    job = queue.enqueue(process_query, query)

    return {"job_id": job.id, "status": "queued", "query": query}

@app.get("/result")
def get_result(
        job_id: str = Query(..., description="The job ID to retrieve the result for"),
):
    job = queue.fetch_job(job_id)
    if job is None:
        return {"error": "Job not found"}
    if job.is_finished:
        return {"job_id": job.id, "status": "finished", "result": job.return_value}
    elif job.is_failed:
        return {"job_id": job.id, "status": "failed", "error": str(job.exc_info)}
    else:
        return {"job_id": job.id, "status": "in progress"}