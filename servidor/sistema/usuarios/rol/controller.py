from servidor.sistema.usuarios.rol.manager import RolManager
from servidor.sistema.usuarios.usuario.manager import ModuloManager
from servidor.common.controllers import CrudController

import json


class RolController(CrudController):
    manager = RolManager
    html_index = "sistema/usuarios/rol/views/index.html"
    routes = {
        '/rol': {'GET': 'index'},
        '/rol_insert': {'POST': 'insert'},
        '/rol_update': {'PUT': 'edit', 'POST': 'update'},
        '/rol_state': {'POST': 'state'},
        '/rol_delete': {'POST': 'delete'},
        '/rol_list': {'POST': 'data_list'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        aux['modulos'] = ModuloManager(self.db).list_all()

        return aux

    def data_list(self):
        try:
            self.set_session()
            idu = self.get_user_id()
            ins_manager = self.manager(self.db)
            indicted_object = ins_manager.all_data(idu)

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
            RolManager(self.db).insert(objeto)

            self.respond(success=True, message='Insertado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))

    def update(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['user'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip
            objeto = self.manager(self.db).entity(**diccionary)
            RolManager(self.db).update(objeto)

            self.respond(success=True, message='Modificado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            id = diccionary['id']
            estado = diccionary['estado']
            response = RolManager(self.db).state(id, estado, self.get_user_id(), self.request.remote_ip)

            if response:
                msg = 'Rol habilitado correctamente.' if estado else 'Rol inhabilitado correctamente.'
                self.respond(success=True, message=msg)
            else:
                self.respond(response=None, success=False, message='No se pudo completar la acción.')
        except Exception as e:
            print(e)
            self.respond(response=None, success=False, message=str(e))

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            self.manager(self.db).delete(diccionary['id'], self.get_user_id(), self.request.remote_ip)
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
