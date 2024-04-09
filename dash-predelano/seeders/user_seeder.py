from db import User, Session, engine

def seed():
    # Clear the data table
    with Session(engine) as session:
        # Seed the users table
        user1 = User(username='user1', password='password1')
        existing_user = session.query(User).filter_by(username='user1').first()

        if not existing_user:
            session.add(user1)

        session.commit()

    
    print("Orders seeded successfully.")