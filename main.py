import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import List

from Logger import Logger
from models.ProductionPlanRequest import ProductionPlanRequest
from models.ProductionPlanResponse import ProductPlanResponseItem

app = FastAPI()
logger = Logger()


@app.post('/productionplan', response_model=List[ProductPlanResponseItem])
def get_production_plan(request: ProductionPlanRequest):
    return request.generate_response()


@app.get('/')
def read_root():
    return {
        'message': 'The only route is /productionplan which accepts a post request , plz go to /docs which integrates '
                   'swagger ui'}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_request: Request, exc: RequestValidationError):
    logger.error(f'Validation error: {exc}')
    return JSONResponse(
        status_code=422,
        content={'detail': exc.errors(), 'body': exc.body}
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(_request: Request, exc: StarletteHTTPException):
    logger.error(f'HTTP error {exc.status_code}: {exc.detail}')
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': str(exc.detail)},
    )


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception):
    logger.error(f'Unhandled error: {exc}')
    return JSONResponse(
        status_code=500,
        content={'message': 'An unexpected error occurred'},
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8888)
