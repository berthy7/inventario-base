from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.negocio.traspaso.model import Traspaso
from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class TraspasoManager(SuperManager):

    def __init__(self, db):
        super().__init__(Traspaso, db)

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/traspaso')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list_dt = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'traspaso_update' not in privilegios else ''
            origen = item.origen.nombre if item.origen else ''
            destino = item.destino.nombre if item.destino else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'traspaso_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['origen'] = origen
            diccionario['destino'] = destino
            list_dt.append(diccionario)

        return list_dt

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = fecha

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registró traspaso.", fecha=fecha, tabla="negocio_traspaso", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó traspaso.", fecha=fecha, tabla="negocio_traspaso", identificador=a.id)
        super().insert(b)
        return a

    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó traspaso" if estado else "Deshabilitó traspaso"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="negocio_traspaso", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó traspaso", fecha=fecha, tabla="negocio_traspaso", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

