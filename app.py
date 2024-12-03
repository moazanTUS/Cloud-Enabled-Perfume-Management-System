from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///perfumes.sqlite3'
app.secret_key = 'super secret key'
db = SQLAlchemy(app)
#define perfume model
class Perfume(db.Model):
    id = db.Column('perfume_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    brand = db.Column(db.String(50))
    scent = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=0)
    travel_size = db.Column(db.Boolean, default=False)
    climate = db.Column(db.String(50))

    def __init__(self, name, brand, scent, price, quantity=0, travel_size=False, climate=None):
        self.name = name
        self.brand = brand
        self.scent = scent
        self.price = price
        self.quantity = quantity
        self.travel_size = travel_size
        self.climate = climate



# Create database tables
db.create_all()


@app.route('/initial_table_data', methods=['GET', 'POST'])
def initial_table_data():
    if request.method == 'POST':
        # Add initial sample data with climate suitability
        db.session.add(Perfume('Dior J\'adore', 'Dior', 'Floral', 145.0, 12, True, 'Summer'))  # Summer climate
        db.session.add(Perfume('Chanel Coco Mademoiselle', 'Chanel', 'Oriental Floral', 155.0, 10, False, 'All Seasons'))
        db.session.add(Perfume('Gucci Bloom', 'Gucci', 'White Floral', 120.0, 18, True, 'Spring'))
        db.session.add(Perfume('YSL Libre', 'Yves Saint Laurent', 'Aromatic Floral', 135.0, 9, True, 'Winter'))
        db.session.add(Perfume('Tom Ford Lost Cherry', 'Tom Ford', 'Amber Floral', 175.0, 7, False, 'Autumn'))
        db.session.add(Perfume('Marc Jacobs Daisy', 'Marc Jacobs', 'Fresh Floral', 90.0, 20, True, 'Summer'))
        db.session.add(Perfume('Versace Bright Crystal', 'Versace', 'Floral Fruity', 85.0, 25, True, 'Spring'))
        db.session.add(Perfume('Jo Malone English Pear & Freesia', 'Jo Malone', 'Fruity Floral', 130.0, 15, False, 'Autumn'))
        db.session.add(Perfume('Lancome Idole', 'Lancôme', 'Floral Musk', 110.0, 11, True, 'All Seasons'))
        db.session.add(Perfume('Paco Rabanne Olympéa', 'Paco Rabanne', 'Floral Vanilla', 120.0, 8, True, 'Winter'))
        db.session.add(Perfume('Carolina Herrera Very Good Girl', 'Carolina Herrera', 'Floral Fruity', 125.0, 14, False, 'Spring'))
        db.session.add(Perfume('Burberry Her', 'Burberry', 'Fruity Floral', 115.0, 16, True, 'Autumn'))
        db.session.add(Perfume('Givenchy L’Interdit', 'Givenchy', 'White Floral', 135.0, 9, True, 'Winter'))
        db.session.add(Perfume('Viktor & Rolf Bonbon', 'Viktor & Rolf', 'Sweet Fruity', 140.0, 7, False, 'All Seasons'))
        db.session.add(Perfume('Prada Candy', 'Prada', 'Sweet Caramel', 120.0, 13, True, 'Autumn'))

        # Commit the updated sample perfumes to the database
        db.session.commit()
        flash('Updated Designer Perfume Data with Climate Added')
    return render_template('initial_table_data.html')


@app.route('/', methods=['GET', 'POST'])
def opening2():
    if request.method == 'POST':
        # Search by Brand
        if 'Search_By_Brand' in request.form:
            searchBrand = request.form.get('brand')
            if not searchBrand:
                flash('Please enter a brand to search', 'error')
            else:
                # Query the database for perfumes matching the brand
                perfume_list = db.session.query(Perfume).filter(Perfume.brand == searchBrand).all()
                if perfume_list:
                    return render_template('show_all.html', perfumes=perfume_list)
                else:
                    flash('No perfumes found for the specified brand', 'info')
    # If GET request or no specific action, show the main page with all perfumes
    all_perfumes = db.session.query(Perfume).all()
    return render_template('opening2.html', perfumes=all_perfumes)

@app.route('/delete_perfume/<int:perfume_id>', methods=['POST'])
def delete_perfume(perfume_id):
    perfume_to_delete = db.session.query(Perfume).filter_by(id=perfume_id).first()
    if perfume_to_delete:
        db.session.delete(perfume_to_delete)
        db.session.commit()
        flash(f'Perfume "{perfume_to_delete.name}" successfully deleted', 'success')
    else:
        flash(f'Perfume not found', 'error')
    return redirect(url_for('show_all'))

@app.route('/increment_quantity/<int:perfume_id>', methods=['GET', 'POST'])
def increment_quantity(perfume_id):
    perfume = db.session.query(Perfume).filter_by(id=perfume_id).first()
    if request.method == 'POST':
        increment_amount = int(request.form.get('increment_amount', 1))
        if perfume:
            perfume.quantity += increment_amount
            db.session.commit()
            flash(f'Quantity of "{perfume.name}" increased by {increment_amount}', 'success')
            return redirect(url_for('show_all'))
        else:
            flash('Perfume not found', 'error')
    return render_template('increment_quantity.html', perfume=perfume)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        brand = request.form['brand']
        scent = request.form['scent']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])
        travel_size = 'travel_size' in request.form
        climate = request.form['climate']  # Get climate

        # Create a new perfume object
        perfume = Perfume(name=name, brand=brand, scent=scent, price=price, quantity=quantity, travel_size=travel_size, climate=climate)
        db.session.add(perfume)
        db.session.commit()
        flash('New perfume added successfully', 'success')

        return redirect(url_for('show_all'))

    return render_template('new.html')


#

@app.route('/update2/<int:perfume_id>', methods=['GET', 'POST'])
def update2(perfume_id):
    perfume = db.session.query(Perfume).filter_by(id=perfume_id).first()
    if not perfume:
        flash('Perfume not found', 'error')
        return redirect(url_for('show_all'))

    if request.method == 'POST':
        # Update perfume details from the form
        perfume.name = request.form.get('name', perfume.name)
        perfume.brand = request.form.get('brand', perfume.brand)
        perfume.scent = request.form.get('scent', perfume.scent)
        perfume.price = float(request.form.get('price', perfume.price))
        perfume.quantity = int(request.form.get('quantity', perfume.quantity))
        perfume.travel_size = 'travel_size' in request.form
        perfume.climate = request.form.get('climate', perfume.climate)  # Update climate

        db.session.commit()
        flash('Perfume updated successfully', 'success')

        return redirect(url_for('show_all'))

    return render_template('update2.html', perfume=perfume)

@app.route('/show_all')
def show_all():
    # Get the climate filter from the query parameters
    climate_filter = request.args.get('climate', default=None)

    if climate_filter:
        # Filter perfumes by the selected climate
        all_perfumes = db.session.query(Perfume).filter_by(climate=climate_filter).all()
    else:
        # If no filter is applied, show all perfumes
        all_perfumes = db.session.query(Perfume).all()

    return render_template('show_all.html', perfumes=all_perfumes)

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')



