from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.negocio.salida.model import Salida
from datetime import datetime

import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class SalidaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Salida, db)

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/salida')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list_dt = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'salida_update' not in privilegios else ''
            sucursal = item.sucursal.nombre if item.sucursal else ''
            cliente = item.cliente.nombre if item.cliente else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'salida_delete' in privilegios

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['sucursal'] = sucursal
            diccionario['cliente'] = cliente
            list_dt.append(diccionario)

        return list_dt

    def insert(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()
        objeto.fecha = fecha

        a = super().insert(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Registr?? salida.", fecha=fecha, tabla="negocio_salida", identificador=a.id)
        super().insert(b)
        return a

    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modific?? salida.", fecha=fecha, tabla="negocio_salida", identificador=a.id)
        super().insert(b)
        return a

    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilit?? salida" if estado else "Deshabilit?? salida"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="negocio_salida", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Elimin?? salida", fecha=fecha, tabla="negocio_salida", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
