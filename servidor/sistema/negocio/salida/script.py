from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        salida_m = session.query(Modulo).filter(Modulo.nombre == 'salida').first()
        if salida_m is None:
            salida_m = Modulo(titulo='Nota de Salida', ruta='/salida', nombre='salida', icono='article')

        negocio_m.children.append(salida_m)

        query_salida = session.query(Modulo).filter(Modulo.nombre == 'salida_query').first()
        if query_salida is None:
            query_salida = Modulo(titulo='Consultar', ruta='', nombre='salida_query', menu=False)
        insert_salida = session.query(Modulo).filter(Modulo.nombre == 'salida_insert').first()
        if insert_salida is None:
            insert_salida = Modulo(titulo='Adicionar', ruta='/salida_insert', nombre='salida_insert', menu=False)
        update_salida = session.query(Modulo).filter(Modulo.nombre == 'salida_update').first()
        if update_salida is None:
            update_salida = Modulo(titulo='Actualizar', ruta='/salida_update', nombre='salida_update', menu=False)
        delete_salida = session.query(Modulo).filter(Modulo.nombre == 'salida_delete').first()
        if delete_salida is None:
            delete_salida = Modulo(titulo='Dar de Baja', ruta='/salida_delete', nombre='salida_delete', menu=False)

        salida_m.children.append(query_salida)
        salida_m.children.append(insert_salida)
        salida_m.children.append(update_salida)
        salida_m.children.append(delete_salida)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(salida_m)
            rol.modulos.append(query_salida)
            rol.modulos.append(insert_salida)
            rol.modulos.append(update_salida)
            rol.modulos.append(delete_salida)

        session.commit()
