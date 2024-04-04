from sqlalchemy.orm import sessionmaker
from db import engine, Data

def seed():
    # Create a session maker using the engine from db.py
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear the data table
    session.query(Data).delete()

    # Seed the table with initial data
    initial_data = [
        Data(region='Hlavní město Praha', item_type='Electronics', price=7000),
        Data(region='Jihomoravský kraj', item_type='Clothing', price=18950),
        Data(region='Středočeský kraj', item_type='Tools', price=15060),
        Data(region='Moravskoslezský kraj', item_type='Books', price=27699),
        Data(region='Jihočeský kraj', item_type='Home Appliances', price=21997),
        Data(region='Plzeňský kraj', item_type='Other', price=27352),
        Data(region='Olomoucký kraj', item_type='Jewelry', price=17234),
        Data(region='Ústecký kraj', item_type='Toys', price=15477),
        Data(region='Liberecký kraj', item_type='Food', price=28543),
        Data(region='Karlovarský kraj', item_type='Furniture', price=8711),
        Data(region='Pardubický kraj', item_type='Sports Equipment', price=2076),
        Data(region='Kraj Vysočina', item_type='Electronics', price=12345),
        Data(region='Karlovarský kraj', item_type='Clothing', price=29814),
        Data(region='Středočeský kraj', item_type='Home Appliances', price=29850),
        Data(region='Olomoucký kraj', item_type='Books', price=24319),
        Data(region='Ústecký kraj', item_type='Furniture', price=18843),
        Data(region='Liberecký kraj', item_type='Jewelry', price=29459),
        Data(region='Plzeňský kraj', item_type='Food', price=21314),
        Data(region='Jihomoravský kraj', item_type='Tools', price=13789),
        Data(region='Pardubický kraj', item_type='Toys', price=24962),
        Data(region='Moravskoslezský kraj', item_type='Sports Equipment', price=29213),
        Data(region='Zlínský kraj', item_type='Other', price=28547),
        Data(region='Královéhradecký kraj', item_type='Electronics', price=28165),
        Data(region='Zlínský kraj', item_type='Clothing', price=13579),
        Data(region='Kraj Vysočina', item_type='Furniture', price=9502),
        Data(region='Hlavní město Praha', item_type='Books', price=23451),
        Data(region='Karlovarský kraj', item_type='Jewelry', price=18753),
        Data(region='Moravskoslezský kraj', item_type='Food', price=27198),
        Data(region='Středočeský kraj', item_type='Electronics', price=22677),
        Data(region='Ústecký kraj', item_type='Clothing', price=15782),
        Data(region='Jihočeský kraj', item_type='Tools', price=29536),
        Data(region='Pardubický kraj', item_type='Books', price=18190),
        Data(region='Kraj Vysočina', item_type='Home Appliances', price=26193),
        Data(region='Liberecký kraj', item_type='Other', price=11477),
        Data(region='Hlavní město Praha', item_type='Jewelry', price=21865),
        Data(region='Zlínský kraj', item_type='Toys', price=19843),
        Data(region='Olomoucký kraj', item_type='Sports Equipment', price=23016),
        Data(region='Moravskoslezský kraj', item_type='Electronics', price=19275),
        Data(region='Karlovarský kraj', item_type='Food', price=16537),
        Data(region='Jihomoravský kraj', item_type='Furniture', price=25314)
    ]
    session.add_all(initial_data)
    session.commit()
    print("Data seeded successfully.")

    # Close the session
    session.close()
