from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional, Any, Dict
import httpx

from auth import jwt_authentication, create_access_token

app = FastAPI(title="Movie Theater API Gateway", version="1.0.0")

# -------------------------------------------------
# SERVICES
# -------------------------------------------------
SERVICES = {
    "movie": "http://localhost:8001",
    "theater": "http://localhost:8002",
    "show": "http://localhost:8003",
    "booking": "http://localhost:8004",
    "payment": "http://localhost:8005"
}

# -------------------------------------------------
# LOGGING MIDDLEWARE
# -------------------------------------------------
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print(f"[REQUEST] {request.method} {request.url}")
        response = await call_next(request)
        print(f"[RESPONSE] {response.status_code}")
        return response

app.add_middleware(LoggingMiddleware)

# -------------------------------------------------
# REQUEST FORWARDER WITH ENHANCED ERROR HANDLING
# -------------------------------------------------
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service '{service}' not registered"
        )

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, **kwargs)

            if response.status_code >= 400:
                return JSONResponse(
                    status_code=response.status_code,
                    content={
                        "error": True,
                        "service": service,
                        "message": response.json().get("detail", "Service error"),
                        "path": path
                    }
                )

            return JSONResponse(
                status_code=response.status_code,
                content=response.json() if response.content else None
            )

        except httpx.ConnectError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"{service} service is unavailable at {url}"
            )

        except httpx.TimeoutException:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail=f"{service} service timeout"
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Gateway error: {str(e)}"
            )

# -------------------------------------------------
# GLOBAL EXCEPTION HANDLERS
# -------------------------------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": True,
            "status_code": 500,
            "message": "Internal server error",
            "details": str(exc),
            "path": str(request.url)
        }
    )

# -------------------------------------------------
# ROOT & AUTH
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Movie Theater API Gateway is running",
        "available_services": list(SERVICES.keys())
    }

@app.post("/gateway/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    # Note: Replace with proper DB check later if needed
    if username == "Movie" and password == "Movie":
        access_token = create_access_token({"sub": username})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    raise HTTPException(status_code=401, detail="Invalid credentials")

# =================================================
# 1. MOVIE ROUTES (Port 8001)
# =================================================
@app.get("/gateway/movies", dependencies=[Depends(jwt_authentication)])
async def get_movies():
    return await forward_request("movie", "/api/movies", "GET")

@app.get("/gateway/movies/{movie_id}", dependencies=[Depends(jwt_authentication)])
async def get_movie(movie_id: int):
    return await forward_request("movie", f"/api/movies/{movie_id}", "GET")

@app.post("/gateway/movies", status_code=201, dependencies=[Depends(jwt_authentication)])
async def create_movie(payload: Dict[Any, Any]):
    return await forward_request("movie", "/api/movies", "POST", json=payload)

@app.put("/gateway/movies/{movie_id}", dependencies=[Depends(jwt_authentication)])
async def update_movie(movie_id: int, payload: Dict[Any, Any]):
    return await forward_request("movie", f"/api/movies/{movie_id}", "PUT", json=payload)

@app.delete("/gateway/movies/{movie_id}", status_code=204, dependencies=[Depends(jwt_authentication)])
async def delete_movie(movie_id: int):
    return await forward_request("movie", f"/api/movies/{movie_id}", "DELETE")

# =================================================
# 2. THEATER ROUTES (Port 8002)
# =================================================
@app.get("/gateway/theaters", dependencies=[Depends(jwt_authentication)])
async def get_theaters():
    return await forward_request("theater", "/api/theaters", "GET")

@app.get("/gateway/theaters/{theater_id}", dependencies=[Depends(jwt_authentication)])
async def get_theater(theater_id: int):
    return await forward_request("theater", f"/api/theaters/{theater_id}", "GET")

@app.post("/gateway/theaters", status_code=201, dependencies=[Depends(jwt_authentication)])
async def create_theater(payload: Dict[Any, Any]):
    return await forward_request("theater", "/api/theaters", "POST", json=payload)

@app.put("/gateway/theaters/{theater_id}", dependencies=[Depends(jwt_authentication)])
async def update_theater(theater_id: int, payload: Dict[Any, Any]):
    return await forward_request("theater", f"/api/theaters/{theater_id}", "PUT", json=payload)

@app.delete("/gateway/theaters/{theater_id}", status_code=204, dependencies=[Depends(jwt_authentication)])
async def delete_theater(theater_id: int):
    return await forward_request("theater", f"/api/theaters/{theater_id}", "DELETE")

# =================================================
# 3. SHOW ROUTES (Port 8003)
# =================================================
@app.get("/gateway/shows", dependencies=[Depends(jwt_authentication)])
async def get_shows():
    return await forward_request("show", "/api/shows", "GET")

@app.get("/gateway/shows/{show_id}", dependencies=[Depends(jwt_authentication)])
async def get_show(show_id: int):
    return await forward_request("show", f"/api/shows/{show_id}", "GET")

@app.post("/gateway/shows", status_code=201, dependencies=[Depends(jwt_authentication)])
async def create_show(payload: Dict[Any, Any]):
    return await forward_request("show", "/api/shows", "POST", json=payload)

@app.put("/gateway/shows/{show_id}", dependencies=[Depends(jwt_authentication)])
async def update_shows(show_id: int, payload: Dict[Any, Any]):
    return await forward_request("show", f"/api/shows/{show_id}", "PUT", json=payload)

@app.delete("/gateway/shows/{show_id}", status_code=204, dependencies=[Depends(jwt_authentication)])
async def delete_shows(show_id: int):
    return await forward_request("show", f"/api/shows/{show_id}", "DELETE")

# =================================================
# 4. BOOKING ROUTES (Port 8004)
# =================================================
@app.get("/gateway/bookings", dependencies=[Depends(jwt_authentication)])
async def get_bookings():
    return await forward_request("booking", "/api/bookings", "GET")

@app.get("/gateway/bookings/{booking_id}", dependencies=[Depends(jwt_authentication)])
async def get_booking(booking_id: int):
    return await forward_request("booking", f"/api/bookings/{booking_id}", "GET")

@app.post("/gateway/bookings", status_code=201, dependencies=[Depends(jwt_authentication)])
async def create_booking(payload: Dict[Any, Any]):
    return await forward_request("booking", "/api/bookings", "POST", json=payload)

@app.put("/gateway/bookings/{booking_id}", dependencies=[Depends(jwt_authentication)])
async def update_booking(booking_id: int, payload: Dict[Any, Any]):
    return await forward_request("booking", f"/api/bookings/{booking_id}", "PUT", json=payload)

@app.delete("/gateway/bookings/{booking_id}", status_code=204, dependencies=[Depends(jwt_authentication)])
async def delete_booking(booking_id: int):
    return await forward_request("booking", f"/api/bookings/{booking_id}", "DELETE")

# =================================================
# 5. PAYMENT ROUTES (Port 8005)
# =================================================
@app.get("/gateway/payments", dependencies=[Depends(jwt_authentication)])
async def get_payments():
    return await forward_request("payment", "/api/payments", "GET")

@app.get("/gateway/payments/{payment_id}", dependencies=[Depends(jwt_authentication)])
async def get_payment(payment_id: int):
    return await forward_request("payment", f"/api/payments/{payment_id}", "GET")

@app.post("/gateway/payments", status_code=201, dependencies=[Depends(jwt_authentication)])
async def create_payment(payload: Dict[Any, Any]):
    return await forward_request("payment", "/api/payments", "POST", json=payload)

@app.put("/gateway/payments/{payment_id}", dependencies=[Depends(jwt_authentication)])
async def update_payment(payment_id: int, payload: Dict[Any, Any]):
    return await forward_request("payment", f"/api/payments/{payment_id}", "PUT", json=payload)

@app.delete("/gateway/payments/{payment_id}", status_code=204, dependencies=[Depends(jwt_authentication)])
async def delete_payment(payment_id: int):
    return await forward_request("payment", f"/api/payments/{payment_id}", "DELETE")