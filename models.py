from time import time
from typing import Any
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

class ApiResponseModel(BaseModel):
    """API响应数据模型"""

    code: int
    message: str
    data: Any = None
    errors: list[str] | None = None
    timestamp: int


class ApiResponse(JSONResponse):
    """标准化API响应类"""

    def __init__(
        self,
        status_code: int = status.HTTP_200_OK,
        message: str = "Success",
        data: Any = None,
        errors: str | list[str] | None = None,
        **kwargs,
    ):
        # 错误信息标准化处理
        processed_errors = None
        if errors:
            processed_errors = [errors] if isinstance(errors, str) else errors

        # 构建响应内容
        content = ApiResponseModel(
            code=status_code, message=message, data=data, errors=processed_errors, timestamp=int(time())
        ).dict(exclude_unset=True, exclude_defaults=True)

        super().__init__(content=content, status_code=status_code, **kwargs)

    @classmethod
    def success(
        cls, data: Any = None, message: str = "Success", status_code: int = status.HTTP_200_OK
    ) -> "ApiResponse":
        """构建成功响应"""
        return cls(status_code=status_code, message=message, data=data)

    @classmethod
    def error(
        cls, errors: str | list[str], message: str = "Error", status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> "ApiResponse":
        """构建错误响应"""
        return cls(status_code=status_code, message=message, errors=errors)