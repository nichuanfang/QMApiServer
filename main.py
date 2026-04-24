from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from qqmusic_api import Credential

# 1. 登录功能
# 2. 自动续签
# 3. qq-api功能集成

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：初始化全局配置或 Session
    print("Initializing high-performance music engine...")
    yield
    # 关闭时：释放资源
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

# 2. 异步端点设计
@app.get("/v1/search")
async def search_music(
    keyword: str = Query(..., min_length=1),
    page: int = 1,
    page_size: int = 20
):
    """
    高性能搜索接口：利用异步 I/O 避免阻塞
    """
    try:
        # 使用 library 的异步方法
        results = await Search.get_search_results(
            keyword=keyword,
            page=page,
            num=page_size
        )
        return {"code": 200, "data": results}
    except Exception as e:
        return {"code": 500, "msg": "Internal Server Error", "detail": str(e)}

@app.get("/v1/song/url")
async def get_song_url(song_mid: str):
    # 示例：获取歌曲播放链接
    url_data = await Song.get_song_urls([song_mid])
    return {"code": 200, "data": url_data}