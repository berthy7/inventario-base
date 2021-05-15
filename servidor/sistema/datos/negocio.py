from servidor.database.connection import transaction
from servidor.sistema.negocio.empresa.model import Empresa
from servidor.sistema.negocio.sucursal.model import Sucursal
from servidor.sistema.negocio.producto.model import Producto
from servidor.sistema.negocio.cliente.model import Cliente


def insertions():
    with transaction() as session:
        store_empress = Empresa(nombre='ROHO Homecenter')
        session.add(store_empress)

        suc_store = Sucursal(nombre='Central')
        suc_store.empresa = store_empress
        suc_store2 = Sucursal(nombre='3er anillo')
        suc_store2.empresa = store_empress

        session.add(suc_store)
        session.add(suc_store2)

        prod01_store = Producto(codigo='AIRCMPG030059', nombre='TERMO ROJO 2.5L ATACAMA', descripcion='Uso: Mantiene las bebidas frías\nCapacidad: 2.5 Litros\nColor: Rojo\nMedidas: 28x20x16Cm\nMarca: Soprano', precio=59.9)
        prod02_store = Producto(codigo='AIRCMPG020007', nombre='CARPA PHILY 2 PERSONAS 2500MM NTK', descripcion='', precio=550)
        prod03_store = Producto(codigo='HRRMANO030073', nombre='CAJA DE HERRAMIENTA PLASTICA 19PLG B/METAL STANLEY', descripcion='CAJA DE HERRAMIENTA PLÁSTICA 19 PULGADA BROCHE METÁLICO STANLEY', precio=190)
        prod04_store = Producto(codigo='MBLOFCN010039', nombre='ESCRITORIO STUDIO 1.3 C/CAJON ARG/PRT 136X75X60CM', descripcion='Con medidas de 60 ancho x 75 alto x 136 largo cm y un peso de 34 kilos, este escritorio podrá utilizarse sin problemas para ubicar un computador e impresora.', precio=969)

        session.add(prod01_store)
        session.add(prod02_store)
        session.add(prod03_store)
        session.add(prod04_store)
        #---------------------------------------------------------------------------------------------------------------------------------#
        # farm_empress = Empresa(nombre='Farmacorp')
        #
        # suc_farm01 = Sucursal(nombre='Banzer 3er anillo')
        # suc_farm01.empresa = farm_empress
        # suc_farm02 = Sucursal(nombre='Torres Gemelas')
        # suc_farm02.empresa = farm_empress
        # suc_farm03 = Sucursal(nombre='Av. Cristo Redentor')
        # suc_farm03.empresa = farm_empress
        # suc_farm04 = Sucursal(nombre='Equipetrol')
        # suc_farm04.empresa = farm_empress
        #
        # session.add(suc_farm01)
        # session.add(suc_farm02)
        # session.add(suc_farm03)
        # session.add(suc_farm04)
        #
        # prod01_farm = Producto(codigo='SK101', nombre='VITARosa', descripcion='Bloqueador solar VITAROSA', precio=50)
        # prod02_farm = Producto(codigo='SK247', nombre='Colágeno', descripcion='Whisky Dewar’s 12, Amaro, mermelada de higo, zumo de limón', precio=80)
        # prod03_farm = Producto(codigo='CR745', nombre='Crema', descripcion='Crema limpia pecas', precio=70)
        #
        # session.add(prod01_farm)
        # session.add(prod02_farm)
        # session.add(prod03_farm)
        # ---------------------------------------------------------------------------------------------------------------------------------#
        cliente01 = Cliente(nombre='Sandra Justiniano', nit='786521317826')
        cliente02 = Cliente(nombre='Marcelo Estrada', nit='234567569845')
        cliente03 = Cliente(nombre='Arturo Aguirre', nit='147832484574')
        cliente04 = Cliente(nombre='Alexander Vega', nit='654685404550')

        session.add(cliente01)
        session.add(cliente02)
        session.add(cliente03)
        session.add(cliente04)

        session.commit()
