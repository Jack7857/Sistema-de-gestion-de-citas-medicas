from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Especialidad
from app.schemas import EspecialidadCreate, EspecialidadUpdate, EspecialidadOut

router = APIRouter(prefix="/especialidades", tags=["Especialidades"])


@router.get("/", response_model=List[EspecialidadOut])
def listar_especialidades(db: Session = Depends(get_db)):
    return db.query(Especialidad).all()


@router.get("/{id_especialidad}", response_model=EspecialidadOut)
def obtener_especialidad(id_especialidad: int, db: Session = Depends(get_db)):
    esp = db.query(Especialidad).filter(Especialidad.id_especialidad == id_especialidad).first()
    if not esp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada")
    return esp


@router.post("/", response_model=EspecialidadOut, status_code=status.HTTP_201_CREATED)
def crear_especialidad(data: EspecialidadCreate, db: Session = Depends(get_db)):
    nueva = Especialidad(**data.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.put("/{id_especialidad}", response_model=EspecialidadOut)
def actualizar_especialidad(id_especialidad: int, data: EspecialidadUpdate, db: Session = Depends(get_db)):
    esp = db.query(Especialidad).filter(Especialidad.id_especialidad == id_especialidad).first()
    if not esp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada")
    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(esp, campo, valor)
    db.commit()
    db.refresh(esp)
    return esp


@router.delete("/{id_especialidad}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_especialidad(id_especialidad: int, db: Session = Depends(get_db)):
    esp = db.query(Especialidad).filter(Especialidad.id_especialidad == id_especialidad).first()
    if not esp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Especialidad no encontrada")
    db.delete(esp)
    db.commit()
