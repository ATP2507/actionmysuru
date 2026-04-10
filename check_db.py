from app.database import SessionLocal
from app.models import Volunteer, Admin
db = SessionLocal()
print("=== ADMINS ===")
for a in db.query(Admin).all():
    print(a.id, a.username)
print("=== VOLUNTEERS ===")
for v in db.query(Volunteer).all():
    print(v.id, v.full_name, v.email)
