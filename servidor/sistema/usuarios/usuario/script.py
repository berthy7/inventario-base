from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Usuario, Modulo
from servidor.sistema.usuarios.rol.model import Rol

import hashlib


def insertions():
    with transaction() as session:
        user_m = session.query(Modulo).filter(Modulo.nombre == 'usuarios_mod').first()
        if user_m is None:
            user_m = Modulo(titulo='Usuarios', nombre='usuarios_mod', icono='group')

        usuarios_m = session.query(Modulo).filter(Modulo.nombre == 'usuario').first()
        if usuarios_m is None:
            usuarios_m = Modulo(titulo='Usuario', ruta='/usuario', nombre='usuario', icono='person')

        perfil_m = session.query(Modulo).filter(Modulo.nombre == 'perfil').first()
        if perfil_m is None:
            perfil_m = Modulo(titulo='Perfil Usuario', ruta='/usuario_profile', nombre='perfil', icono='account_box')

        user_m.children.append(usuarios_m)
        user_m.children.append(perfil_m)

        query_usuario = session.query(Modulo).filter(Modulo.nombre == 'usuario_query').first()
        if query_usuario is None:
            query_usuario = Modulo(titulo='Consultar', ruta='', nombre='usuario_query', menu=False)
        insert_usuario = session.query(Modulo).filter(Modulo.nombre == 'usuario_insert').first()
        if insert_usuario is None:
            insert_usuario = Modulo(titulo='Adicionar', ruta='/usuario_insert', nombre='usuario_insert', menu=False)
        update_usuario = session.query(Modulo).filter(Modulo.nombre == 'usuario_update').first()
        if update_usuario is None:
            update_usuario = Modulo(titulo='Actualizar', ruta='/usuario_update', nombre='usuario_update', menu=False)
        delete_usuario = session.query(Modulo).filter(Modulo.nombre == 'usuario_delete').first()
        if delete_usuario is None:
            delete_usuario = Modulo(titulo='Dar de Baja', ruta='/usuario_delete', nombre='usuario_delete', menu=False)

        usuarios_m.children.append(query_usuario)
        usuarios_m.children.append(insert_usuario)
        usuarios_m.children.append(update_usuario)
        usuarios_m.children.append(delete_usuario)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(user_m)
            rol.modulos.append(usuarios_m)
            rol.modulos.append(perfil_m)
            rol.modulos.append(query_usuario)
            rol.modulos.append(insert_usuario)
            rol.modulos.append(update_usuario)
            rol.modulos.append(delete_usuario)

        super_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()
        super_user = session.query(Usuario).filter(Usuario.username == 'admin').first()

        if super_user is None:
            hex_dig = hashlib.sha512(b'ProBase2020').hexdigest()
            super_user = Usuario(username='admin', password=hex_dig)
            super_user.rol = super_role

        session.add(super_user)
        session.commit()
