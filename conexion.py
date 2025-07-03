import mysql.connector
import hashlib

def conectar():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="",
        database="datos"  
    )

def validar_usuario(usuario, clave):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    hash_clave = hashlib.sha256(clave.encode()).hexdigest()
    query = "SELECT * FROM usuarios WHERE nombre = %s AND contraseña = %s"
    cursor.execute(query, (usuario, clave))  

    resultado = cursor.fetchone()
    conexion.close()
    return resultado



#usuarios#
def obtener_usuarios():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre FROM usuarios")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_usuario(nombre, clave):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = "INSERT INTO usuarios (nombre, contraseña,) VALUES (%s, %s)"
        cursor.execute(query, (nombre, clave,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar usuario:", e)
        return False



#parte de abono#

def insertar_abono(id_cliente, id_venta, monto):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = "INSERT INTO abonos (id_cliente, id_venta, monto_abono) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_cliente, id_venta, monto))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar abono:", e)
        return False

def obtener_clientes():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nombre FROM clientes")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def obtener_ventas():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
#    cursor.execute("SELECT id_venta FROM ventas")
    cursor.execute("SELECT t1.id_venta t2.nombre FROM ventas t1 INNER JOIN cientes t2 ON t1.id_cliente = t2.id_cliente;")

    resultado = cursor.fetchall()
    conexion.close()
    return resultado



#parte de categorias#

def obtener_categorias():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categorias")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_categoria(nombre, imagen):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO categorias (nombre_categoria, imagen_categoria) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, imagen))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar categoría:", e)
        return False


#parte de clientes#

def obtener_clientes():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_cliente(nombre, direccion, telefono, saldo):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = "INSERT INTO clientes (nombre, direccion_cliente, telefono, saldo) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, direccion, telefono, saldo))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar cliente:", e)
        return False

def obtener_cliente_por_id(id_cliente):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id_cliente,))
    cliente = cursor.fetchone()
    conexion.close()
    return cliente

def actualizar_cliente(id_cliente, nombre, direccion, telefono, saldo):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            UPDATE clientes
            SET nombre = %s, direccion_cliente = %s, telefono = %s, saldo = %s
            WHERE id_cliente = %s
        """
        cursor.execute(sql, (nombre, direccion, telefono, saldo, id_cliente))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al actualizar cliente:", e)
        return False

def eliminar_cliente(id_cliente):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id_cliente,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al eliminar cliente:", e)
        return False





#parte de compras#

def obtener_compras():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT c.id_compra, c.fecha_compra, c.total, p.nombre AS proveedor, cl.nombre AS cliente
    FROM compras c
    JOIN proveedores p ON c.id_proveedor = p.id_proveedor
    JOIN clientes cl ON c.id_cliente = cl.id_cliente
    ORDER BY c.id_compra DESC
    """
    cursor.execute(query)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_compra(id_proveedor, id_cliente, total):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = "INSERT INTO compras (id_proveedor, id_cliente, total) VALUES (%s, %s, %s)"
        cursor.execute(query, (id_proveedor, id_cliente, total))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar compra:", e)
        return False

def obtener_proveedores():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_proveedor, nombre FROM proveedores")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


#parte de detalles_pedidos#

def obtener_detalles_pedidos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    query = """
    SELECT dp.id_pedido, p.nombre_producto, dp.cantidad_pedido, dp.precio_compra
    FROM detalles_pedidos dp
    JOIN productos p ON dp.id_producto = p.id_producto
    """
    cursor.execute(query)
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_detalle_pedido(id_pedido, id_producto, cantidad, precio):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        query = "INSERT INTO detalles_pedidos (id_pedido, id_producto, cantidad_pedido, precio_compra) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (id_pedido, id_producto, cantidad, precio))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar detalle de pedido:", e)
        return False

def obtener_pedidos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_pedido FROM pedidos")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT id_producto, nombre_producto FROM productos")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado


#detalles_ventas



def obtener_detalles_ventas():
    
    consulta = "SELECT * FROM detalles_ventas"
    
    pass

def insertar_detalle_venta(id_venta, id_producto, cantidad, precio_venta):
    consulta = "INSERT INTO detalles_ventas (id_venta, id_producto, cantidad, precio_Venta) VALUES (%s, %s, %s, %s)"
    valores = (id_venta, id_producto, cantidad, precio_venta)
    
    pass

def obtener_ventas():
    
    pass

def obtener_productos():
    
    pass


#parte de detalle_compra

def obtener_detalle_compras():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM detalle_compras")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_detalle_compra(id_compra, id_producto, cantidad, precio_unitario):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO detalle_compras (id_compra, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
        """
        valores = (id_compra, id_producto, cantidad, precio_unitario)
        cursor.execute(consulta, valores)
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar detalle de compra:", e)
        return False


#parte de estado_pedido#

def obtener_estados_pedido():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estado_pedido")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_estado_pedido(nombre_estado):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO estado_pedido (nombre_estado) VALUES (%s)"
        cursor.execute(sql, (nombre_estado,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar estado_pedido:", e)
        return False



#parte de lotes#

def obtener_lotes():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lotess")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_lote(id_producto, fecha_vencimiento, stock, agotado, id_pedido):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO lotess (id_producto, fecha_vencimiento, stock, agotado, id_pedido)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (id_producto, fecha_vencimiento, stock, agotado, id_pedido)
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar lote:", e)
        return False


#parte de pedidos#

def obtener_pedidos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    conexion.close()
    return pedidos

def insertar_pedido(fecha_pedido, fecha_entrega, id_proveedor, id_estado_pedido):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO pedidos (fecha_pedido, fecha_entrega, id_proveedor, id_estado_pedido)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (fecha_pedido, fecha_entrega, id_proveedor, id_estado_pedido))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar pedido:", e)
        return False




#parte de productos#

def obtener_productos():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conexion.close()
    return productos

def insertar_producto(nombre, descripcion, precio, stock, fecha_vencimiento, id_categoria):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO productos 
            (nombre_producto, descripcion_producto, precio_producto, stock, fecha_vencimiento, id_categoria)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nombre, descripcion, precio, stock, fecha_vencimiento, id_categoria))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar producto:", e)
        return False



#parte de ventas#

def obtener_ventas():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ventas")
    resultado = cursor.fetchall()
    conexion.close()
    return resultado

def insertar_venta(tipo_venta, id_cliente, id_usuario, total_venta):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            INSERT INTO ventas (tipo_venta, id_cliente, id_usuario, total_venta)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (tipo_venta, id_cliente, id_usuario, total_venta))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar venta:", e)
        return False


#parte de provedores# 

def insertar_proveedor(nombre, direccion, telefono):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "INSERT INTO proveedores (nombre, direccion_provedor, telefono) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, direccion, telefono))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al insertar proveedor:", e)
        return False

def eliminar_proveedor(id_proveedor):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = "DELETE FROM proveedores WHERE id_proveedor = %s"
        cursor.execute(sql, (id_proveedor,))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al eliminar proveedor:", e)
        return False

def obtener_proveedor_por_id(id_proveedor):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = "SELECT * FROM proveedores WHERE id_proveedor = %s"
    cursor.execute(sql, (id_proveedor,))
    proveedor = cursor.fetchone()
    conexion.close()
    return proveedor

def actualizar_proveedor(id_proveedor, nombre, direccion, telefono):
    try:
        conexion = conectar()
        cursor = conexion.cursor()
        sql = """
            UPDATE proveedores
            SET nombre = %s, direccion_provedor = %s, telefono = %s
            WHERE id_proveedor = %s
        """
        cursor.execute(sql, (nombre, direccion, telefono, id_proveedor))
        conexion.commit()
        conexion.close()
        return True
    except Exception as e:
        print("Error al actualizar proveedor:", e)
        return False

