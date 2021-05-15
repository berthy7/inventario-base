from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        sucursal_m = session.query(Modulo).filter(Modulo.nombre == 'sucursal').first()
        if sucursal_m is None:
            sucursal_m = Modulo(titulo='Sucursal', ruta='/sucursal', nombre='sucursal', icono='add_business')

        negocio_m.children.append(sucursal_m)

        query_sucursal = session.query(Modulo).filter(Modulo.nombre == 'sucursal_query').first()
        if query_sucursal is None:
            query_sucursal = Modulo(titulo='Consultar', ruta='', nombre='sucursal_query', menu=False)
        insert_sucursal = session.query(Modulo).filter(Modulo.nombre == 'sucursal_insert').first()
        if insert_sucursal is None:
            insert_sucursal = Modulo(titulo='Adicionar', ruta='/sucursal_insert', nombre='sucursal_insert', menu=False)
        update_sucursal = session.query(Modulo).filter(Modulo.nombre == 'sucursal_update').first()
        if update_sucursal is None:
            update_sucursal = Modulo(titulo='Actualizar', ruta='/sucursal_update', nombre='sucursal_update', menu=False)
        delete_sucursal = session.query(Modulo).filter(Modulo.nombre == 'sucursal_delete').first()
        if delete_sucursal is None:
            delete_sucursal = Modulo(titulo='Dar de Baja', ruta='/sucursal_delete', nombre='sucursal_delete', menu=False)

        sucursal_m.children.append(query_sucursal)
        sucursal_m.children.append(insert_sucursal)
        sucursal_m.children.append(update_sucursal)
        sucursal_m.children.append(delete_sucursal)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(sucursal_m)
            rol.modulos.append(query_sucursal)
            rol.modulos.append(insert_sucursal)
            rol.modulos.append(update_sucursal)
            rol.modulos.append(delete_sucursal)

        session.commit()
