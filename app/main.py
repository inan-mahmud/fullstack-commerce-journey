from fastapi import FastAPI
from app.api.v1 import products, categories

# Create FastAPI application instance
app = FastAPI(
    title="Fullstack Commerce Journey",
    description="An e-commerce backend learning project with JSON:API responses",
    version="0.1.0",
)

# Include API v1 routers
app.include_router(products.router, prefix="/api/v1", tags=["Products"])
app.include_router(categories.router, prefix="/api/v1", tags=["Categories"])


@app.get("/")
async def root():
    """
    Root endpoint - returns a welcome message.
    """
    return {
        "message": "Welcome to Fullstack Commerce Journey API",
        "version": "0.1.0",
        "docs": "/docs",
        "api_v1": "/api/v1"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}