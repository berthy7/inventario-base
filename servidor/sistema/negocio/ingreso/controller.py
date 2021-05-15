from servidor.common.controllers import CrudController
from servidor.sistema.negocio.sucursal.manager import SucursalManager
from servidor.sistema.negocio.producto.manager import ProductoManager
from servidor.sistema.negocio.inventario.manager import InventarioManager
from servidor.sistema.negocio.ingreso.manager import IngresoManager

import json


class IngresoController(CrudController):
    manager = IngresoManager
    html_index = "sistema/negocio/ingreso/views/index.html"

    routes = {
        '/ingreso': {'GET': 'index', 'POST': 'table'},
        '/ingreso_insert': {'POST': 'insert'},
        '/ingreso_update': {'PUT': 'edit', 'POST': 'update'},
        '/ingreso_state': {'POST': 'state'},
        '/ingreso_delete': {'POST': 'delete'},
        '/ingreso_list': {'POST': 'data_list'},
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        us = self.get_user()
        aux['sucursales'] = SucursalManager(self.db).listar_habilitados()
        aux['productos'] = ProductoManager(self.db).listar_habilitados()

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
            objeto_ingreso = IngresoManager(self.db).insert(objeto)
            InventarioManager(self.db).actualizar_productos(objeto_ingreso, diccionary['user'], diccionary['ip'])
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
            InventarioManager(self.db).update_ingresos(obj_item, diccionary)
            IngresoManager(self.db).update(objeto)
            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            result = IngresoManager(self.db).state(diccionary['id'], diccionary['estado'], self.get_user_id(), self.request.remote_ip)

            if result:
                msg = 'Habilitado correctamente.' if result.estado else 'Deshabilitado correctamente.'
                self.respond(success=True, message=msg)
            else:
                self.respond(success=False, message='ERROR 403')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            self.manager(self.db).delete(diccionary['id'], self.get_user_id(), self.request.remote_ip)
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
