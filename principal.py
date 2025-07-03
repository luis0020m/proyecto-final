from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'clave_secreta'  

from conexion import validar_usuario

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    usuario = request.form['usuario']
    contra = request.form['contra']

    user_data = validar_usuario(usuario, contra)
    print(user_data)

    if user_data:
        if user_data['rol'] == 'administrador':
            return redirect("/admin")
        elif user_data['rol'] == 'vendedor':
            return redirect("/vendedor")
    else:
        return render_template("login.html", msg = "Credenciales incorrectas. <a href='/'>Intentar de nuevo</a>")

@app.route('/admin')
def admin():
#    return redirect(url_for('index'))
    return render_template('admin_dashboard.html')

@app.route('/vendedor')
def vendedor():
    return redirect(url_for('index'))
    return "<h1>Bienvenido Vendedor</h1>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#parte de usuario#

from conexion import obtener_usuarios, insertar_usuario

@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        nombre = request.form['nombre']
        clave = request.form['clave']

        exito = insertar_usuario(nombre, clave,)
        if exito:
            return redirect(url_for('usuarios'))
        else:
            return "Error al agregar usuario. <a href='/usuarios'>Volver</a>"

    lista = obtener_usuarios()
    return render_template('usuarios.html', usuarios=lista)

#parte de abonos#

from conexion import validar_usuario, insertar_abono, obtener_clientes, obtener_ventas

@app.route('/abonar', methods=['GET', 'POST'])
def abonar():
    if request.method == 'POST':
        id_cliente = request.form['id_cliente']
        id_venta = request.form['id_venta']
        monto = request.form['monto']

        exito = insertar_abono(id_cliente, id_venta, monto)
        if exito:
            return "Abono registrado con éxito. <a href='/abonar'>Nuevo abono</a>"
        else:
            return "Error al registrar abono. <a href='/abonar'>Intentar de nuevo</a>"

    clientes = obtener_clientes()
    ventas = obtener_ventas()
    return render_template('abonos.html', clientes=clientes, ventas=ventas)

#parte de categorias#

from conexion import obtener_categorias, insertar_categoria

@app.route('/categorias', methods=['GET', 'POST'])
def categorias():
    if request.method == 'POST':
        nombre = request.form['nombre']
        exito = insertar_categoria(nombre)
        if exito:
            return redirect(url_for('categorias'))
        else:
            return "Error al agregar categoría. <a href='/categorias'>Volver</a>"

    lista = obtener_categorias()
    return render_template('categorias.html', categorias=lista)

#partes de clientes#

from flask import render_template, request, redirect, url_for
from conexion import (
    obtener_clientes, insertar_cliente,
    obtener_cliente_por_id, actualizar_cliente,
    eliminar_cliente
)

@app.route('/clientes')
def clientes():
    lista = obtener_clientes()
    return render_template("clientes", clientes=lista)

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    saldo = request.form['saldo']

    exito = insertar_cliente(nombre, direccion, telefono, saldo)
    if exito:
        return redirect(url_for('clientes'))
    else:
        return "Error al agregar cliente. <a href='/clientes'>Volver</a>"

@app.route('/editar_cliente/<int:id_cliente>')
def editar_cliente(id_cliente):
    cliente = obtener_cliente_por_id(id_cliente)
    return render_template('cliente', cliente=clientes)

@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente_route():
    id_cliente = request.form['id_cliente']
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    saldo = request.form['saldo']

    exito = actualizar_cliente(id_cliente, nombre, direccion, telefono, saldo)
    if exito:
        return redirect(url_for('clientes'))
    else:
        return "Error al actualizar cliente. <a href='/clientes'>Volver</a>"

@app.route('/eliminar_cliente/<int:id_cliente>')
def eliminar_cliente_route(id_cliente):
    exito = eliminar_cliente(id_cliente)
    if exito:
        return redirect(url_for('clientes'))
    else:
        return f"Error al eliminar cliente. <a href='/clientes'>Volver</a>"

#parte de compras#

from conexion import obtener_compras, insertar_compra, obtener_proveedores, obtener_clientes

@app.route('/compras', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        id_proveedor = request.form['id_proveedor']
        id_cliente = request.form['id_cliente']
        total = request.form['total']

        exito = insertar_compra(id_proveedor, id_cliente, total)
        if exito:
            return redirect(url_for('compras'))
        else:
            return "Error al registrar la compra. <a href='/compras'>Volver</a>"

    compras = obtener_compras()
    proveedores = obtener_proveedores()
    clientes = obtener_clientes()
    return render_template('compras', compras=compras, proveedores=proveedores, clientes=clientes)

#parte de detalles_pedidos#

from conexion import obtener_detalles_pedidos, insertar_detalle_pedido, obtener_pedidos, obtener_productos

@app.route('/detalles_pedidos', methods=['GET', 'POST'])
def detalles_pedidos():
    if request.method == 'POST':
        id_pedido = request.form['id_pedido']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        exito = insertar_detalle_pedido(id_pedido, id_producto, cantidad, precio)
        if exito:
            return redirect(url_for('detalles_pedidos'))
        else:
            return "Error al insertar detalle de pedido. <a href='/detalles_pedidos'>Volver</a>"

    detalles = obtener_detalles_pedidos()
    pedidos = obtener_pedidos()
    productos = obtener_productos()
    return render_template('detalles_pedidos.html', detalles=detalles, pedidos=pedidos, productos=productos)

#parte de detalles_ventas

from conexion import obtener_detalles_ventas, insertar_detalle_venta, obtener_ventas, obtener_productos

@app.route('/detalles_ventas', methods=['GET', 'POST'])
def detalles_ventas():
    if request.method == 'POST':
        id_venta = request.form['id_venta']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        precio_venta = request.form['precio_venta']

        exito = insertar_detalle_venta(id_venta, id_producto, cantidad, precio_venta)
        if exito:
            return redirect(url_for('detalles_ventas'))
        else:
            return "Error al insertar detalle de venta. <a href='/detalles_ventas'>Volver</a>"

    detalles = obtener_detalles_ventas()
    ventas = obtener_ventas()
    productos = obtener_productos()
    return render_template('detalles_ventas.html', detalles=detalles, ventas=ventas, productos=productos)

#parte de detalle_compra

from conexion import obtener_detalle_compras, insertar_detalle_compra, obtener_compras, obtener_productos

@app.route('/detalle_compras', methods=['GET', 'POST'])
def detalle_compras():
    if request.method == 'POST':
        id_compra = request.form['id_compra']
        id_producto = request.form['id_producto']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']

        exito = insertar_detalle_compra(id_compra, id_producto, cantidad, precio_unitario)
        if exito:
            return redirect(url_for('detalle_compras'))
        else:
            return "Error al insertar detalle de compra. <a href='/detalle_compras'>Volver</a>"

    detalles = obtener_detalle_compras()
    compras = obtener_compras()
    productos = obtener_productos()
    return render_template('detalle_compras.html', detalles=detalles, compras=compras, productos=productos)


    
#parte de estado_pedido#

from conexion import obtener_estados_pedido, insertar_estado_pedido

@app.route('/estado_pedido', methods=['GET', 'POST'])
def estado_pedido():
    if request.method == 'POST':
        nombre_estado = request.form['nombre_estado']
        exito = insertar_estado_pedido(nombre_estado)
        if exito:
            return redirect(url_for('estado_pedido'))
        else:
            return "Error al insertar estado. <a href='/estado_pedido'>Volver</a>"

    estados = obtener_estados_pedido()
    return render_template('estado_pedido.html', estados=estados)

#parte de lotes#

from conexion import obtener_lotes, insertar_lote, obtener_productos, obtener_pedidos

@app.route('/lotes', methods=['GET', 'POST'])
def lotes():
    if request.method == 'POST':
        id_producto = request.form['id_producto']
        fecha_vencimiento = request.form['fecha_vencimiento']
        stock = request.form['stock']
        agotado = request.form.get('agotado', 0)
        id_pedido = request.form['id_pedido']

        exito = insertar_lote(id_producto, fecha_vencimiento, stock, agotado, id_pedido)
        if exito:
            return redirect(url_for('lotes'))
        else:
            return "Error al registrar lote. <a href='/lotes'>Volver</a>"

    lotes = obtener_lotes()
    productos = obtener_productos()
    pedidos = obtener_pedidos()
    return render_template('lotes.html', lotes=lotes, productos=productos, pedidos=pedidos)



#parte de pedidos#

from conexion import obtener_pedidos, insertar_pedido, obtener_proveedores, obtener_estados_pedido

@app.route('/pedidos', methods=['GET', 'POST'])
def pedidos():
    if request.method == 'POST':
        fecha_pedido = request.form['fecha_pedido']
        fecha_entrega = request.form['fecha_entrega']
        id_proveedor = request.form['id_proveedor']
        id_estado_pedido = request.form['id_estado_pedido']

        exito = insertar_pedido(fecha_pedido, fecha_entrega, id_proveedor, id_estado_pedido)
        if exito:
            return redirect(url_for('pedidos'))
        else:
            return "Error al registrar el pedido. <a href='/pedidos'>Volver</a>"

    pedidos = obtener_pedidos()
    proveedores = obtener_proveedores()
    estados = obtener_estados_pedido()
    return render_template('pedidos.html', pedidos=pedidos, proveedores=proveedores, estados=estados)


#parte de productos#

from conexion import obtener_productos, insertar_producto, obtener_categorias

@app.route('/productos', methods=['GET', 'POST'])
def productos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        fecha_vencimiento = request.form['fecha_vencimiento']
        id_categoria = request.form['id_categoria']

        exito = insertar_producto(nombre, descripcion, precio, stock, fecha_vencimiento, id_categoria)
        if exito:
            return redirect(url_for('productos'))
        else:
            return "Error al registrar producto. <a href='/productos'>Volver</a>"

    productos = obtener_productos()
    categorias = obtener_categorias()
    return render_template('productos.html', productos=productos, categorias=categorias)


#parte de ventas#

from conexion import obtener_ventas, insertar_venta, obtener_clientes, obtener_usuarios

@app.route('/ventas', methods=['GET', 'POST'])
def ventas():
    if request.method == 'POST':
        tipo_venta = request.form['tipo_venta']
        id_cliente = request.form['id_cliente']
        id_usuario = request.form['id_usuario']
        total_venta = request.form['total_venta']

        exito = insertar_venta(tipo_venta, id_cliente, id_usuario, total_venta)
        if exito:
            return redirect(url_for('ventas'))
        else:
            return "Error al registrar la venta. <a href='/ventas'>Volver</a>"

    ventas = obtener_ventas()
    clientes = obtener_clientes()
    usuarios = obtener_usuarios()
    return render_template('ventas.html', ventas=ventas, clientes=clientes, usuarios=usuarios)


#parte de provedores#

from conexion import obtener_proveedores, insertar_proveedor, eliminar_proveedor, obtener_proveedor_por_id, actualizar_proveedor

@app.route('/proveedores', methods=['GET', 'POST'])
def proveedores():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        exito = insertar_proveedor(nombre, direccion, telefono)
        if exito:
            return redirect(url_for('proveedores'))
        else:
            return "Error al agregar proveedor. <a href='/proveedores'>Volver</a>"

    lista = obtener_proveedores()
    return render_template('proveedores.html', proveedores=lista)

@app.route('/editar_proveedor/<int:id>', methods=['GET'])
def editar_proveedor(id):
    proveedor = obtener_proveedor_por_id(id)
    return render_template('proveedor.html', proveedor=proveedor)


@app.route('/actualizar_proveedor', methods=['POST'])
def actualizar_proveedor_route():
    id_proveedor = request.form['id_proveedor']
    nombre = request.form['nombre']
    direccion = request.form['direccion']
    telefono = request.form['telefono']

    exito = actualizar_proveedor(id_proveedor, nombre, direccion, telefono)
    if exito:
        return redirect(url_for('proveedores'))
    else:
        return "Error al actualizar proveedor. <a href='/proveedores'>Volver</a>"

@app.route('/eliminar_proveedor/<int:id>', methods=['GET'])
def eliminar_proveedor_route(id):
    exito = eliminar_proveedor(id)
    if exito:
        return redirect(url_for('proveedores'))
    else:
        return "Error al eliminar proveedor. <a href='/proveedores'>Volver</a>"







if __name__ == '__main__':
    app.run(debug=True)
    
