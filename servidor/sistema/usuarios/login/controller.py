from servidor.sistema.usuarios.login.manager import LoginManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.common.controllers import SuperController
from tornado.gen import coroutine
from servidor.database.connection import transaction
from datetime import datetime

import json
import pytz


class LoginController(SuperController):

    @coroutine
    def get(self):
        """Renderiza el login"""
        self.set_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.set_header('Pragma', 'no-cache')
        self.set_header('Expires', '0')
        usuario = self.get_secure_cookie("user")

        if usuario:
            self.redirect("/")
        else:
            self.clear_cookie("user")
            self.render("sistema/usuarios/login/views/index.html", error=0)

    @coroutine
    def post(self):
        """Inicia sesión en la aplicación.
        Si se inicia sesión con éxito enctonces se guarda el
        usuario en la cookie caso contrario se vuelve al login.
        """
        self.check_xsrf_cookie()
        ip = self.request.remote_ip

        diccionary = json.loads(self.get_argument("object"))
        username = diccionary['username']
        password = diccionary['password']

        with transaction() as db:
            pass

        if username is not None and password is not None:
            user = LoginManager().login(username, password)

            if user:
                fecha = self.fecha_actual()
                b = Bitacora(fkusuario=user.id, ip=ip, accion="Inicio de sesión.", fecha=fecha)
                self.insertar_bitacora(b)
                self.set_user_id(user.id)
                self.respond(success=True, message='Sesión iniciada correctamente.')
            else:
                userb = LoginManager().not_enabled(username, password)

                if userb:
                    self.render("sistema/usuarios/login/views/index.html", error=1)
                else:
                    self.render("sistema/usuarios/login/views/index.html", error=2)
        else:
            self.render("sistema/usuarios/login/views/index.html", error=0)

    def fecha_actual(self):
        fzona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha_str = fzona.strftime('%Y-%m-%d %H:%M:%S.%f')
        dtm_fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')

        return dtm_fecha

    def insertar_bitacora(self, bitacora):
        with transaction() as session:
            session.add(bitacora)
            session.commit()


class AutenticacionController(SuperController):

    @coroutine
    def get(self):
        usuario = self.get_user()
        with transaction() as db:
            self.render("usuarios/usuario/views/manual.html", user=usuario)


class LogoutController(SuperController):

    @coroutine
    def get(self):
        try:
            user_id = self.get_user_id()
            ip = self.request.remote_ip
            fecha = self.fecha_actual()
            b = Bitacora(fkusuario=user_id, ip=ip, accion="Finalizó sesión.", fecha=fecha)
            self.insertar_bitacora(b)
            self.clear_cookie('user')
            self.redirect(self.get_argument("next", "/"))
        except Exception as e:
            self.clear_cookie('user')
            self.redirect(self.get_argument("next", "/"))

    def fecha_actual(self):
        fzona = datetime.now(pytz.timezone('America/La_Paz'))
        fecha_str = fzona.strftime('%Y-%m-%d %H:%M:%S.%f')
        dtm_fecha = datetime.strptime(fecha_str, '%Y-%m-%d %H:%M:%S.%f')

        return dtm_fecha

    def insertar_bitacora(self, bitacora):
        with transaction() as session:
            session.add(bitacora)
            session.commit()


class ApiLoginController(SuperController):

    @coroutine
    def post(self):
        """Devuelve el usuario que coincida con el username y password dados.

        Si ocurre algún error se retornará None en la respuesta json al
        cliente invocador.
        """
        try:
            username = self.get_argument('username')
            password = self.get_argument('password')
            usuario = LoginManager().login(username, password)
            self.respond(usuario.get_dict())
        except:
            self.respond(success=False)
