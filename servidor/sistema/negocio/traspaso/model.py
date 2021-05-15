from servidor.database.models import Base
from servidor.database.serializable import Serializable
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship


class Traspaso(Serializable, Base):
    way = {'origen': {}, 'destino': {}, 'detalle': {}}

    __tablename__ = 'negocio_traspaso'

    id = Column(Integer, primary_key=True)
    descripcion = Column(String(50), nullable=False, unique=True)
    fecha = Column(DateTime, nullable=True)
    fkorigen = Column(Integer, ForeignKey("negocio_sucursal.id"), nullable=True)
    fkdestino = Column(Integer, ForeignKey("negocio_sucursal.id"), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    origen = relationship("Sucursal", foreign_keys=[fkorigen])
    destino = relationship("Sucursal", foreign_keys=[fkdestino])
    detalle = relationship("Traspaso_detalle", cascade="save-update, merge, delete, delete-orphan")


    def get_dict(self, way=None):
        aux = super().get_dict(way)

        if aux['fecha'] == 'None':
            aux['fecha'] = "----"
        else:
            aux['fecha'] = self.fecha.strftime("%d/%m/%Y %H:%M")
        return aux

class Traspaso_detalle(Serializable, Base):
    way = {'traspaso': {}, 'producto': {}}

    __tablename__ = 'negocio_traspaso_detalle'

    id = Column(Integer, primary_key=True)
    fktraspaso = Column(Integer, ForeignKey("negocio_traspaso.id"), nullable=True)
    fkproducto = Column(Integer, ForeignKey("negocio_producto.id"), nullable=True)
    cantidad = Column(Integer, default=0)
    estado = Column(Boolean, nullable=False, default=True)
    enabled = Column(Boolean, default=True)

    traspaso = relationship("Traspaso")
    producto = relationship("Producto")
