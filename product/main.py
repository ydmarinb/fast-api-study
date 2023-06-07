from fastapi import FastAPI, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import schemas
from . import model
from .database import engine, SessionLocal

# Creación instancia de Fast api
app = FastAPI (
    title='Products API'
)

######################################
# Manejo de la base de datos
###################################
model.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


############################
# Definición de logica api
###############################
@app.get('/products')
def products(db:Session=Depends(get_db)):
    products = db.query(model.Product).all()
    return products

@app.get('/product/{id}')
def product(id, db:Session=Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == id).first()
    return product

@app.post('/product')
def add(request:schemas.Product, db:Session=Depends(get_db)):
    new_product = model.Product(
        name=request.name, description=request.description, price=request.price
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request


@app.put('/product/{id}')
def update(id, reponse:Response, db:Session=Depends(get_db)):
    product = db.query(model.Product).filter(model.Product.id == id)
    if not product.first():
        reponse.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Product not found')
    product.update(request.dict())
    return {'Product update'}



@app.delete('/product/{id}')
def delete(id, db:Session=Depends(get_db)):
    db.query(model.Product).filter(model.Product.id == id).delete(synchronize_session=False)
    db.commit()
