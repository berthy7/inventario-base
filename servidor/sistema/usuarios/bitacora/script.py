from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol

def insertions():
    with transaction() as session:
        user_m = session.query(Modulo).filter(Modulo.nombre == 'usuarios_mod').first()
        if user_m is None:
            user_m = Modulo(titulo='Usuarios', nombre='usuarios_mod', icono='group')

        bitacora_m = session.query(Modulo).filter(Modulo.nombre == 'bitacora').first()
        if bitacora_m is None:
            bitacora_m = Modulo(titulo='Bitácora', ruta='/bitacora', nombre='bitacora', icono='library_books')

        user_m.children.append(bitacora_m)

        query_bitacora = session.query(Modulo).filter(Modulo.nombre == 'bitacora_query').first()
        if query_bitacora is None:
            query_bitacora = Modulo(titulo='Consultar', ruta='', nombre='bitacora_query', menu=False)

        bitacora_m.children.append(query_bitacora)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', 'ADMINISTRADOR'])).all()

        for rol in roles:
            rol.modulos.append(user_m)
            rol.modulos.append(bitacora_m)
            rol.modulos.append(query_bitacora)

        session.commit()
