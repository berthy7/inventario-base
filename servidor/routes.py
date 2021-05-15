from servidor.sistema.usuarios.login.controller import LoginController, LogoutController
from servidor.sistema.usuarios.usuario.controller import UsuarioController, ManualController
from servidor.sistema.usuarios.persona.controller import PersonaController
from servidor.sistema.usuarios.rol.controller import RolController
from servidor.sistema.usuarios.bitacora.controller import BitacoraController


from servidor.sistema.negocio.cliente.controller import ClienteController
from servidor.sistema.negocio.empresa.controller import EmpresaController
from servidor.sistema.negocio.ingreso.controller import IngresoController
from servidor.sistema.negocio.inventario.controller import InventarioController
from servidor.sistema.negocio.producto.controller import ProductoController
from servidor.sistema.negocio.salida.controller import SalidaController
from servidor.sistema.negocio.sucursal.controller import SucursalController
from servidor.sistema.negocio.traspaso.controller import TraspasoController


from servidor.main.controller import Index
from tornado.web import StaticFileHandler

import os


def get_routes(handler):
    routes = list()

    for route in handler.routes:
        routes.append((route, handler))

    return routes


def get_handlers():
    """Retorna una lista con las rutas, sus manejadores y datos extras."""
    handlers = list()

    # Principal
    handlers.append((r'/', Index))

    # Login
    handlers.append((r'/inicio', LoginController))
    handlers.append((r'/logout', LogoutController))

    # Usuarios
    handlers.append((r'/manual', ManualController))
    handlers.extend(get_routes(BitacoraController))
    handlers.extend(get_routes(RolController))
    handlers.extend(get_routes(UsuarioController))
    handlers.extend(get_routes(PersonaController))

    # Negocio
    handlers.extend(get_routes(ClienteController))
    handlers.extend(get_routes(EmpresaController))
    handlers.extend(get_routes(IngresoController))
    handlers.extend(get_routes(InventarioController))
    handlers.extend(get_routes(ProductoController))
    handlers.extend(get_routes(SalidaController))
    handlers.extend(get_routes(SucursalController))
    handlers.extend(get_routes(TraspasoController))



    handlers.append((r'/resources/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'resources')}))

    # Recursos por submodulo
    handlers.append((r'/common/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'common', 'assets')}))
    handlers.append((r'/main/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'main', 'assets')}))
    handlers.append((r'/usuarios/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'sistema', 'usuarios')}))
    handlers.append((r'/negocio/(.*)', StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'sistema', 'negocio')}))

    return handlers
