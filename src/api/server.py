from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import Employee, admin
import json
import logging
import sys
from starlette.middleware.cors import CORSMiddleware

description = """
tracks employee data
"""
#on render
app = FastAPI(
    title="Employee tracker",
    description=description,
    version="0.0.1",
    terms_of_service="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
)

#origins = ["https://potion-exchange.vercel.app"]


app.include_router(Employee.router)
app.include_router(admin.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to the Echo Archives"}
