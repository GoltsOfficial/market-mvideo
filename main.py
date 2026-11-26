from fastapi import FastAPI

app = FastAPI(title="Market")


@app.get("/")
def root():
    return {"message": "Server is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
