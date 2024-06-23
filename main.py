import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from Logger import Logger

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f'HTTP error {exc.status_code}: {exc.detail}')
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': str(exc.detail)},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f'Unhandled error: {exc}')
    return JSONResponse(
        status_code=500,
        content={'message': 'An unexpected error occurred'},
    )


if __name__ == '__main__':
    logger = Logger()
    uvicorn.run(app, host='0.0.0.0', port=8888)
