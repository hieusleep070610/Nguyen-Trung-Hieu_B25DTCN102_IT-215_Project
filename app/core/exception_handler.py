from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request,exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "message": exc.detail
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request,exc: RequestValidationError):
        # Lấy lỗi
        error = exc.errors()[0]

        field = error["loc"][-1]
        msg = error["msg"]

        if msg == "Field required":
            message = "Có Field bắt buộc phải nhập"
        elif "Input should be greater than or equal to" in msg:
            message = "Field không hợp lệ"

        elif "String should match pattern" in msg:
            message = "Có Field nhập sai định dạng"

        else:
            message = msg

        return JSONResponse(
            status_code=422,
            content={
                "message": message
            }
        )