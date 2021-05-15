from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.common.controllers import CrudController

class BitacoraController(CrudController):
    manager = BitacoraManager
    html_index = "sistema/usuarios/bitacora/views/index.html"
    routes = {
        '/bitacora': {'GET': 'index'},
        '/bitacora_list': {'POST': 'data_list'}
    }

    def data_list(self):
        try:
            self.set_session()
            user = self.get_user()
            ins_manager = self.manager(self.db)
            indicted_object = ins_manager.all_data(user.id)

            if len(ins_manager.errors) == 0:
                self.respond_ajax(indicted_object, message='Lista recuperada correctamente.')
            else:
                self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al consultar')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()
