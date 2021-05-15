from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, ForeignKey, String, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))

class Bitacora(Serializable, Base):
    way = {'usuario': {}}

    __tablename__ = 'usuarios_bitacora'

    id = Column(BigInteger, primary_key=True)
    fkusuario = Column(BigInteger, ForeignKey('usuarios_usuario.id'), nullable=True)
    ip = Column(String(100), nullable=True)
    accion = Column(String(200), nullable=True)
    fecha = Column(DateTime, nullable=False, default=fecha_zona)
    tabla = Column(String(200), nullable=True)
    identificador = Column(BigInteger, nullable=True)

    usuario = relationship('Usuario')

    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fkusuario'] == 'None':
            aux['fkusuario'] = ""

        if aux['fecha'] == 'None':
            aux['fecha'] = "----"
        else:
            aux['fecha'] = self.fecha.strftime("%d/%m/%Y %H:%M")

        if aux['ip'] == 'None':
            aux['ip'] = "----"

        return aux
