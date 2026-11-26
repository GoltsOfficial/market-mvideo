from fastapi import FastAPI

from routes import plans


app = FastAPI(title="Market")

app.include_router(plans.router)


@app.get("/")
def root():
    return {"message": "Server is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
