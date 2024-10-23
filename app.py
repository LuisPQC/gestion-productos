from flask import Flask, session, redirect, url_for, render_template, request
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Clave necesaria para el manejo de sesiones

# Ruta principal para mostrar los productos
@app.route('/')
def index():
    if 'products' not in session:
        session['products'] = []  # Inicializa la lista de productos en la sesión
    return render_template('index.html', products=session['products'])

# Ruta para agregar un nuevo producto
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        # Generar un ID único
        new_id = len(session['products']) + 1
        
        # Crear un diccionario con los datos del producto
        new_product = {
            'id': new_id,
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }

        # Agregar el nuevo producto a la sesión
        session['products'].append(new_product)
        session.modified = True  # Para que Flask reconozca los cambios en la sesión
        
        return redirect(url_for('index'))
    
    return render_template('add_product.html')

# Ruta para editar un producto
@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    # Encontrar el producto por su ID
    product = next((p for p in session['products'] if p['id'] == product_id), None)
    
    if request.method == 'POST':
        # Actualizar los campos del producto
        product['nombre'] = request.form['nombre']
        product['cantidad'] = int(request.form['cantidad'])
        product['precio'] = float(request.form['precio'])
        product['fecha_vencimiento'] = request.form['fecha_vencimiento']
        product['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))

    # Si es GET, mostrar el formulario de edición con los datos del producto actual
    return render_template('edit_product.html', product=product)

# Ruta para eliminar un producto
@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    # Buscar y eliminar el producto por su ID
    session['products'] = [product for product in session['products'] if product['id'] != product_id]
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
