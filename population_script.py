import os
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.contrib.auth import get_user_model
from django.db import transaction

from accounts.models import Profile
from drinks.models import Drink
from reviews.models import DrinkReview, ShopReview
from shops.models import Shop


PASSWORD = "spillthebeans123"

USER_DATA = [
    {
        "username": "owner_emma",
        "email": "emma@example.com",
        "password": PASSWORD,
        "first_name": "Emma",
        "last_name": "Reid",
        "bio": "Shop owner who cares about smooth espresso, warm service, and consistent quality.",
    },
    {
        "username": "owner_jamie",
        "email": "jamie@example.com",
        "password": PASSWORD,
        "first_name": "Jamie",
        "last_name": "Kerr",
        "bio": "Independent café owner focused on neighbourhood coffee culture and seasonal drinks.",
    },
    {
        "username": "owner_nina",
        "email": "nina@example.com",
        "password": PASSWORD,
        "first_name": "Nina",
        "last_name": "Patel",
        "bio": "Owner and roaster who loves flat whites, single origins, and friendly local spaces.",
    },
    {
        "username": "owner_callum",
        "email": "callum@example.com",
        "password": PASSWORD,
        "first_name": "Callum",
        "last_name": "Ross",
        "bio": "Runs smaller community-focused cafés and cares about approachable menus and reliable service.",
    },
    {
        "username": "maya",
        "email": "maya@example.com",
        "password": PASSWORD,
        "first_name": "Maya",
        "last_name": "Ali",
        "bio": "Student reviewer always looking for good value coffee and quiet study spots.",
    },
    {
        "username": "rory",
        "email": "rory@example.com",
        "password": PASSWORD,
        "first_name": "Rory",
        "last_name": "Fraser",
        "bio": "Commutes through the city centre and reviews coffee based on consistency and speed.",
    },
    {
        "username": "zara",
        "email": "zara@example.com",
        "password": PASSWORD,
        "first_name": "Zara",
        "last_name": "Iqbal",
        "bio": "Likes strong coffee, neat presentation, and cafés with a good atmosphere.",
    },
    {
        "username": "lewis",
        "email": "lewis@example.com",
        "password": PASSWORD,
        "first_name": "Lewis",
        "last_name": "Campbell",
        "bio": "Weekend café hopper interested in iced drinks, espresso balance, and fair prices.",
    },
    {
        "username": "aisha",
        "email": "aisha@example.com",
        "password": PASSWORD,
        "first_name": "Aisha",
        "last_name": "Rahman",
        "bio": "Reviews cafés based on atmosphere, seating, and whether they are good for long catch-ups.",
    },
    {
        "username": "ben",
        "email": "ben@example.com",
        "password": PASSWORD,
        "first_name": "Ben",
        "last_name": "Murray",
        "bio": "Enjoys darker roasts, straightforward espresso drinks, and quick city-centre stops.",
    },
    {
        "username": "chloe",
        "email": "chloe@example.com",
        "password": PASSWORD,
        "first_name": "Chloe",
        "last_name": "Douglas",
        "bio": "Prefers sweeter drinks and likes cafés with polished presentation and friendly staff.",
    },
    {
        "username": "hamish",
        "email": "hamish@example.com",
        "password": PASSWORD,
        "first_name": "Hamish",
        "last_name": "Stewart",
        "bio": "Often explores independent coffee shops around Glasgow and rates them on consistency and value.",
    },
]


SHOP_BLUEPRINTS = [
    {
        "name": "Bean There Glasgow",
        "location": "West End, Glasgow",
        "description": "A cosy neighbourhood coffee shop with brunch pastries, warm lighting, and a calm study-friendly vibe.",
        "owner": "owner_emma",
        "submitted_by": "owner_emma",
        "is_approved": True,
        "drink_names": [
            ("Signature Flat White", Drink.FLAT_WHITE, "3.60"),
            ("House Mocha", Drink.MOCHA, "4.10"),
            ("Morning Espresso", Drink.ESPRESSO, "2.60"),
            ("Brown Sugar Iced Latte", Drink.ICED, "4.30"),
        ],
    },
    {
        "name": "Clyde Roast House",
        "location": "City Centre, Glasgow",
        "description": "A busy city-centre stop focused on fast service, strong espresso, and takeaway commuters.",
        "owner": "owner_jamie",
        "submitted_by": "owner_jamie",
        "is_approved": True,
        "drink_names": [
            ("Clyde Americano", Drink.AMERICANO, "3.20"),
            ("Oat Latte", Drink.LATTE, "3.95"),
            ("Iced Vanilla Coffee", Drink.ICED, "4.25"),
            ("Double Shot Cappuccino", Drink.CAPPUCCINO, "3.85"),
        ],
    },
    {
        "name": "Southside Sips",
        "location": "Shawlands, Glasgow",
        "description": "Relaxed southside café with a small bakery counter, friendly staff, and a focus on milk-based drinks.",
        "owner": "owner_nina",
        "submitted_by": "owner_nina",
        "is_approved": True,
        "drink_names": [
            ("Classic Cappuccino", Drink.CAPPUCCINO, "3.70"),
            ("Caramel Latte", Drink.LATTE, "4.05"),
            ("Double Espresso", Drink.ESPRESSO, "2.80"),
            ("Iced Honey Latte", Drink.ICED, "4.35"),
        ],
    },
    {
        "name": "Merchant Grind",
        "location": "Merchant City, Glasgow",
        "description": "Modern central café with bright interiors, strong Wi-Fi, and a menu built around everyday favourites.",
        "owner": "owner_jamie",
        "submitted_by": "owner_jamie",
        "is_approved": True,
        "drink_names": [
            ("Merchant Flat White", Drink.FLAT_WHITE, "3.75"),
            ("Hazelnut Mocha", Drink.MOCHA, "4.35"),
            ("Cold Brew", Drink.ICED, "4.10"),
            ("Daily Latte", Drink.LATTE, "3.90"),
        ],
    },
    {
        "name": "Hidden Lane Coffee Lab",
        "location": "Finnieston, Glasgow",
        "description": "Small-batch coffee bar with rotating beans, stronger espresso profiles, and a slightly more specialist feel.",
        "owner": "owner_nina",
        "submitted_by": "owner_nina",
        "is_approved": True,
        "drink_names": [
            ("Single Origin Espresso", Drink.ESPRESSO, "3.00"),
            ("Honey Cinnamon Latte", Drink.LATTE, "4.20"),
            ("Iced Americano", Drink.ICED, "3.80"),
            ("Velvet Flat White", Drink.FLAT_WHITE, "3.95"),
        ],
    },
    {
        "name": "Riverside Brew Bar",
        "location": "Glasgow Green, Glasgow",
        "description": "Bright café near the river with plenty of window seats, pastries, and an easygoing all-day crowd.",
        "owner": "owner_emma",
        "submitted_by": "owner_emma",
        "is_approved": True,
        "drink_names": [
            ("Maple Latte", Drink.LATTE, "4.15"),
            ("River Roast Americano", Drink.AMERICANO, "3.25"),
            ("Iced Mocha", Drink.ICED, "4.45"),
            ("Cocoa Cappuccino", Drink.CAPPUCCINO, "3.95"),
        ],
    },
    {
        "name": "Campus Cup",
        "location": "Hillhead, Glasgow",
        "description": "Student-friendly café with lots of plug sockets, quiet weekday mornings, and good value combo deals.",
        "owner": "owner_callum",
        "submitted_by": "owner_callum",
        "is_approved": True,
        "drink_names": [
            ("Budget Flat White", Drink.FLAT_WHITE, "3.20"),
            ("Study Session Latte", Drink.LATTE, "3.65"),
            ("Night Before Espresso", Drink.ESPRESSO, "2.50"),
            ("Vanilla Iced Coffee", Drink.ICED, "3.95"),
        ],
    },
    {
        "name": "North Kelvinside Coffee Co",
        "location": "North Kelvinside, Glasgow",
        "description": "Neighbourhood café known for patient service, calm décor, and classic drinks done carefully.",
        "owner": "owner_emma",
        "submitted_by": "owner_emma",
        "is_approved": True,
        "drink_names": [
            ("House Flat White", Drink.FLAT_WHITE, "3.70"),
            ("Toffee Mocha", Drink.MOCHA, "4.25"),
            ("Long Black", Drink.AMERICANO, "3.05"),
            ("Iced Oat Latte", Drink.ICED, "4.20"),
        ],
    },
    {
        "name": "Garnet Bean Room",
        "location": "Charing Cross, Glasgow",
        "description": "Compact independent spot with strong espresso, quick service, and a stylish minimalist interior.",
        "owner": "owner_jamie",
        "submitted_by": "owner_jamie",
        "is_approved": True,
        "drink_names": [
            ("Dark Roast Espresso", Drink.ESPRESSO, "2.85"),
            ("Almond Latte", Drink.LATTE, "4.00"),
            ("Classic Americano", Drink.AMERICANO, "3.15"),
            ("Iced Caramel Coffee", Drink.ICED, "4.30"),
        ],
    },
    {
        "name": "Botanic Beans",
        "location": "Byres Road, Glasgow",
        "description": "Leafy café close to the Botanic Gardens with relaxed seating and a menu that suits long weekend visits.",
        "owner": "owner_nina",
        "submitted_by": "owner_nina",
        "is_approved": True,
        "drink_names": [
            ("Garden Latte", Drink.LATTE, "3.95"),
            ("Flat White No. 2", Drink.FLAT_WHITE, "3.80"),
            ("Mocha Supreme", Drink.MOCHA, "4.40"),
            ("Cold Oat Brew", Drink.ICED, "4.20"),
        ],
    },
    {
        "name": "Kelvin Corner Coffee",
        "location": "Partick, Glasgow",
        "description": "Newly submitted shop waiting for moderation approval.",
        "owner": "owner_callum",
        "submitted_by": "owner_callum",
        "is_approved": False,
        "drink_names": [],
    },
]


SHOP_COMMENT_OPENERS = [
    "Great atmosphere and very dependable coffee.",
    "Friendly staff and a shop I would happily revisit.",
    "Strong all-round experience with good seating and service.",
    "Really solid café with a menu that feels well thought out.",
    "Pleasant stop with coffee that tastes carefully made.",
    "A reliable place when I want something consistent and well presented.",
]

SHOP_COMMENT_CLOSERS = [
    "It feels welcoming without being noisy.",
    "The drinks arrive quickly and still feel polished.",
    "I would recommend it for both takeaway and sitting in.",
    "Good balance between quality, atmosphere, and price.",
    "It stands out compared with other nearby coffee spots.",
    "The space suits studying, chatting, or a quick coffee stop equally well.",
]

DRINK_COMMENT_OPENERS = [
    "Tasty and well balanced.",
    "Easy to drink and clearly made with care.",
    "A very solid cup overall.",
    "Nicely made and better than I expected.",
    "Really enjoyable with a good coffee flavour.",
    "Consistent and properly finished.",
]

DRINK_COMMENT_CLOSERS = [
    "The temperature was spot on.",
    "Presentation was neat and it felt worth the price.",
    "I would order this again without hesitation.",
    "It had enough strength to still taste like coffee.",
    "Good value for the portion and quality.",
    "It would be an easy recommendation from this menu.",
]


REVIEWER_USERNAMES = [
    "maya",
    "rory",
    "zara",
    "lewis",
    "aisha",
    "ben",
    "chloe",
    "hamish",
]


def rotate_reviewers(start, count):
    reviewers = []
    for offset in range(count):
        reviewers.append(REVIEWER_USERNAMES[(start + offset) % len(REVIEWER_USERNAMES)])
    return reviewers


def build_shop_reviews(shop_index, shop_name):
    reviewers = rotate_reviewers(shop_index, 5)
    reviews = []
    for review_index, username in enumerate(reviewers):
        score = 5 if (shop_index + review_index) % 4 != 0 else 4
        opener = SHOP_COMMENT_OPENERS[(shop_index + review_index) % len(SHOP_COMMENT_OPENERS)]
        closer = SHOP_COMMENT_CLOSERS[(shop_index + review_index) % len(SHOP_COMMENT_CLOSERS)]
        reviews.append(
            {
                "user": username,
                "overall_score": score,
                "review_text": f"{opener} {shop_name} has a good vibe and {closer}",
            }
        )
    return reviews


def build_drink_reviews(shop_index, drink_index, drink_name):
    reviewers = rotate_reviewers(shop_index + drink_index, 3)
    reviews = []
    for review_index, username in enumerate(reviewers):
        base = shop_index + drink_index + review_index
        taste = 5 if base % 3 != 0 else 4
        temperature = 5 if base % 4 != 0 else 4
        value = 4 if base % 5 else 5
        presentation = 4 if base % 2 == 0 else 5
        strength = 4 if drink_index % 2 == 0 else 3
        if "Espresso" in drink_name or "Long Black" in drink_name:
            strength = 5
        elif "Mocha" in drink_name:
            strength = 3
        elif "Flat White" in drink_name:
            strength = 4

        opener = DRINK_COMMENT_OPENERS[base % len(DRINK_COMMENT_OPENERS)]
        closer = DRINK_COMMENT_CLOSERS[base % len(DRINK_COMMENT_CLOSERS)]
        reviews.append(
            {
                "user": username,
                "taste": taste,
                "temperature": temperature,
                "value": value,
                "presentation": presentation,
                "strength": strength,
                "comment": f"{opener} {drink_name} was smooth and {closer}",
            }
        )
    return reviews


def build_shop_data():
    shop_data = []
    for shop_index, blueprint in enumerate(SHOP_BLUEPRINTS):
        shop = {
            "name": blueprint["name"],
            "location": blueprint["location"],
            "description": blueprint["description"],
            "owner": blueprint["owner"],
            "submitted_by": blueprint["submitted_by"],
            "is_approved": blueprint["is_approved"],
            "shop_reviews": [],
            "drinks": [],
        }

        if blueprint["is_approved"]:
            shop["shop_reviews"] = build_shop_reviews(shop_index, blueprint["name"])
            for drink_index, (drink_name, drink_type, price) in enumerate(blueprint["drink_names"]):
                shop["drinks"].append(
                    {
                        "name": drink_name,
                        "drink_type": drink_type,
                        "price": Decimal(price),
                        "reviews": build_drink_reviews(shop_index, drink_index, drink_name),
                    }
                )

        shop_data.append(shop)

    return shop_data


SHOP_DATA = build_shop_data()


def create_or_update_user(user_model, data):
    user, _ = user_model.objects.update_or_create(
        username=data["username"],
        defaults={
            "email": data["email"],
            "first_name": data["first_name"],
            "last_name": data["last_name"],
        },
    )
    user.set_password(data["password"])
    user.save()

    Profile.objects.update_or_create(
        user=user,
        defaults={
            "bio": data["bio"],
        },
    )
    return user


def create_or_update_shop(user_lookup, data):
    shop, _ = Shop.objects.update_or_create(
        name=data["name"],
        defaults={
            "location": data["location"],
            "description": data["description"],
            "owner": user_lookup[data["owner"]],
            "submitted_by": user_lookup[data["submitted_by"]],
            "is_approved": data["is_approved"],
        },
    )
    return shop


def create_or_update_drink(shop, data):
    drink, _ = Drink.objects.update_or_create(
        shop=shop,
        name=data["name"],
        defaults={
            "drink_type": data["drink_type"],
            "price": data["price"],
        },
    )
    return drink


def create_or_update_shop_review(user_lookup, shop, data):
    ShopReview.objects.update_or_create(
        user=user_lookup[data["user"]],
        shop=shop,
        defaults={
            "overall_score": data["overall_score"],
            "review_text": data["review_text"],
        },
    )


def create_or_update_drink_review(user_lookup, drink, data):
    DrinkReview.objects.update_or_create(
        user=user_lookup[data["user"]],
        drink=drink,
        defaults={
            "taste": data["taste"],
            "temperature": data["temperature"],
            "value": data["value"],
            "presentation": data["presentation"],
            "strength": data["strength"],
            "comment": data["comment"],
        },
    )


@transaction.atomic
def populate():
    user_model = get_user_model()
    user_lookup = {}

    for user_data in USER_DATA:
        user_lookup[user_data["username"]] = create_or_update_user(user_model, user_data)

    created_shops = 0
    created_drinks = 0
    created_shop_reviews = 0
    created_drink_reviews = 0

    for shop_data in SHOP_DATA:
        shop = create_or_update_shop(user_lookup, shop_data)
        created_shops += 1

        for review_data in shop_data["shop_reviews"]:
            create_or_update_shop_review(user_lookup, shop, review_data)
            created_shop_reviews += 1

        for drink_data in shop_data["drinks"]:
            drink = create_or_update_drink(shop, drink_data)
            created_drinks += 1

            for review_data in drink_data["reviews"]:
                create_or_update_drink_review(user_lookup, drink, review_data)
                created_drink_reviews += 1

    print("Spill The Beans database populated successfully.")
    print("Users/Profiles:", len(USER_DATA))
    print("Shops:", created_shops)
    print("Drinks:", created_drinks)
    print("Shop reviews:", created_shop_reviews)
    print("Drink reviews:", created_drink_reviews)
    print("\nLogin password for seeded users:", PASSWORD)
    print("Seeded usernames:", ", ".join(user_lookup.keys()))


if __name__ == "__main__":
    populate()
