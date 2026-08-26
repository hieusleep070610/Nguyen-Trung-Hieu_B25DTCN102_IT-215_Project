from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status_code": exc.status_code,
                "message": exc.detail
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        error = exc.errors()[0]

        field = error["loc"][-1]
        msg = error["msg"]

        if msg == "Field required":
            message = f"Trường '{field}' là bắt buộc"

        elif "Input should be greater than or equal to" in msg:
            message = f"Giá trị của '{field}' không hợp lệ"

        elif "String should match pattern" in msg:
            message = f"'{field}' không đúng định dạng"

        elif "String should have at least" in msg:
            message = f"'{field}' quá ngắn"

        elif "String should have at most" in msg:
            message = f"'{field}' quá dài"

        else:
            message = msg

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": message,
                "detail": exc.errors()
            }
        )
