@echo off
echo Starting Movie Theater Microservices Architecture...

:: Start Movie Service
start "Movie Service (8001)" cmd /k "venv\Scripts\activate && cd Movie-service && uvicorn main:app --port 8001 --reload"

:: Start Theater Service
start "Theater Service (8002)" cmd /k "venv\Scripts\activate && cd Theater-service && uvicorn main:app --port 8002 --reload"

:: Start Show Service
start "Show Service (8003)" cmd /k "venv\Scripts\activate && cd Show-service && uvicorn main:app --port 8003 --reload"

:: Start Booking Service
start "Booking Service (8004)" cmd /k "venv\Scripts\activate && cd Booking-service && uvicorn main:app --port 8004 --reload"

:: Start Payment Service
start "Payment Service (8005)" cmd /k "venv\Scripts\activate && cd Payment-service && uvicorn main:app --port 8005 --reload"

:: Start API Gateway
echo Starting API Gateway...
start "API Gateway (8000)" cmd /k "venv\Scripts\activate && cd gateway && uvicorn main:app --port 8000 --reload"

echo All servers are booting up in separate windows!