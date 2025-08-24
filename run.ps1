# Navigate to the project root
cd (Split-Path -Path $MyInvocation.MyCommand.Path -Parent)

Write-Host "Activating virtual environment..."
& ".\venv\Scripts\activate"

Write-Host "Stopping and removing existing Redis container..."
docker stop redis-server | Out-Null
docker rm redis-server | Out-Null

Write-Host "Starting Redis server..."
docker run --name redis-server -d -p 6379:6379 redis

Write-Host "Starting FastAPI server in the background..."
Start-Process powershell -ArgumentList "-Command `"uvicorn src.backend.main:app --reload`""

Write-Host "Starting Celery worker in the foreground..."
& ".\venv\Scripts\celery" -A src.tasks worker --loglevel=info --pool=gevent