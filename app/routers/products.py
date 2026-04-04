from fastapi import APIRouter

router = APIRouter(prefix="/products",
                    responses={404: {"description": "Product not found"}},
                    tags=["Products"]) #prefijo para todas las rutas de este router y tag para documentacion


@router.get("") #La solicitud tuvo éxito, El recurso ha sido recuperado y transmitido en el cuerpo del mensaje.
async def products():
    return [{"name": "laptop", "price": 1000},
            {"name": "phone", "price": 500},
            {"name": "tablet", "price": 300}]   
