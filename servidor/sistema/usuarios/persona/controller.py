from servidor.sistema.usuarios.persona.manager import PersonaManager
from servidor.sistema.usuarios.usuario.manager import ModuloManager
from servidor.common.controllers import CrudController

import json

class PersonaController(CrudController):
    manager = PersonaManager
    html_index = "sistema/usuarios/persona/views/index.html"
    routes = {
        '/persona': {'GET': 'index'},
        '/persona_insert': {'POST': 'insert'},
        '/persona_update': {'PUT': 'edit', 'POST': 'update'},
        '/persona_delete': {'POST': 'delete_persona'},
        '/persona_list': {'POST': 'data_list'}
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
            PersonaManager(self.db).insert(objeto)

            self.respond(success=True, message='Datos registrados correctamente.')
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
            PersonaManager(self.db).update(objeto)

            self.respond(success=True, message='Datos actualizados correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))

    def delete_persona(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            id = diccionary['id']
            enable = diccionary['enabled']
            response = PersonaManager(self.db).delete(id, enable, self.get_user_id(), self.request.remote_ip)

            if response:
                msg = 'Persona habilitada correctamente.' if enable else 'Persona inhabilitada correctamente.'
                self.respond(success=True, message=msg)
            else:
                self.respond(success=False, message='No se pudo completar la acción.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
