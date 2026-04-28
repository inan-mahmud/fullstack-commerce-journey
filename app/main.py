from fastapi import FastAPI

# Create FastAPI application instance
app = FastAPI(
    title="Fullstack Commerce Journey",
    description="An e-commerce backend learning project",
    version="0.1.0",
)


@app.get("/")
async def root():
    """
    Root endpoint - returns a welcome message.
    """
    return {
        "message": "Welcome to Fullstack Commerce Journey API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {"status": "healthy"}