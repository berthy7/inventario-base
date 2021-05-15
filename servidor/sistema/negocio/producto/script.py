from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        producto_m = session.query(Modulo).filter(Modulo.nombre == 'producto').first()
        if producto_m is None:
            producto_m = Modulo(titulo='Producto', ruta='/producto', nombre='producto', icono='add_shopping_cart')

        negocio_m.children.append(producto_m)

        query_producto = session.query(Modulo).filter(Modulo.nombre == 'producto_query').first()
        if query_producto is None:
            query_producto = Modulo(titulo='Consultar', ruta='', nombre='producto_query', menu=False)
        insert_producto = session.query(Modulo).filter(Modulo.nombre == 'producto_insert').first()
        if insert_producto is None:
            insert_producto = Modulo(titulo='Adicionar', ruta='/producto_insert', nombre='producto_insert', menu=False)
        update_producto = session.query(Modulo).filter(Modulo.nombre == 'producto_update').first()
        if update_producto is None:
            update_producto = Modulo(titulo='Actualizar', ruta='/producto_update', nombre='producto_update', menu=False)
        delete_producto = session.query(Modulo).filter(Modulo.nombre == 'producto_delete').first()
        if delete_producto is None:
            delete_producto = Modulo(titulo='Dar de Baja', ruta='/producto_delete', nombre='producto_delete', menu=False)

        producto_m.children.append(query_producto)
        producto_m.children.append(insert_producto)
        producto_m.children.append(update_producto)
        producto_m.children.append(delete_producto)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(producto_m)
            rol.modulos.append(query_producto)
            rol.modulos.append(insert_producto)
            rol.modulos.append(update_producto)
            rol.modulos.append(delete_producto)

        session.commit()
