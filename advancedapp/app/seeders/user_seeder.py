from db import User, sessionmaker, engine

def seed():
    # Clear the data table
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seed the users table
    user1 = User(username='user1', password='password1')
    existing_user = session.query(User).filter_by(username='user1').first()

    if not existing_user:
        session.add(user1)

    session.commit()
    session.close()
    
    print("Orders seeded successfully.")
