from db import Order, sessionmaker, engine

def seed():
    # Clear the data table
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(Order).delete()

    # Seed the table with initial data
    initial_data = [
        Order(region='Hlavní město Praha', item_type='Electronics', price=7000),
        Order(region='Jihomoravský kraj', item_type='Clothing', price=18950),
        Order(region='Středočeský kraj', item_type='Tools', price=15060),
        Order(region='Moravskoslezský kraj', item_type='Books', price=27699),
        Order(region='Jihočeský kraj', item_type='Home Appliances', price=21997),
        Order(region='Plzeňský kraj', item_type='Other', price=27352),
        Order(region='Olomoucký kraj', item_type='Jewelry', price=17234),
        Order(region='Ústecký kraj', item_type='Toys', price=15477),
        Order(region='Liberecký kraj', item_type='Food', price=28543),
        Order(region='Karlovarský kraj', item_type='Furniture', price=8711),
        Order(region='Pardubický kraj', item_type='Sports Equipment', price=2076),
        Order(region='Kraj Vysočina', item_type='Electronics', price=12345),
        Order(region='Karlovarský kraj', item_type='Clothing', price=29814),
        Order(region='Středočeský kraj', item_type='Home Appliances', price=29850),
        Order(region='Olomoucký kraj', item_type='Books', price=24319),
        Order(region='Ústecký kraj', item_type='Furniture', price=18843),
        Order(region='Liberecký kraj', item_type='Jewelry', price=29459),
        Order(region='Plzeňský kraj', item_type='Food', price=21314),
        Order(region='Jihomoravský kraj', item_type='Tools', price=13789),
        Order(region='Pardubický kraj', item_type='Toys', price=24962),
        Order(region='Moravskoslezský kraj', item_type='Sports Equipment', price=29213),
        Order(region='Zlínský kraj', item_type='Other', price=28547),
        Order(region='Královéhradecký kraj', item_type='Electronics', price=28165),
        Order(region='Zlínský kraj', item_type='Clothing', price=13579),
        Order(region='Kraj Vysočina', item_type='Furniture', price=9502),
        Order(region='Hlavní město Praha', item_type='Books', price=23451),
        Order(region='Karlovarský kraj', item_type='Jewelry', price=18753),
        Order(region='Moravskoslezský kraj', item_type='Food', price=27198),
        Order(region='Středočeský kraj', item_type='Electronics', price=22677),
        Order(region='Ústecký kraj', item_type='Clothing', price=15782),
        Order(region='Jihočeský kraj', item_type='Tools', price=29536),
        Order(region='Pardubický kraj', item_type='Books', price=18190),
        Order(region='Kraj Vysočina', item_type='Home Appliances', price=26193),
        Order(region='Liberecký kraj', item_type='Other', price=11477),
        Order(region='Hlavní město Praha', item_type='Jewelry', price=21865),
        Order(region='Zlínský kraj', item_type='Toys', price=19843),
        Order(region='Olomoucký kraj', item_type='Sports Equipment', price=23016),
        Order(region='Moravskoslezský kraj', item_type='Electronics', price=19275),
        Order(region='Karlovarský kraj', item_type='Food', price=16537),
        Order(region='Jihomoravský kraj', item_type='Furniture', price=25314)
    ]

    session.add_all(initial_data)
    session.commit()
    session.close()
    
    print("Orders seeded successfully.")
