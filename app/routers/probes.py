from fastapi import APIRouter, Response

router = APIRouter(
    prefix="/probes",
    tags=["probes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/startup")
async def startup_check():
    """
    Startup check endpoint to verify if the service has started successfully.
    """

    ## Comprobar si el servicio de fastapi esta ejecutandose correctamente

    return Response(status_code=200, content="Service is started up successfully.") 


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the service is running.
    """

    ## Comprobar si el servicio de fastapi esta ejecutandose correctamente
    

    return Response(status_code=200, content="Service is healthy.") 


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint to verify if the service is ready to accept requests.
    """

    ## Comprobar si la base de datos o las dependencias externas estan disponibles

    return Response(status_code=200, content="Service is ready to accept requests.")