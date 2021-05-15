from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        inventario_m = session.query(Modulo).filter(Modulo.nombre == 'inventario').first()
        if inventario_m is None:
            inventario_m = Modulo(titulo='Inventario', ruta='/inventario', nombre='inventario', icono='assignment')

        negocio_m.children.append(inventario_m)

        query_inventario = session.query(Modulo).filter(Modulo.nombre == 'inventario_query').first()
        if query_inventario is None:
            query_inventario = Modulo(titulo='Consultar', ruta='', nombre='inventario_query', menu=False)
        insert_inventario = session.query(Modulo).filter(Modulo.nombre == 'inventario_insert').first()
        if insert_inventario is None:
            insert_inventario = Modulo(titulo='Adicionar', ruta='/inventario_insert', nombre='inventario_insert', menu=False)
        update_inventario = session.query(Modulo).filter(Modulo.nombre == 'inventario_update').first()
        if update_inventario is None:
            update_inventario = Modulo(titulo='Actualizar', ruta='/inventario_update', nombre='inventario_update', menu=False)
        delete_inventario = session.query(Modulo).filter(Modulo.nombre == 'inventario_delete').first()
        if delete_inventario is None:
            delete_inventario = Modulo(titulo='Dar de Baja', ruta='/inventario_delete', nombre='inventario_delete', menu=False)

        inventario_m.children.append(query_inventario)
        inventario_m.children.append(insert_inventario)
        inventario_m.children.append(update_inventario)
        inventario_m.children.append(delete_inventario)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(inventario_m)
            rol.modulos.append(query_inventario)
            rol.modulos.append(insert_inventario)
            rol.modulos.append(update_inventario)
            rol.modulos.append(delete_inventario)

        session.commit()
