import uvicorn

# 파일이 실행되었을 때 유비콘을 통해 서버를 실행시킴
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8000)
