from decimal import Decimal
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shops.models import Shop
from drinks.models import Drink
from reviews.models import DrinkReview, ShopReview


class Command(BaseCommand):
    help = "Seed the database with demo users, shops, drinks, and reviews"

from decimal import Decimal
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shops.models import Shop
from drinks.models import Drink
from reviews.models import DrinkReview, ShopReview


class Command(BaseCommand):
    help = "Seed the database with demo users, shops, drinks, and reviews"

    def handle(self, *args, **options):
        random.seed(42)

        self.stdout.write(self.style.WARNING("Seeding demo data..."))

        # Reset demo data
        DrinkReview.objects.all().delete()
        ShopReview.objects.all().delete()
        Drink.objects.all().delete()
        Shop.objects.all().delete()

        users = []
        demo_users = [
            ("alice", "alice@example.com"),
            ("bob", "bob@example.com"),
            ("charlie", "charlie@example.com"),
            ("dana", "dana@example.com"),
            ("eva", "eva@example.com"),
        ]

        for username, email in demo_users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email},
            )
            if created:
                user.set_password("password123")
                user.save()
            users.append(user)

        owner1 = users[0]
        owner2 = users[1]
        owner3 = users[2]

        shops_data = [
            {
                "name": "Bean There",
                "description": "Independent coffee shop with cosy seating and specialty beans.",
                "location": "Glasgow City Centre",
                "owner": owner1,
            },
            {
                "name": "Roast Republic",
                "description": "Modern cafe focused on espresso and milk-based drinks.",
                "location": "West End",
                "owner": owner2,
            },
            {
                "name": "Daily Grind",
                "description": "Student-friendly coffee stop with affordable drinks.",
                "location": "University Area",
                "owner": owner3,
            },
            {
                "name": "Cloud Nine Coffee",
                "description": "Bright cafe with brunch, pastries, and iced drinks.",
                "location": "Merchant City",
                "owner": owner1,
            },
            {
                "name": "North Brew",
                "description": "Minimalist coffee bar known for strong espresso.",
                "location": "Finnieston",
                "owner": owner2,
            },
        ]

        shops = []
        for item in shops_data:
            shop, _ = Shop.objects.get_or_create(
                name=item["name"],
                defaults={
                    "description": item["description"],
                    "location": item["location"],
                    "owner": item["owner"],
                    "submitted_by": item["owner"],
                    "is_approved": True,
                },
            )
            shop.description = item["description"]
            shop.location = item["location"]
            shop.owner = item["owner"]
            shop.submitted_by = item["owner"]
            shop.is_approved = True
            shop.save()
            shops.append(shop)

        drink_templates = [
            ("Flat White", Drink.FLAT_WHITE, Decimal("3.40")),
            ("Cappuccino", Drink.CAPPUCCINO, Decimal("3.60")),
            ("Latte", Drink.LATTE, Decimal("3.75")),
            ("Espresso", Drink.ESPRESSO, Decimal("2.80")),
            ("Americano", Drink.AMERICANO, Decimal("3.10")),
            ("Mocha", Drink.MOCHA, Decimal("4.10")),
            ("Iced Coffee", Drink.ICED, Decimal("3.95")),
        ]

        drinks = []
        for shop in shops:
            for name, drink_type, price in drink_templates:
                drink, _ = Drink.objects.get_or_create(
                    name=name,
                    shop=shop,
                    defaults={
                        "drink_type": drink_type,
                        "price": price,
                    },
                )
                drink.drink_type = drink_type
                drink.price = price
                drink.save()
                drinks.append(drink)

        comments = [
            "Really smooth and balanced.",
            "Nice flavour, would order again.",
            "Good value for money.",
            "Presentation was great and tasted fresh.",
            "A bit too hot, but still enjoyable.",
            "Strong coffee taste and good texture.",
            "Could be better, but still decent.",
            "One of the better coffees I have had recently.",
            "Nice shop and friendly staff.",
            "Would definitely recommend this drink.",
        ]

        for drink in drinks:
            reviewers = random.sample(users, k=random.randint(2, min(5, len(users))))
            for user in reviewers:
                DrinkReview.objects.update_or_create(
                    user=user,
                    drink=drink,
                    defaults={
                        "taste": random.randint(2, 5),
                        "temperature": random.randint(2, 5),
                        "value": random.randint(2, 5),
                        "presentation": random.randint(2, 5),
                        "strength": random.randint(2, 5),
                        "comment": random.choice(comments),
                    },
                )

        for shop in shops:
            reviewers = random.sample(users, k=random.randint(2, min(5, len(users))))
            for user in reviewers:
                ShopReview.objects.update_or_create(
                    user=user,
                    shop=shop,
                    defaults={
                        "overall_score": random.randint(3, 5),
                        "review_text": random.choice(comments),
                    },
                )

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
        self.stdout.write("Demo login examples:")
        self.stdout.write("  alice / password123")
        self.stdout.write("  bob / password123")
        self.stdout.write("  charlie / password123")