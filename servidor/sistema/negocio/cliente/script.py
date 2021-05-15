from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        cliente_m = session.query(Modulo).filter(Modulo.nombre == 'cliente').first()
        if cliente_m is None:
            cliente_m = Modulo(titulo='Cliente', ruta='/cliente', nombre='cliente', icono='assignment_ind')

        negocio_m.children.append(cliente_m)

        query_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_query').first()
        if query_cliente is None:
            query_cliente = Modulo(titulo='Consultar', ruta='', nombre='cliente_query', menu=False)
        insert_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_insert').first()
        if insert_cliente is None:
            insert_cliente = Modulo(titulo='Adicionar', ruta='/cliente_insert', nombre='cliente_insert', menu=False)
        update_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_update').first()
        if update_cliente is None:
            update_cliente = Modulo(titulo='Actualizar', ruta='/cliente_update', nombre='cliente_update', menu=False)
        delete_cliente = session.query(Modulo).filter(Modulo.nombre == 'cliente_delete').first()
        if delete_cliente is None:
            delete_cliente = Modulo(titulo='Dar de Baja', ruta='/cliente_delete', nombre='cliente_delete', menu=False)

        cliente_m.children.append(query_cliente)
        cliente_m.children.append(insert_cliente)
        cliente_m.children.append(update_cliente)
        cliente_m.children.append(delete_cliente)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(cliente_m)
            rol.modulos.append(query_cliente)
            rol.modulos.append(insert_cliente)
            rol.modulos.append(update_cliente)
            rol.modulos.append(delete_cliente)

        session.commit()
