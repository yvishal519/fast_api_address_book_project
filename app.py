# !/usr/bin/python
# -*- coding: utf-8 -*-

from json import JSONDecodeError
import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette import status

from webservices.configs import app_constants, app_configurations
from webservices.utilities.logger_utils import logger
from webservices.microservices.services.service import address_router

app = FastAPI(
    title="FastAPI Services 2.0 - Swagger UI",
    version="1.0",
    openapi_url=f"{app_configurations.api_service_url}/openapi.json" if app_configurations.ENVIRONMENT in (
        "dev", "local") else None,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)


@app.exception_handler(RequestValidationError)
async def input_validation_handler(request: Request, exc: RequestValidationError):
    if isinstance(exc.__context__, JSONDecodeError):  # Checking for invalid request body
        logger.error(exc)
        errs = [i['msg'] for i in exc.errors()]
        response = app_constants.result_error_template(message="Invalid Request Body.", data=errs)
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(response))

    validation_error: ValidationError = exc.raw_errors[0]

    if validation_error:
        model_fields = validation_error.model.__fields__
        validation_msgs = {field: details.get('validation_msg', None) for field, details in model_fields.items()}
        overwritten_errors = validation_error.errors()
        errs = [f"{i['loc'][-1]} - {validation_msgs.get(i['loc'][-1], i['msg'])}" for i in overwritten_errors]
        response = app_constants.result_error_template(message="Validation Error", data=errs)
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(response))


app.include_router(address_router)


@app.get(f"{app_configurations.api_service_url}/")
def read_root():
    """
    Root service
    :return:
    """
    logger.info("Welcome to the Application")
    return "Welcome to the Application"


@app.get(f"{app_configurations.api_service_url}/health")
async def get_health():
    return {"message": "OK"}


if __name__ == '__main__':
    uvicorn.run('app:app', host=app_configurations.SERVICE_HOST, port=int(app_configurations.SERVICES_PORT),
                headers=[("server", 'XXXXX')])
