"""
Seed script to populate the database with test data.

Run this after applying migrations:
python scripts/seed_data.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.category import Category
from app.models.product import Product
from decimal import Decimal
import uuid


def seed_database():
    """Populate database with test categories and products."""
    db = SessionLocal()

    try:
        print("🌱 Seeding database...")

        # Check if data already exists
        existing_categories = db.query(Category).count()
        if existing_categories > 0:
            print("⚠️  Database already has data. Skipping seed.")
            return

        # Create Categories (with hierarchy)
        electronics = Category(
            id=uuid.uuid4(),
            name="Electronics",
            slug="electronics",
            parent_id=None
        )
        db.add(electronics)
        db.flush()  # Get the ID

        mobile = Category(
            id=uuid.uuid4(),
            name="Mobile Phones",
            slug="mobile-phones",
            parent_id=electronics.id
        )
        db.add(mobile)
        db.flush()

        android = Category(
            id=uuid.uuid4(),
            name="Android",
            slug="android",
            parent_id=mobile.id
        )
        db.add(android)

        ios = Category(
            id=uuid.uuid4(),
            name="iOS",
            slug="ios",
            parent_id=mobile.id
        )
        db.add(ios)

        laptops = Category(
            id=uuid.uuid4(),
            name="Laptops",
            slug="laptops",
            parent_id=electronics.id
        )
        db.add(laptops)

        clothing = Category(
            id=uuid.uuid4(),
            name="Clothing",
            slug="clothing",
            parent_id=None
        )
        db.add(clothing)

        mens = Category(
            id=uuid.uuid4(),
            name="Men's Clothing",
            slug="mens-clothing",
            parent_id=clothing.id
        )
        db.add(mens)

        womens = Category(
            id=uuid.uuid4(),
            name="Women's Clothing",
            slug="womens-clothing",
            parent_id=clothing.id
        )
        db.add(womens)

        db.commit()
        print("✅ Categories created")

        # Create Products
        products = [
            # Android Phones
            Product(
                name="Samsung Galaxy S24",
                slug="samsung-galaxy-s24",
                description="Latest Samsung flagship with AI features",
                price=Decimal("999.99"),
                stock=50,
                category_id=android.id,
                is_active=True
            ),
            Product(
                name="Google Pixel 8 Pro",
                slug="google-pixel-8-pro",
                description="Google's premium smartphone with advanced camera",
                price=Decimal("899.99"),
                stock=30,
                category_id=android.id,
                is_active=True
            ),
            Product(
                name="OnePlus 12",
                slug="oneplus-12",
                description="Flagship killer with incredible specs",
                price=Decimal("699.99"),
                stock=40,
                category_id=android.id,
                is_active=True
            ),
            # iOS Phones
            Product(
                name="iPhone 15 Pro Max",
                slug="iphone-15-pro-max",
                description="Apple's premium flagship with titanium design",
                price=Decimal("1199.99"),
                stock=60,
                category_id=ios.id,
                is_active=True
            ),
            Product(
                name="iPhone 15",
                slug="iphone-15",
                description="Standard iPhone with dynamic island",
                price=Decimal("799.99"),
                stock=80,
                category_id=ios.id,
                is_active=True
            ),
            # Laptops
            Product(
                name="MacBook Pro 16\"",
                slug="macbook-pro-16",
                description="Professional laptop with M3 Max chip",
                price=Decimal("2499.99"),
                stock=20,
                category_id=laptops.id,
                is_active=True
            ),
            Product(
                name="Dell XPS 15",
                slug="dell-xps-15",
                description="Premium Windows laptop for creators",
                price=Decimal("1799.99"),
                stock=25,
                category_id=laptops.id,
                is_active=True
            ),
            Product(
                name="ThinkPad X1 Carbon",
                slug="thinkpad-x1-carbon",
                description="Business ultrabook with legendary keyboard",
                price=Decimal("1499.99"),
                stock=15,
                category_id=laptops.id,
                is_active=True
            ),
            # Clothing
            Product(
                name="Men's Cotton T-Shirt",
                slug="mens-cotton-tshirt",
                description="Comfortable everyday t-shirt",
                price=Decimal("19.99"),
                stock=200,
                category_id=mens.id,
                is_active=True
            ),
            Product(
                name="Men's Denim Jeans",
                slug="mens-denim-jeans",
                description="Classic blue jeans",
                price=Decimal("49.99"),
                stock=150,
                category_id=mens.id,
                is_active=True
            ),
            Product(
                name="Women's Summer Dress",
                slug="womens-summer-dress",
                description="Floral summer dress",
                price=Decimal("39.99"),
                stock=100,
                category_id=womens.id,
                is_active=True
            ),
            Product(
                name="Women's Yoga Pants",
                slug="womens-yoga-pants",
                description="Comfortable activewear",
                price=Decimal("29.99"),
                stock=180,
                category_id=womens.id,
                is_active=True
            ),
            # Out of stock product
            Product(
                name="iPhone 14 Pro (Out of Stock)",
                slug="iphone-14-pro",
                description="Previous generation iPhone",
                price=Decimal("999.99"),
                stock=0,
                category_id=ios.id,
                is_active=True
            ),
        ]

        db.bulk_save_objects(products)
        db.commit()
        print(f"✅ {len(products)} products created")

        print("\n🎉 Database seeded successfully!")
        print(f"\n📊 Summary:")
        print(f"   Categories: {db.query(Category).count()}")
        print(f"   Products: {db.query(Product).count()}")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
