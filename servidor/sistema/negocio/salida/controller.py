from servidor.common.controllers import CrudController
from servidor.sistema.negocio.salida.manager import SalidaManager
from servidor.sistema.negocio.sucursal.manager import SucursalManager
from servidor.sistema.negocio.cliente.manager import ClienteManager
from servidor.sistema.negocio.inventario.manager import InventarioManager

import json


class SalidaController(CrudController):
    manager = SalidaManager
    html_index = "sistema/negocio/salida/views/index.html"

    routes = {
        '/salida': {'GET': 'index', 'POST': 'table'},
        '/salida_insert': {'POST': 'insert'},
        '/salida_update': {'PUT': 'edit', 'POST': 'update'},
        '/salida_state': {'POST': 'state'},
        '/salida_delete': {'POST': 'delete'},
        '/salida_list': {'POST': 'data_list'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        aux['sucursales'] = SucursalManager(self.db).listar_habilitados()
        aux['clientes'] = ClienteManager(self.db).listar_habilitados()

        return aux

    def data_list(self):
        try:
            self.set_session()
            user = self.get_user()
            ins_manager = self.manager(self.db)
            indicted_object = ins_manager.all_data(user.id)

            if len(ins_manager.errors) == 0:
                self.respond_ajax(indicted_object, message='Operación exitosa!')
            else:
                self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al consultar')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def insert(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip

            objeto = self.manager(self.db).entity(**diccionary)
            objeto_resp = SalidaManager(self.db).insert(objeto)
            InventarioManager(self.db).descontar_productos(objeto_resp, diccionary['user'], diccionary['ip'])
            self.respond(success=True, message='Registrado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def update(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip
            obj_item = self.manager(self.db).obtain(diccionary['id'])
            objeto = self.manager(self.db).entity(**diccionary)
            InventarioManager(self.db).update_salidas(obj_item, diccionary)
            SalidaManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = SalidaManager(self.db).state(diccionary['id'], diccionary['enabled'], self.get_user_id(), self.request.remote_ip)
            msg = 'Habilitado correctamente.' if result.estado else 'Deshabilitado correctamente.'
            self.respond(success=True, message=msg)
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            SalidaManager(self.db).delete(diccionary['id'], self.get_user_id(), self.request.remote_ip)
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()
