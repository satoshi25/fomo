from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"message": "hello world"}
