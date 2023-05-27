import uvicorn

if __name__ == "__main__":
    uvicorn.run("projects.main:app", host="127.0.0.1", port=300, reload=True) #host="0.0.0.0", port=300
