from servidor.database.connection import transaction
from servidor.sistema.usuarios.usuario.model import Modulo
from servidor.sistema.usuarios.rol.model import Rol


def insertions():
    with transaction() as session:
        negocio_m = session.query(Modulo).filter(Modulo.nombre == 'negocio_mod').first()
        if negocio_m is None:
            negocio_m = Modulo(titulo='Negocio', nombre='negocio_mod', icono='business_center')

        empresa_m = session.query(Modulo).filter(Modulo.nombre == 'empresa').first()
        if empresa_m is None:
            empresa_m = Modulo(titulo='Empresa', ruta='/empresa', nombre='empresa', icono='business')

        negocio_m.children.append(empresa_m)

        query_empresa = session.query(Modulo).filter(Modulo.nombre == 'empresa_query').first()
        if query_empresa is None:
            query_empresa = Modulo(titulo='Consultar', ruta='', nombre='empresa_query', menu=False)
        insert_empresa = session.query(Modulo).filter(Modulo.nombre == 'empresa_insert').first()
        if insert_empresa is None:
            insert_empresa = Modulo(titulo='Adicionar', ruta='/empresa_insert', nombre='empresa_insert', menu=False)
        update_empresa = session.query(Modulo).filter(Modulo.nombre == 'empresa_update').first()
        if update_empresa is None:
            update_empresa = Modulo(titulo='Actualizar', ruta='/empresa_update', nombre='empresa_update', menu=False)
        delete_empresa = session.query(Modulo).filter(Modulo.nombre == 'empresa_delete').first()
        if delete_empresa is None:
            delete_empresa = Modulo(titulo='Dar de Baja', ruta='/empresa_delete', nombre='empresa_delete', menu=False)

        empresa_m.children.append(query_empresa)
        empresa_m.children.append(insert_empresa)
        empresa_m.children.append(update_empresa)
        empresa_m.children.append(delete_empresa)

        roles = session.query(Rol).filter(Rol.nombre.in_(['SUPER ADMINISTRADOR', "ADMINISTRADOR"])).all()

        for rol in roles:
            rol.modulos.append(negocio_m)
            rol.modulos.append(empresa_m)
            rol.modulos.append(query_empresa)
            rol.modulos.append(insert_empresa)
            rol.modulos.append(update_empresa)
            rol.modulos.append(delete_empresa)

        session.commit()
