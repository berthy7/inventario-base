from configparser import ConfigParser
from sqlalchemy.engine import create_engine
from servidor.database import connection
from servidor.database.models import Base
from servidor.sistema.usuarios.rol.script import insertions as rol_insertions
from servidor.sistema.usuarios.usuario.script import insertions as user_insertions
from servidor.sistema.usuarios.bitacora.script import insertions as log_insertions

from servidor.sistema.negocio.empresa.script import insertions as empresa_insertions
from servidor.sistema.negocio.sucursal.script import insertions as sucursal_insertions
from servidor.sistema.negocio.producto.script import insertions as producto_insertions
from servidor.sistema.negocio.cliente.script import insertions as cliente_insertions
from servidor.sistema.negocio.ingreso.script import insertions as ingreso_insertions
from servidor.sistema.negocio.salida.script import insertions as salida_insertions
from servidor.sistema.negocio.traspaso.script import insertions as traspaso_insertions
from servidor.sistema.negocio.inventario.script import insertions as inventario_insertions

from servidor.sistema.datos.negocio import insertions as negocio_insertions

import sys
import sqlite3


def main():
    reload_db()
    rol_insertions()
    user_insertions()
    log_insertions()

    empresa_insertions()
    sucursal_insertions()
    producto_insertions()
    cliente_insertions()

    ingreso_insertions()
    salida_insertions()
    traspaso_insertions()
    inventario_insertions()

    negocio_insertions()

    print('Base de datos creada/actualizada correctamente!')


def reload_db():
    config = ConfigParser()
    config.read('settings.ini')
    db_url = config['Database']['url']
    connection.db_url = config['Database']['url']

    if 'sqlite' in db_url:
        dbname = db_url.split('///')[1]
        sqlite3.connect(dbname)

    engine = create_engine(config['Database']['url'])
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine, checkfirst=True)


def clean_db():
    config = ConfigParser()
    config.read('settings.ini')
    db_url = config['Database']['url']
    connection.db_url = config['Database']['url']

    if 'sqlite' in db_url:
        dbname = db_url.split('///')[1]
        sqlite3.connect(dbname)

    engine = create_engine(config['Database']['url'])
    Base.metadata.drop_all(engine, checkfirst=True)
    print("Las tablas de la base de datos se eliminaron correctamente!")


if __name__ == '__main__':
    sys.exit(int(main() or 0))
