from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.login.manager import LoginManager
from servidor.sistema.usuarios.rol.manager import RolManager
from servidor.sistema.usuarios.persona.manager import PersonaManager
from servidor.common.controllers import CrudController, SuperController
from datetime import datetime
from tornado.gen import coroutine
from servidor.database.connection import transaction
from more_itertools import one

import json
import pytz


class UsuarioController(CrudController):
    manager = UsuarioManager
    html_index = "sistema/usuarios/usuario/views/index.html"
    routes = {
        '/usuario': {'GET': 'index'},
        '/usuario_insert': {'POST': 'insert'},
        '/usuario_update': {'PUT': 'edit', 'POST': 'update'},
        '/usuario_state': {'POST': 'state'},
        '/usuario_delete': {'POST': 'delete'},
        '/usuario_list': {'POST': 'data_list'},
        '/usuario_modify_password': {'POST': 'update_password'},
        '/usuario_autenticacion': {'PUT': 'usuario_autenticacion'},
        '/usuario_update_profile': {'POST': 'user_update_profile'},
        '/usuario_update_credential': {'POST': 'user_update_credential'},
        '/usuario_profile': {'GET': 'usuario_profile'},
        '/usuario_file': {'POST': 'upload_file'}
    }

    def get_extra_data(self):
        aux = super().get_extra_data()
        user = self.get_user()
        aux['roles'] = RolManager(self.db).get_all()

        return aux

    def usuario_profile(self):
        user = self.get_user()
        self.set_session()
        result = self.manager(self.db).obtain(user.id)
        self.render("sistema/usuarios/usuario/views/profile.html", usuario=user, dtuser=result)
        self.db.close()

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
            username_reg = UsuarioManager(self.db).user_exist(diccionary['persona']['email'])

            if username_reg:
                self.respond(response=None, success=False, message='El nombre de usuario ya fue registrado, por favor ingresa otro.')
                return

            diccionary['user_id'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip
            UsuarioManager(self.db).insert(diccionary)

            self.respond(success=True, message='Usuario registrado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))

    def update(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            user_info = self.manager(self.db).get_by_id(diccionary['id'])
            username_reg = UsuarioManager(self.db).user_exist(diccionary['persona']['email'])

            if user_info.persona and user_info.persona.email != diccionary['persona']['email']:
                if username_reg:
                    self.respond(response=None, success=False, message='El nombre de usuario ya fue registrado, por favor ingresa otro.')
                    return

            diccionary['user_id'] = self.get_user_id()
            diccionary['ip'] = self.request.remote_ip
            objeto = self.manager(self.db).entity(**diccionary)
            UsuarioManager(self.db).update(objeto)

            self.respond(success=True, message='Usuario actualizado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))

    def state(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            id = diccionary['id']
            estado = diccionary['estado']
            resp = UsuarioManager(self.db).state(id, estado, self.get_user_id(), self.request.remote_ip)

            if resp:
                msg = 'Usuario habilitado correctamente.'if estado else 'Usuario inhabilitado correctamente.'
                self.respond(success=True, message=msg)
            else:
                msg = 'Rol asignado dado de baja, no es posible habilitar el usuario.'
                self.respond(success=False, message=msg)
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))

    def delete(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            self.manager(self.db).delete(diccionary['id'], self.get_user_id(), self.request.remote_ip)
            self.respond(success=True, message='Eliminado correctamente.')
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))

    def usuario_autenticacion(self):
        self.set_session()
        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        password = diccionary['password']
        user = LoginManager().login(username, password)

        if user:
            self.respond(success=True)
        else:
            self.respond(success=False, message='Datos incorrectos.')
        self.db.close()

    def user_update_profile(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            diccionary['ip'] = self.request.remote_ip
            objeto = PersonaManager(self.db).entity(**diccionary)
            person = PersonaManager(self.db).update(objeto)

            if person:
                self.respond(message="Datos modificados correctamente.", success=True)
            else:
                self.respond(message="No se pudo realizar la acción.", success=False)
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def user_update_credential(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))
            user = self.manager(self.db).get_by_password(self.get_user_id(), diccionary['old_password'])

            if user:
                if diccionary['new_password'] == diccionary['new_rpassword']:
                    user.username = diccionary['username']
                    user.password = diccionary['new_password']
                    self.manager(self.db).update_password(user)
                    self.respond(message="Contraseña cambiada correctamente ", success=True)
                else:
                    self.respond(message="Datos incorrectos", success=False)
            else:
                self.respond(message="Datos incorrectos", success=False)
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def update_password(self):
        try:
            self.set_session()
            diccionary = json.loads(self.get_argument("object"))

            if diccionary['new_password'] == diccionary['new_rpassword']:
                user = self.manager(self.db).get_by_id(diccionary['id'])
                user.password = diccionary['new_password']
                self.manager(self.db).update_password(user)
                self.respond(message="Contraseña cambiada correctamente ", success=True)
            else:
                self.respond(message="Datos incorrectos", success=False)
        except Exception as e:
            print(e)
            self.respond(response=[], success=False, message=str(e))
        self.db.close()

    def fecha_actual(self):
        fzona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha_str = fzona.strftime('%Y-%m-%d %H:%M:%S.%f')
        dtm_fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')

        return dtm_fecha

    def upload_file(self):
        try:
            self.set_session()
            response = None

            if "file" in self.request.files:
                fileinfo = one(self.request.files["file"])
                response = self.manager(self.db).imagen(fileinfo)

            if response is not None:
                self.respond(response=response, success=True, message='Imagen subida correctamente.')
            else:
                self.respond(response=None, success=False, message='Error al subir la imagen.')
        except Exception as e:
            print(e)
            self.respond(response=None, success=False, message=str(e))


class ManualController(SuperController):

    @coroutine
    def get(self):
        usuario = self.get_user()
        with transaction() as db:
            self.render("usuarios/usuario/views/manual.html", user=usuario)
