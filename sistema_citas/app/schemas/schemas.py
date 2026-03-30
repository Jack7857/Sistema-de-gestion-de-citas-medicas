from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date, time


# ── ESPECIALIDAD ──────────────────────────────────────────────
class EspecialidadBase(BaseModel):
    descripcion: str

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadUpdate(BaseModel):
    descripcion: Optional[str] = None

class EspecialidadOut(EspecialidadBase):
    id_especialidad: int

    model_config = {"from_attributes": True}


# ── MÉDICO ────────────────────────────────────────────────────
class MedicoBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    correo: Optional[str] = None

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(BaseModel):
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    correo: Optional[str] = None

class MedicoOut(MedicoBase):
    id_medico: int

    model_config = {"from_attributes": True}


# ── PACIENTE ──────────────────────────────────────────────────
class PacienteBase(BaseModel):
    cedula_paciente: str
    id_rol: Optional[int] = None
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    edad: Optional[int] = None
    tipo_sangre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

    @field_validator("edad")
    @classmethod
    def edad_no_negativa(cls, v):
        if v is not None and v < 0:
            raise ValueError("La edad no puede ser negativa")
        return v

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    id_rol: Optional[int] = None
    primer_nombre: Optional[str] = None
    segundo_nombre: Optional[str] = None
    primer_apellido: Optional[str] = None
    segundo_apellido: Optional[str] = None
    edad: Optional[int] = None
    tipo_sangre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

class PacienteOut(PacienteBase):
    model_config = {"from_attributes": True}


# ── CONSULTORIO ───────────────────────────────────────────────
class ConsultorioBase(BaseModel):
    id_medico: int
    id_especialidad: int

class ConsultorioCreate(ConsultorioBase):
    pass

class ConsultorioUpdate(BaseModel):
    id_medico: Optional[int] = None
    id_especialidad: Optional[int] = None

class ConsultorioOut(ConsultorioBase):
    id_consultorio: int

    model_config = {"from_attributes": True}


# ── CITA ──────────────────────────────────────────────────────
ESTADOS_VALIDOS = {"pendiente", "confirmada", "cancelada", "completada"}

class CitaBase(BaseModel):
    cedula_paciente: str
    id_consultorio: int
    id_medico: int
    fecha_cita: date
    hora: time
    motivo: Optional[str] = None
    estado: str

    @field_validator("estado")
    @classmethod
    def estado_valido(cls, v):
        if v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Opciones: {ESTADOS_VALIDOS}")
        return v

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    cedula_paciente: Optional[str] = None
    id_consultorio: Optional[int] = None
    id_medico: Optional[int] = None
    fecha_cita: Optional[date] = None
    hora: Optional[time] = None
    motivo: Optional[str] = None
    estado: Optional[str] = None

    @field_validator("estado")
    @classmethod
    def estado_valido(cls, v):
        if v is not None and v not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado inválido. Opciones: {ESTADOS_VALIDOS}")
        return v

class CitaOut(CitaBase):
    id_cita: int

    model_config = {"from_attributes": True}
