from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        ingreso_m = session.query(Modulo).filter(Modulo.nombre == 'ingreso').first()
        if ingreso_m is None:
            ingreso_m = Modulo(titulo='Nota de Ingreso', ruta='/ingreso', nombre='ingreso', icono='addchart')

        negocio_m.children.append(ingreso_m)

        query_ingreso = session.query(Modulo).filter(Modulo.nombre == 'ingreso_query').first()
        if query_ingreso is None:
            query_ingreso = Modulo(titulo='Consultar', ruta='', nombre='ingreso_query', menu=False)
        insert_ingreso = session.query(Modulo).filter(Modulo.nombre == 'ingreso_insert').first()
        if insert_ingreso is None:
            insert_ingreso = Modulo(titulo='Adicionar', ruta='/ingreso_insert', nombre='ingreso_insert', menu=False)
        update_ingreso = session.query(Modulo).filter(Modulo.nombre == 'ingreso_update').first()
        if update_ingreso is None:
            update_ingreso = Modulo(titulo='Actualizar', ruta='/ingreso_update', nombre='ingreso_update', menu=False)
        delete_ingreso = session.query(Modulo).filter(Modulo.nombre == 'ingreso_delete').first()
        if delete_ingreso is None:
            delete_ingreso = Modulo(titulo='Dar de Baja', ruta='/ingreso_delete', nombre='ingreso_delete', menu=False)

        ingreso_m.children.append(query_ingreso)
        ingreso_m.children.append(insert_ingreso)
        ingreso_m.children.append(update_ingreso)
        ingreso_m.children.append(delete_ingreso)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(ingreso_m)
            rol.modulos.append(query_ingreso)
            rol.modulos.append(insert_ingreso)
            rol.modulos.append(update_ingreso)
            rol.modulos.append(delete_ingreso)

        session.commit()
