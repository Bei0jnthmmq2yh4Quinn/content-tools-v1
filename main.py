"""
Content Tools - 自媒体运营工具
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import trends, analysis, topics, media, health

app = FastAPI(title="Content Tools", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(trends.router, prefix="/api/trends", tags=["trends"])
app.include_router(analysis.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(topics.router, prefix="/api/topics", tags=["topics"])
app.include_router(media.router, prefix="/api/media", tags=["media"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
