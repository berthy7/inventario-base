from servidor.sistema.usuarios.persona.model import Persona
from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.usuarios.usuario.model import Usuario
from servidor.sistema.usuarios.rol.model import Rol
from more_itertools import one


class PersonaManager(SuperManager):

    def __init__(self, db):
        super().__init__(Persona, db)

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled == True))

    def get_all(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).all()

    def get_by_id(self, id):
        return self.db.query(self.entity).filter(self.entity.enabled == True).filter(self.entity.id == id).first()

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/persona')
        list = []

        for objeto in self.db.query(Persona).all():
            disable = 'disabled' if 'persona_update' not in privilegios else ''
            estado = 'Activo' if objeto.enabled else 'Inactivo'
            check = 'checked' if objeto.enabled else ''

            diccionario = objeto.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            list.append(diccionario)

        return list

    def get_all_by_lastname(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.apellidopaterno.asc()).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled == True).order_by(self.entity.apellido.asc()).all()

    def insert_person(self, personadt):
        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=personadt.user, ip=personadt.ip, accion="Se registró una persona.", fecha=fecha, tabla="usuarios_persona")
        super().insert(personadt)
        super().insert(b)

        return dict(respuesta=True, Mensaje="Insertado correctamente", data=personadt.id)

    def update(self, persona):
        fecha = BitacoraManager(self.db).fecha_actual()
        a = super().update(persona)
        b = Bitacora(fkusuario=persona.user, ip=persona.ip, accion="Modificó persona.", fecha=fecha, tabla="usuarios_persona", identificador=a.id)
        super().insert(b)

        return a

    def delete(self, id, estado, user, ip):
        x = self.db.query(Persona).filter(Persona.id == id).one()
        message = "Habilitó persona."if estado else "Inhabilitó persona."
        x.enabled = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=message, fecha=fecha, tabla="usuarios_persona")
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

        return True
