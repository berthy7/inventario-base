from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        traspaso_m = session.query(Modulo).filter(Modulo.nombre == 'traspaso').first()
        if traspaso_m is None:
            traspaso_m = Modulo(titulo='Nota de Traspaso', ruta='/traspaso', nombre='traspaso', icono='compare_arrows')

        negocio_m.children.append(traspaso_m)

        query_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_query').first()
        if query_traspaso is None:
            query_traspaso = Modulo(titulo='Consultar', ruta='', nombre='traspaso_query', menu=False)
        insert_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_insert').first()
        if insert_traspaso is None:
            insert_traspaso = Modulo(titulo='Adicionar', ruta='/traspaso_insert', nombre='traspaso_insert', menu=False)
        update_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_update').first()
        if update_traspaso is None:
            update_traspaso = Modulo(titulo='Actualizar', ruta='/traspaso_update', nombre='traspaso_update', menu=False)
        delete_traspaso = session.query(Modulo).filter(Modulo.nombre == 'traspaso_delete').first()
        if delete_traspaso is None:
            delete_traspaso = Modulo(titulo='Dar de Baja', ruta='/traspaso_delete', nombre='traspaso_delete', menu=False)

        traspaso_m.children.append(query_traspaso)
        traspaso_m.children.append(insert_traspaso)
        traspaso_m.children.append(update_traspaso)
        traspaso_m.children.append(delete_traspaso)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(traspaso_m)
            rol.modulos.append(query_traspaso)
            rol.modulos.append(insert_traspaso)
            rol.modulos.append(update_traspaso)
            rol.modulos.append(delete_traspaso)

        session.commit()
