from servidor.sistema.usuarios.rol.model import Rol
from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.usuario.model import Usuario
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager


class RolManager(SuperManager):

    def __init__(self, db):
        super().__init__(Rol, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity).all())

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/rol')
        list = []

        for item in self.db.query(self.entity).filter(self.entity.enabled):
            is_active = item.estado
            delete = 'rol_delete' in privilegios
            disable = 'disabled' if 'rol_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            list.append(diccionario)

        return list

    def get_all(self):
        items = self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled)
        return items

    def get_page(self, page_nr=1, max_entries=10, like_search=None, order_by=None, ascendant=True, query=None):
        query = self.db.query(self.entity).filter(self.entity.id > 1)
        return super().get_page(page_nr, max_entries, like_search, order_by, ascendant, query)

    def insert(self, rol):
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=rol.user, ip=rol.ip, accion="Se registró un rol.", fecha=fecha)
        super().insert(b)
        a = super().insert(rol)

        return a

    def update(self, rol):
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=rol.user, ip=rol.ip, accion="Se modificó un rol.", fecha=fecha)
        super().insert(b)
        a = super().update(rol)

        return a

    def state(self, id, estado, userid, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()

        x.estado = estado
        neg_estado = not estado
        message = "Se habilitó un rol." if estado else "Se inhabilitó un rol y usuarios relacionados."
        users = self.db.query(Usuario).filter(Usuario.estado == neg_estado).filter(Usuario.fkrol == id).all()

        for u in users:
            u.estado = estado

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
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó rol", fecha=fecha, tabla="usuarios_rol", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
