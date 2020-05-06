from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__) # la constante de la aplicacion



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'cricket'
app.config['MYSQL_PASSWORD'] = 'backinthe90s'
app.config['MYSQL_DB'] = 'test_db'
mysql = MySQL(app)

#Session en localstorage
app.secret_key = 'mysupersecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM customers' )
    data = cur.fetchall()
    return render_template('index.html', clients = data)


@app.route('/sales')
def sales():
    cur = mysql.connection.cursor()
    cur.execute('select sales.sales_id,  customers.customer_name, sales.sales_amount from sales inner join customers on sales.customer_id=customers.customer_id;' )
    data = cur.fetchall()
    return render_template('ventas.html', sales = data)


@app.route('/add', methods=['POST'])
def addClient():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        customer_name = request.form['customer_name']
        level = request.form['level']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO customers (customer_id, customer_name, level) VALUES (%s, %s, %s)', 
        (customer_id, customer_name, level ))
        mysql.connection.commit()
        flash('Cliente añadido correctamente!')
        return redirect(url_for('index'))

@app.route('/add_sale', methods=['POST'])
def addSale():
    if request.method == 'POST':
        sales_id = request.form['sales_id']
        customer_id = request.form['customer_id']
        sales_amount = request.form['sales_amount']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO sales (sales_id, customer_id, sales_amount) VALUES (%s, %s, %s)', 
        (sales_id, customer_id, sales_amount ))
        mysql.connection.commit()
        flash('Venta añadida correctamente!')
        return redirect(url_for('sales'))


@app.route('/delete_customer/<string:id>')
def deleteCustomer(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM customers WHERE customer_id = {}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado correctamente!')
    return redirect(url_for('index'))


@app.route('/delete_sale/<string:id>')
def deleteSale(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM sales WHERE sales_id = {}'.format(id))
    mysql.connection.commit()
    flash('Venta eliminada correctamente!')
    return redirect(url_for('sales'))

@app.route('/edit_sale/<id>')
def getSale(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT sales.sales_id, customers.customer_name, sales.sales_amount FROM sales inner join customers on sales.customer_id=customers.customer_id WHERE sales_id = {};'.format(id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-sale.html', sale=data[0])

@app.route('/update_sale/<id>', methods=['POST'])
def updateSale(id):
    if request.method=='POST':
        sales_amount = request.form['sales_amount']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE sales SET sales_amount={} WHERE sales_id={};'.format(sales_amount, id))
        mysql.connection.commit()
        flash('Venta actualizada correctamente!')
        return redirect(url_for('sales'))    

if __name__ == "__main__": #verificar que estemos en el entorno main
    app.run(port=4000, debug=True)