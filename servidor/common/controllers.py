from tornado.web import RequestHandler, HTTPError
from servidor.database.connection import get_session
from servidor.sistema.usuarios.login.manager import LoginManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from tornado.web import authenticated
from tornado.gen import coroutine
from servidor.common.utils import decorators

import traceback
import json


class Error404Handler(RequestHandler):

    def prepare(self):
        self.set_status(404)
        self.render("common/views/error.html", error_code='404',  message="Página no encontrada", url_redirect='/')


class SuperController(RequestHandler):
    """Utilice esta clase para factorizar metodos comunes de entre los controladores."""
    def set_session(self):
        if not hasattr(self, 'db'):
            self.db = get_session()

    def delete_session(self):
        if hasattr(self, 'db'):
            self.db.close()

    def get_user_id(self):
        return int(self.get_current_user())

    def get_user_token(self):
        return str(self.get_current_token())

    def get_user(self):
        return LoginManager().get(self.get_user_id())

    def get_persona(self,fkpersona):
        return LoginManager().obtener_persona(fkpersona)

    def set_user_id(self, user_id):
        self.set_secure_cookie('user', str(user_id))

    def set_user_token(self, token):
        self.set_secure_cookie('token', str(token))

    def set_user_conexion(self, conex):
        self.clear_cookie('conexion')
        self.set_secure_cookie('conexion', str(conex))

    def get_current_user(self):
        """Sobrecarga del metodo `get_current_user()`"""
        return self.get_secure_cookie("user")

    def get_current_conexion(self):
        """Sobrecarga del metodo `get_current_conexion()`"""
        return self.get_secure_cookie("conexion")

    def get_current_token(self):
        """Sobrecarga del metodo `get_current_conexion()`"""
        return self.get_secure_cookie("token")

    def respond(self, response=None, success=True, message=""):
        """Retorna al cliente invocador un respuesta estándar serializada con json."""
        if not response and not success:
            response = traceback.format_exc()

        self.write(json.dumps({"response": response, 'success': success, 'message': message}))

    def respond_ajax(self, response=None, success=True, message=""):
        """Retorna al cliente invocador un respuesta estándar serializada con json."""
        if not response and not success:
            response = traceback.format_exc()
            print(response)
        self.write(json.dumps({"data": response}))
        self.set_header('Content-Type', 'application/json')

    def get(self):
        """Prueba del json, solo para api controllers.
        Quitar este método en producción.
        """
        self.post()

    def write_error(self, status_code, **kwargs):
        self.render("common/views/error.html", error_code=status_code, message=kwargs.get('message', 'Error interno del servidor'), url_redirect='/')


class MethodDispatcher(SuperController):
    routes = {}

    def no_method(self):
        raise HTTPError(401)

    def get(self):
        getattr(self, self.routes[self.request.uri.split("?")[0]].get('GET', 'no_method'))()

    def post(self):
        getattr(self, self.routes[self.request.uri.split("?")[0]].get('POST', 'no_method'))()

    def put(self):
        getattr(self, self.routes[self.request.uri.split("?")[0]].get('PUT', 'no_method'))()


class CrudController(MethodDispatcher):
    routes = {}
    html_index = None
    manager = None

    @decorators(authenticated, coroutine)
    def get(self):
        super().get()

    @decorators(authenticated, coroutine)
    def post(self):
        self.check_xsrf_cookie()
        super().post()

    def index(self):
        self.set_session()
        self.verif_privileges()
        result = self.manager(self.db).list_all()
        result['user'] = self.get_user()
        result['privileges'] = UsuarioManager(self.db).get_privileges(self.get_user_id(), self.request.uri)
        result.update(self.get_extra_data())
        self.render(self.html_index, **result)
        self.db.close()

    def edit(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        indicted_object = ins_manager.obtain(diccionary['id'])

        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Operación exitosa!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def insert(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        object = ins_manager.entity(**diccionary)
        indicted_object = ins_manager.insert(object)

        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Insertado correctamente!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al insertar')
        self.db.close()

    def update(self):
        self.set_session()
        self.verif_privileges()
        ins_manager = self.manager(self.db)
        diccionary = json.loads(self.get_argument("object"))
        object = ins_manager.entity(**diccionary)
        indicted_object = ins_manager.update(object)

        if len(ins_manager.errors) == 0:
            self.respond(indicted_object.get_dict(), message='Actualizado correctamente!')
        else:
            self.respond([item.__dict__ for item in ins_manager.errors], False, 'Ocurrió un error al actualizar')
        self.db.close()

    def change_state(self):
        self.set_session()
        self.verif_privileges()
        id = json.loads(self.get_argument("id"))
        state = json.loads(self.get_argument("enabled"))
        updated_object = self.manager(self.db).change_state(id, state)

        if state:
            message = "Dado de Alta!"
        else:
            message = "Dado de Baja!"
        self.respond(updated_object.get_dict(), message=message)
        self.db.close()

    def verif_privileges(self):
        if not UsuarioManager(self.db).has_access(self.get_user_id(), self.request.uri.split("?")[0]):
            raise HTTPError(401)

    def set_session(self):
        if not hasattr(self, 'db'):
            self.db = get_session()

    def delete_session(self):
        if hasattr(self, 'db'):
            self.db.close()

    def get_extra_data(self):
        usuario = self.get_user()

        if usuario:
            return dict(usuario=usuario)
        else:
            return {}


class ApiController(MethodDispatcher):

    def no_method(self):
        """lanza un error cuando no encuentra el metodo"""
        raise HTTPError(401)

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', self.request.headers.get('Origin', '*'))

    def check_xsrf_cookie(self):
        return

    @coroutine
    def get(self):
        getattr(self, self.routes[self.request.uri.split("?")[0]].get('GET', 'no_method'))()

    @coroutine
    def post(self):
        getattr(self, self.routes[self.request.uri.split("?")[0]].get('POST', 'no_method'))()
