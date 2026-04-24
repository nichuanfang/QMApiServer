from contextlib import asynccontextmanager
from contextvars import ContextVar

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from qqmusic_api import Client, Credential

from models import ApiResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：初始化全局配置或 Session
    print("Starting...")
    yield
    # 关闭时：释放资源
    print("Shutting down...")

# 创建一个上下文变量
current_client: ContextVar[Client | None] = ContextVar("client", default=None)

app = FastAPI(
    title="QQMusic API",
    description="QQMusic API Web Port",
    version="1.0.0",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    default_response_class=ApiResponse,  # 设置默认响应类
)

# 常用中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


# 自动注入客户端
@app.middleware("http")
async def inject_credential_middleware(request: Request, call_next):
    # 是否使用加密接口
    enableSign = request.headers.get("X-Enable-Sign")
    # 音乐id
    musicid = request.cookies.get("musicid")
    # 音乐密钥
    musickey = request.cookies.get("musickey")
    # 登录方式
    login_type = request.cookies.get("login_type")
    # 刷新key
    refresh_key = request.cookies.get("refresh_key")
    # 刷新token
    refresh_token = request.cookies.get("refresh_token")

    if musicid and musickey:
        # 准备基础参数
        cred_kwargs = {"musicid": musicid, "musickey": musickey}

        # 如果有刷新相关的参数，动态加入字典
        if refresh_key and refresh_token and login_type:
            cred_kwargs.update({
                "refresh_token": refresh_token,
                "refresh_key": refresh_key,
                "login_type": login_type
            })

        cred = Credential(**cred_kwargs)

        client = Client(credential=cred)
        if enableSign:
            client.enable_sign = enableSign
        token = current_client.set(client)
    else:
        token = None
    try:
        response = await call_next(request)
        return response
    finally:
        # 请求结束后重置，防止上下文污染
        if token:
            current_client.reset(token)


@app.get("/login/api_check_expired")
async def check_expired():
    """
    检测cookie是否过期
    """
    client = current_client.get()
    if client:
        try:
            result = await client.login.check_expired()
            return ApiResponse.success(result)
        except Exception as e:
            return ApiResponse.error(errors="服务器处理请求时发生异常",message=e.__str__(),status_code=400)
    else:
        return ApiResponse.error(errors="未授权",status_code=401)


@app.get("/login/api_refresh_cookies")
async def refresh_credential():
    """
    刷新cookie
    :return: 新的凭据
    """
    client = current_client.get()
    if client:
        try:
            credential = await client.login.refresh_credential()
            return ApiResponse.success(credential)
        except Exception as e:
            return ApiResponse.error(errors="服务器处理请求时发生异常", message=e.__str__(), status_code=400)
    else:
        return ApiResponse.error(errors="未授权",status_code=401)


if __name__ == "__main__":
    import uvicorn

    # 这里的 "app:app" 指的是：文件名是 app.py，变量名是 app
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
