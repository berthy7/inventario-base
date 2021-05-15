from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.usuario.model import Usuario, Modulo
from servidor.sistema.usuarios.rol.model import Rol
from datetime import datetime

import pytz
global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class BitacoraManager(SuperManager):

    def __init__(self, db):
        super().__init__(Bitacora, db)

    def list_all(self):
        return dict(objects=self.db.query(Bitacora).order_by(Bitacora.id.asc()))

    def fecha_actual(self):
        fzona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha_str = fzona.strftime('%Y-%m-%d %H:%M:%S.%f')
        dtm_fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')

        return dtm_fecha

    def fecha(self):
        return fecha_zona.strftime('%Y/%d/%m')

    def get_privileges(self, id, route):
        parent_module = self.db.query(Modulo).join(Rol.modulos).join(Usuario).filter(Modulo.ruta == route).filter(Usuario.id == id).filter(Usuario.enabled).first()

        if not parent_module:
            return dict()

        modules = self.db.query(Modulo).join(Rol.modulos).join(Usuario).filter(Modulo.fkmodulo == parent_module.id).filter(Usuario.id == id).filter(Usuario.enabled)
        privileges = {parent_module.nombre: parent_module}

        for module in modules:
            privileges[module.nombre] = module

        return privileges

    def all_data(self, idu):
        privilegios = self.get_privileges(idu, '/bitacora')
        logs = self.db.query(self.entity).all()
        list = []

        if 'bitacora_query' in privilegios:
            for item in logs:
                username = item.usuario.username if item.fkusuario else ''
                diccionario = item.get_dict()
                diccionario['username'] = username

                list.append(diccionario)

        return list
