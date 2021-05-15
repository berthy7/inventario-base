from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        user_m = session.query(Modulo).filter(Modulo.nombre == 'usuarios_mod').first()
        if user_m is None:
            user_m = Modulo(titulo='Usuarios', nombre='usuarios_mod', icono='group')

        roles_m = session.query(Modulo).filter(Modulo.nombre == 'roles').first()
        if roles_m is None:
            roles_m = Modulo(titulo='Rol', ruta='/rol', nombre='roles', icono='settings')

        user_m.children.append(roles_m)

        query_rol = session.query(Modulo).filter(Modulo.nombre == 'rol_query').first()
        if query_rol is None:
            query_rol = Modulo(titulo='Consultar', ruta='', nombre='rol_query', menu=False)
        insert_rol = session.query(Modulo).filter(Modulo.nombre == 'rol_insert').first()
        if insert_rol is None:
            insert_rol = Modulo(titulo='Adicionar', ruta='/rol_insert', nombre='rol_insert', menu=False)
        update_rol = session.query(Modulo).filter(Modulo.nombre == 'rol_update').first()
        if update_rol is None:
            update_rol = Modulo(titulo='Actualizar', ruta='/rol_update', nombre='rol_update', menu=False)
        delete_rol = session.query(Modulo).filter(Modulo.nombre == 'rol_delete').first()
        if delete_rol is None:
            delete_rol = Modulo(titulo='Dar de Baja', ruta='/rol_delete', nombre='rol_delete', menu=False)

        roles_m.children.append(query_rol)
        roles_m.children.append(insert_rol)
        roles_m.children.append(update_rol)
        roles_m.children.append(delete_rol)

        super_role = session.query(Rol).filter(Rol.nombre == 'SUPER ADMINISTRADOR').first()
        if super_role is None:
            super_role = Rol(nombre='SUPER ADMINISTRADOR', descripcion='Todos los permisos.')

        admin_role = session.query(Rol).filter(Rol.nombre == 'ADMINISTRADOR').first()
        if admin_role is None:
            admin_role = Rol(nombre='ADMINISTRADOR', descripcion='Solo permisos de administrador.')

        super_role.modulos.append(user_m)
        super_role.modulos.append(roles_m)
        super_role.modulos.append(query_rol)
        super_role.modulos.append(insert_rol)
        super_role.modulos.append(update_rol)
        super_role.modulos.append(delete_rol)

        session.add(super_role)
        session.add(admin_role)

        session.commit()
