from sqlalchemy import Column, Integer, String, Date, Time, Text, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database.connection import Base


class Especialidad(Base):
    __tablename__ = "especialidad"

    id_especialidad = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100), nullable=False)

    consultorios = relationship("Consultorio", back_populates="especialidad")


class Medico(Base):
    __tablename__ = "medico"

    id_medico = Column(Integer, primary_key=True, index=True)
    primer_nombre = Column(String(50), nullable=False)
    segundo_nombre = Column(String(50))
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50))
    correo = Column(String(100))

    consultorios = relationship("Consultorio", back_populates="medico")
    citas = relationship("Cita", back_populates="medico")


class Paciente(Base):
    __tablename__ = "paciente"

    cedula_paciente = Column(String(20), primary_key=True, index=True)
    id_rol = Column(Integer)
    primer_nombre = Column(String(50), nullable=False)
    segundo_nombre = Column(String(50))
    primer_apellido = Column(String(50), nullable=False)
    segundo_apellido = Column(String(50))
    edad = Column(Integer)
    tipo_sangre = Column(String(5))
    telefono = Column(String(20))
    correo = Column(String(100))

    citas = relationship("Cita", back_populates="paciente")


class Consultorio(Base):
    __tablename__ = "consultorio"

    id_consultorio = Column(Integer, primary_key=True, index=True)
    id_medico = Column(Integer, ForeignKey("medico.id_medico", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    id_especialidad = Column(Integer, ForeignKey("especialidad.id_especialidad", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)

    medico = relationship("Medico", back_populates="consultorios")
    especialidad = relationship("Especialidad", back_populates="consultorios")
    citas = relationship("Cita", back_populates="consultorio")


class Cita(Base):
    __tablename__ = "cita"

    id_cita = Column(Integer, primary_key=True, index=True)
    cedula_paciente = Column(String(20), ForeignKey("paciente.cedula_paciente", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    id_consultorio = Column(Integer, ForeignKey("consultorio.id_consultorio", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    id_medico = Column(Integer, ForeignKey("medico.id_medico", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    fecha_cita = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    motivo = Column(Text)
    estado = Column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("estado IN ('pendiente', 'confirmada', 'cancelada', 'completada')", name="chk_estado_cita"),
    )

    paciente = relationship("Paciente", back_populates="citas")
    consultorio = relationship("Consultorio", back_populates="citas")
    medico = relationship("Medico", back_populates="citas")
