import uvicorn
from config import settings

if __name__ == "__main__":
    # Run the server directly from main.py
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True) 