from servidor.common.managers import SuperManager
from servidor.sistema.usuarios.bitacora.manager import BitacoraManager
from servidor.sistema.usuarios.usuario.manager import UsuarioManager
from servidor.sistema.usuarios.bitacora.model import Bitacora
from servidor.sistema.negocio.inventario.model import Inventario
from datetime import datetime

import pytz
import json
import pandas as pd

global fecha_zona
fecha_zona = datetime.now(pytz.timezone('America/La_Paz'))


class InventarioManager(SuperManager):

    def __init__(self, db):
        super().__init__(Inventario, db)

    def listar_habilitados(self):
        return self.db.query(self.entity).filter(self.entity.estado).filter(self.entity.enabled).all()

    def listar_todo(self):
        return self.db.query(self.entity).filter(self.entity.enabled).all()

    def list_all(self):
        return dict(objects=self.db.query(self.entity).filter(self.entity.enabled))

    def all_data(self, idu):
        privilegios = UsuarioManager(self.db).get_privileges(idu, '/inventario')
        datos = self.db.query(self.entity).filter(self.entity.enabled).all()
        list_dt = []

        for item in datos:
            is_active = item.estado
            disable = 'disabled' if 'inventario_update' not in privilegios else ''
            estado = 'Activo' if is_active else 'Inactivo'
            check = 'checked' if is_active else ''
            delete = 'inventario_delete' in privilegios
            sucursal = item.sucursal.nombre if item.sucursal else ''
            producto = item.producto.nombre if item.producto else ''
            codigo = item.producto.codigo if item.producto else ''

            diccionario = item.get_dict()
            diccionario['estado'] = estado
            diccionario['check'] = check
            diccionario['disable'] = disable
            diccionario['delete'] = delete
            diccionario['sucursal'] = sucursal
            diccionario['producto'] = producto
            diccionario['codigo'] = codigo
            list_dt.append(diccionario)

        return list_dt

    def data_by_sucursal(self, idsucursal):
        datos = self.db.query(self.entity).filter(self.entity.enabled).filter(self.entity.fksucursal == idsucursal).all()
        list_dt = []

        for item in datos:
            sucursal = item.sucursal.nombre if item.sucursal else ''
            producto = item.producto.nombre if item.producto else ''
            codigo = item.producto.codigo if item.producto else ''

            diccionario = item.get_dict()
            diccionario['sucursal'] = sucursal
            diccionario['producto'] = producto
            diccionario['codigo'] = codigo
            list_dt.append(diccionario)

        return list_dt

    def actualizar_productos(self, objeto, user_id, ip):
        fecha = BitacoraManager(self.db).fecha_actual()

        for i in objeto.detalle:
            objeto_inventario = self.db.query(self.entity).filter(self.entity.fksucursal == objeto.fksucursal).filter(self.entity.fkproducto == i.fkproducto).first()

            if objeto_inventario:
                nueva_cantidad = int(i.cantidad) + int(objeto_inventario.cantidad)
                objeto_inventario.cantidad = nueva_cantidad
                a = super().update(objeto_inventario)
            else:
                dict_inventario = dict(cantidad=i.cantidad, fkproducto=i.fkproducto, fksucursal=objeto.fksucursal)
                objeto = InventarioManager(self.db).entity(**dict_inventario)
                a = super().insert(objeto)

            b = Bitacora(fkusuario=user_id, ip=ip, accion="Registró entrada del inventario.", fecha=fecha, tabla="negocio_inventario", identificador=a.id)
            super().insert(b)

    def descontar_productos(self, objeto, user_id, ip):
        fecha = BitacoraManager(self.db).fecha_actual()

        for i in objeto.detalle:
            objeto_inventario = self.db.query(self.entity).filter(self.entity.fksucursal == objeto.fksucursal).filter(self.entity.fkproducto == i.fkproducto).first()

            if objeto_inventario:
                nueva_cantidad = int(objeto_inventario.cantidad) - int(i.cantidad)
                objeto_inventario.cantidad = nueva_cantidad
                a = super().update(objeto_inventario)
                b = Bitacora(fkusuario=user_id, ip=ip, accion="Registró salida del inventario.", fecha=fecha, tabla="negocio_inventario", identificador=a.id)
                super().insert(b)

    def traspaso_productos(self, objeto, user_id, ip):
        fecha = BitacoraManager(self.db).fecha_actual()

        for i in objeto.detalle:

            objeto_inventario_ingreso = self.db.query(self.entity).filter(self.entity.fksucursal == objeto.fkdestino).filter(
                self.entity.fkproducto == i.fkproducto).first()

            if objeto_inventario_ingreso:
                nueva_cantidad = int(i.cantidad) + int(objeto_inventario_ingreso.cantidad)
                objeto_inventario_ingreso.cantidad = nueva_cantidad
                a = super().update(objeto_inventario_ingreso)
            else:
                dict_inventario = dict(cantidad=i.cantidad, fkproducto=i.fkproducto, fksucursal=objeto.fkdestino)
                objeto = InventarioManager(self.db).entity(**dict_inventario)
                a = super().insert(objeto)

            b = Bitacora(fkusuario=user_id, ip=ip, accion="Registró entrada de inventario.", fecha=fecha,
                         tabla="negocio_inventario", identificador=a.id)
            super().insert(b)

            objeto_inventario_salida = self.db.query(self.entity).filter(self.entity.fksucursal == objeto.fkorigen).filter(
                self.entity.fkproducto == i.fkproducto).first()

            if objeto_inventario_salida:
                nueva_cantidad = int(objeto_inventario_salida.cantidad) - int(i.cantidad)
                objeto_inventario_salida.cantidad = nueva_cantidad
                a = super().update(objeto_inventario_salida)
                b = Bitacora(fkusuario=user_id, ip=ip, accion="Registró salida de inventario.", fecha=fecha,
                             tabla="negocio_inventario", identificador=a.id)
                super().insert(b)






    def update(self, objeto):
        fecha = BitacoraManager(self.db).fecha_actual()

        a = super().update(objeto)
        b = Bitacora(fkusuario=objeto.user, ip=objeto.ip, accion="Modificó inventario.", fecha=fecha, tabla="negocio_inventario", identificador=a.id)
        super().insert(b)
        return a

    def state(self, id, estado, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        mensaje = "Habilitó inventario" if estado else "Deshabilitó inventario"
        x.estado = estado

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="negocio_inventario", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()
        return x

    def delete(self, id, user, ip):
        x = self.db.query(self.entity).filter(self.entity.id == id).one()
        x.enabled = False

        fecha = BitacoraManager(self.db).fecha_actual()
        b = Bitacora(fkusuario=user, ip=ip, accion="Eliminó inventario", fecha=fecha, tabla="negocio_inventario", identificador=id)
        super().insert(b)
        self.db.merge(x)
        self.db.commit()

    def transaccion_item(self, item):
        ip = item['ip']
        user = item['user']
        accion = item['accion']
        idsucursal = item['fksucursal']
        cantidad = int(item['cantidad'])
        idproducto = int(item['fkproducto'])
        fecha = BitacoraManager(self.db).fecha_actual()
        obj_invent = self.db.query(self.entity).filter(self.entity.fksucursal == idsucursal).filter(self.entity.fkproducto == idproducto).first()
        mensaje = "Registró entrada del inventario." if accion == 'ingreso' else "Registró salida del inventario."

        if obj_invent:
            obj_invent.cantidad += int(cantidad) if accion == 'ingreso' else - int(cantidad)
            a = super().update(obj_invent)
        else:
            dict_inventario = dict(cantidad=cantidad, fkproducto=idproducto, fksucursal=idsucursal)
            objeto = InventarioManager(self.db).entity(**dict_inventario)
            a = super().insert(objeto)

        b = Bitacora(fkusuario=user, ip=ip, accion=mensaje, fecha=fecha, tabla="negocio_inventario", identificador=a.id)
        super().insert(b)

    def iteritems_func(self, df_data, accion, check_cant, ip, user, fksucursal, tipo):
        for index, row in df_data.iterrows():
            if not check_cant or check_cant and row['cantidad'] != row['cant_prev']:
                item = dict()
                item['ip'] = ip
                item['user'] = user
                item['accion'] = accion
                item['fksucursal'] = fksucursal
                item['cantidad'] = row['cantidad']
                item['fkproducto'] = row['fkproducto']

                if check_cant:
                    item['cantidad'] = row['cantidad'] - row['cant_prev'] if row['cantidad'] > row['cant_prev'] else row['cant_prev'] - row['cantidad']

                    if tipo == 'ingresos':
                        item['accion'] = 'ingreso' if row['cantidad'] > row['cant_prev'] else 'salida'
                    else:
                        item['accion'] = 'salida' if row['cantidad'] > row['cant_prev'] else 'ingreso'

                self.transaccion_item(item)

    def update_ingresos(self, dtprev, dtcur):
        fksucursal = dtcur['fksucursal']
        user = dtcur['user']
        ip = dtcur['ip']
        dtant = dtprev.get_dict()
        dtact = dtcur

        dfant = pd.DataFrame(dtant['detalle'])
        dfant = dfant.filter(items=['id', 'fkproducto', 'cantidad'])
        dfcur = pd.DataFrame(dtact['detalle'])
        convert_dict = {'fkproducto': int, 'cantidad': int}
        dfcur = dfcur.astype(convert_dict)
        dfins = dfcur[pd.isnull(dfcur.id)]
        dfins = dfins.filter(items=['fkproducto', 'cantidad'])
        dfins = dfins.astype(convert_dict)
        dfcur = dfcur[pd.notnull(dfcur.id)]
        conv_dict = {'id': int}
        dfcur = dfcur.astype(conv_dict)

        dfantrn = dfant.rename(columns={'cantidad': 'cant_prev'})
        dfupd_cant = dfantrn.merge(dfcur, on=['id', 'fkproducto'])
        dfantrnm = dfant.rename(columns={'fkproducto': 'fkpro_prev', 'cantidad': 'cant_prev'})
        dfupd_id = dfantrnm.merge(dfcur, on=['id'])
        dfupd_val = dfupd_id[(~dfupd_id.id.isin(dfupd_cant.id)) & (~dfupd_id.fkproducto.isin(dfupd_cant.fkproducto))]
        dfdel = dfant[(~dfant.id.isin(dfupd_cant.id)) & (~dfant.fkproducto.isin(dfupd_cant.fkproducto))]

        self.iteritems_func(dfins, 'ingreso', False, ip, user, fksucursal, 'ingresos')
        self.iteritems_func(dfdel, 'salida', False, ip, user, fksucursal, 'ingresos')
        self.iteritems_func(dfupd_cant, '', True, ip, user, fksucursal, 'ingresos')
        self.iteritems_func(dfupd_val, 'ingreso', False, ip, user, fksucursal, 'ingresos')

    def update_salidas(self, dtprev, dtcur):
        fksucursal = dtcur['fksucursal']
        user = dtcur['user']
        ip = dtcur['ip']
        dtant = dtprev.get_dict()
        dtact = dtcur

        dfant = pd.DataFrame(dtant['detalle'])
        dfant = dfant.filter(items=['id', 'fkproducto', 'cantidad'])
        dfcur = pd.DataFrame(dtact['detalle'])
        convert_dict = {'fkproducto': int, 'cantidad': int}
        dfcur = dfcur.astype(convert_dict)
        dfins = dfcur[pd.isnull(dfcur.id)]
        dfins = dfins.filter(items=['fkproducto', 'cantidad'])
        dfins = dfins.astype(convert_dict)
        dfcur = dfcur[pd.notnull(dfcur.id)]
        conv_dict = {'id': int}
        dfcur = dfcur.astype(conv_dict)

        dfantrn = dfant.rename(columns={'cantidad': 'cant_prev'})
        dfupd = dfantrn.merge(dfcur, on=['id', 'fkproducto'])
        dfdel = dfant[(~dfant.id.isin(dfupd.id)) & (~dfant.fkproducto.isin(dfupd.fkproducto))]

        self.iteritems_func(dfins, 'salida', False, ip, user, fksucursal, 'salidas')
        self.iteritems_func(dfdel, 'ingreso', False, ip, user, fksucursal, 'salidas')
        self.iteritems_func(dfupd, '', True, ip, user, fksucursal, 'salidas')
