from servidor.sistema.usuarios.usuario.model import Usuario, Modulo, Acceso
from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.usuarios.rol.model import Rol
from datetime import datetime

import string
import random
import hashlib
import pytz

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class UsuarioManager(SuperManager):

    def __init__(self, db):
        super().__init__(Usuario, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity).all())

    def get_privileges(self, id, route):
        parent_module = self.db.query(Modulo).join(Rol.modulos).join(Usuario).filter(Modulo.ruta == route).filter(Usuario.id == id).filter(Usuario.estado).filter(Usuario.enabled).first()

        if not parent_module:
            return dict()

        modules = self.db.query(Modulo).join(Rol.modulos).join(Usuario).filter(Modulo.fkmodulo == parent_module.id).filter(Usuario.id == id).filter(Usuario.estado).filter(Usuario.enabled)
        privileges = {parent_module.nombre: parent_module}

        for module in modules:
            privileges[module.nombre] = module

        return privileges

    def get_page(self, page_nr=1, max_entries=10, like_search=None, order_by=None, ascendant=True, query=None):
        query = self.db.query(self.entity).join(Rol).filter(Rol.id > 1)
        return super().get_page(page_nr, max_entries, like_search, order_by, ascendant, query)

    def get_by_id(self, id):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).filter(self.entity.id == id).first()

    def get_by_password(self, idu, password):
        return self.db.query(self.entity).filter(self.entity.id == idu).filter(self.entity.password == hashlib.sha512(str(password).encode()).hexdigest()).first()

    def get_random_string(self):
        random_list = []

        for i in range(8):
            random_list.append(random.choice(string.ascii_uppercase + string.digits))

        return ''.join(random_list)

    def obtener_diccionario_usuario(self, id):
        usuario = self.db.query(Usuario).filter(Usuario.id == id).first()

        if usuario.fkpersona:
            nombre = usuario.persona.fullname
            email = usuario.persona.email

            persona = {'id': usuario.persona.id, 'nombre': usuario.persona.nombre, 'apellido': usuario.persona.apellido, 'fullname': usuario.persona.fullname,
                        'ci': usuario.persona.ci, 'email': usuario.persona.email, 'enabled': usuario.persona.enabled}
        else:
            persona = None
            nombre = "---------"
            email = "---------"

    def insert(self, diccionary):
        usuario = UsuarioManager(self.db).entity(**diccionary)
        user = self.db.query(Usuario).filter(Usuario.username == usuario.username).first()

        if user:
            return dict(response=None, success=False, message="Ya se le creo un usuario al personal")
        else:
            usuario.password = hashlib.sha512(usuario.password.encode()).hexdigest()
            codigo = self.get_random_string()
            Usuario.codigo = codigo
            _objeto = super().insert(usuario)
            fecha = BitacoraManager(self.db).fecha_actual()
            b = Bitacora(fkusuario=usuario.user_id, ip=usuario.ip, accion="Se registró un usuario.", fecha=fecha, identificador=_objeto.id)
            super().insert(b)
            _dict = _objeto.get_dict()
            return dict(response=_dict, success=True, message="Insertado correctamente")

    def update(self, usuario):
        if not usuario.password or usuario.password == '':
            usuario.password = (self.db.query(Usuario.password).filter(Usuario.id == usuario.id).first())[0]
        else:
            usuario.password = hashlib.sha512(usuario.password.encode()).hexdigest()

        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().update(usuario)
        b = Bitacora(fkusuario=usuario.user_id, ip=usuario.ip, accion="Modificó Usuario.", fecha=fecha, tabla="cb_usuarios_usuario", identificador=a.id)
        super().insert(b)

        return a

    def state(self, id, estado, userid, ip):
        x = self.db.query(Usuario).filter(Usuario.id == id).one()

        if estado:
            r = self.db.query(Rol).filter(Rol.id == x.fkrol).one()
            if r.estado and r.enabled:
                x.estado = estado
            else:
                return False
            message = "Se habilitó un usuario."
        else:
            x.estado = estado
            message = "Se inhabilitó un usuario."

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=userid, ip=ip, accion=message, fecha=fecha)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return True

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó usuario", fecha=fecha, tabla="usuarios_usuario", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def all_data(self, idu):
        privilegios = self.get_privileges(idu, '/usuario')
        datos = self.db.query(self.entity).filter(self.entity.id != 1).filter(self.entity.enabled).all()
        user = self.db.query(Usuario).filter(Usuario.id == idu).first()
        list = []

        for item in datos:
            disable = 'disabled' if 'usuario_update' not in privilegios else ''
            delete = 'usuario_delete' in privilegios
            person = item.persona.fullname if item.persona else ''
            rol = item.rol.nombre if item.rol else ''
            estado = 'Activo' if item.estado else 'Inactivo'
            check = 'checked' if item.estado else ''
            updpass = user.rol.nombre == 'SUPER ADMINISTRADOR'

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['updpass'] = updpass
            diccionario['nombre'] = person
            diccionario['rol'] = rol

            list.append(diccionario)

        return list

    def user_exist(self, email):
        usuario = self.db.query(self.entity).filter(self.entity.enabled).filter(self.entity.username == email).first()

        if usuario:
            return True

    def update_password(self, user):
        user.password = hashlib.sha512(user.password.encode()).hexdigest()
        return super().update(user)

    def has_access(self, id, route):
        aux = self.db.query(Usuario.id).join(Rol).join(Acceso).join(Modulo).filter(Usuario.id == id).filter(Modulo.ruta == route).filter(Usuario.estado).filter(Usuario.enabled).all()

        return len(aux) != 0


class ModuloManager:

    def __init__(self, db):
        self.db = db

    def list_all(self):
        return self.db.query(Modulo).filter(Modulo.fkmodulo == None)
