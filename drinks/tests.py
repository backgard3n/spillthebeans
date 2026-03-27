from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from reviews.models import DrinkReview
from shops.models import Shop
from .models import Drink


class DrinkModelTests(TestCase):
    def setUp(self):
        self.shop = Shop.objects.create(name="North Roast", is_approved=True)

    def test_drink_generates_slug_from_name_and_shop(self):
        drink = Drink.objects.create(
            name="Flat White",
            shop=self.shop,
            drink_type=Drink.FLAT_WHITE,
            price="3.50",
        )

        self.assertEqual(drink.slug, "flat-white-north-roast")

    def test_duplicate_base_slugs_get_unique_suffix(self):
        matching_shop = Shop.objects.create(name="North Roast", is_approved=True)
        first = Drink.objects.create(name="Mocha", shop=self.shop, drink_type=Drink.MOCHA)
        second = Drink.objects.create(name="Mocha", shop=matching_shop, drink_type=Drink.MOCHA)

        self.assertEqual(first.slug, "mocha-north-roast")
        self.assertEqual(second.slug, "mocha-north-roast-2")

    def test_slug_falls_back_when_slugify_is_empty(self):
        nameless_shop = Shop.objects.create(name="!!!", is_approved=True)
        drink = Drink.objects.create(name="!!!", shop=nameless_shop, drink_type=Drink.OTHER)

        self.assertTrue(drink.slug)
        self.assertEqual(len(drink.slug), 8)

    def test_string_representation_includes_drink_and_shop(self):
        drink = Drink.objects.create(name="Latte", shop=self.shop, drink_type=Drink.LATTE)

        self.assertEqual(str(drink), "Latte @ North Roast")


class DrinkViewBaseTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="testpass123")
        self.other_user = User.objects.create_user(username="other", password="testpass123")
        self.staff_user = User.objects.create_user(
            username="staff", password="testpass123", is_staff=True
        )

        self.approved_shop = Shop.objects.create(
            name="Bean Works",
            location="Glasgow",
            description="Specialty coffee",
            owner=self.owner,
            submitted_by=self.owner,
            is_approved=True,
        )
        self.second_shop = Shop.objects.create(
            name="Southside Sips",
            location="Paisley",
            description="Neighbourhood cafe",
            owner=self.owner,
            submitted_by=self.owner,
            is_approved=True,
        )
        self.pending_shop = Shop.objects.create(
            name="Hidden Grounds",
            location="Edinburgh",
            description="Pending moderation",
            owner=self.owner,
            submitted_by=self.owner,
            is_approved=False,
        )

        self.high_rated_drink = Drink.objects.create(
            name="Flat White",
            shop=self.approved_shop,
            drink_type=Drink.FLAT_WHITE,
            price="3.60",
        )
        self.low_rated_drink = Drink.objects.create(
            name="Iced Latte",
            shop=self.second_shop,
            drink_type=Drink.ICED,
            price="4.10",
        )
        self.no_review_drink = Drink.objects.create(
            name="Americano",
            shop=self.approved_shop,
            drink_type=Drink.AMERICANO,
            price="2.90",
        )
        self.pending_drink = Drink.objects.create(
            name="Secret Mocha",
            shop=self.pending_shop,
            drink_type=Drink.MOCHA,
            price="4.50",
        )

        DrinkReview.objects.create(
            user=self.owner,
            drink=self.high_rated_drink,
            taste=5,
            temperature=4,
            value=4,
            presentation=5,
            strength=4,
            comment="Really smooth.",
        )
        DrinkReview.objects.create(
            user=self.other_user,
            drink=self.high_rated_drink,
            taste=4,
            temperature=4,
            value=5,
            presentation=4,
            strength=4,
            comment="Great balance.",
        )
        extra_reviewer = User.objects.create_user(username="third", password="testpass123")
        DrinkReview.objects.create(
            user=extra_reviewer,
            drink=self.low_rated_drink,
            taste=2,
            temperature=3,
            value=2,
            presentation=3,
            strength=2,
            comment="Not for me.",
        )


class DrinkListViewTests(DrinkViewBaseTestCase):
    def test_drink_list_shows_only_drinks_from_approved_shops(self):
        response = self.client.get(reverse("drinks:list"))

        drinks = list(response.context["drinks"])
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.high_rated_drink, drinks)
        self.assertIn(self.low_rated_drink, drinks)
        self.assertIn(self.no_review_drink, drinks)
        self.assertNotIn(self.pending_drink, drinks)

    def test_drink_list_filters_by_shop_type_and_query(self):
        response = self.client.get(
            reverse("drinks:list"),
            {
                "shop": self.approved_shop.slug,
                "drink_type": Drink.FLAT_WHITE,
                "q": "bean",
            },
        )

        drinks = list(response.context["drinks"])
        self.assertEqual(drinks, [self.high_rated_drink])

    def test_drink_list_filters_by_minimum_rating(self):
        response = self.client.get(reverse("drinks:list"), {"rating": "4"})

        drinks = list(response.context["drinks"])
        self.assertEqual(drinks, [self.high_rated_drink])

    def test_drink_list_ignores_invalid_rating_filter(self):
        response = self.client.get(reverse("drinks:list"), {"rating": "not-a-number"})

        drinks = list(response.context["drinks"])
        self.assertEqual(len(drinks), 3)

    def test_drink_list_can_sort_by_top_rated_and_price(self):
        top_rated_response = self.client.get(reverse("drinks:list"), {"sort": "top_rated"})
        price_low_response = self.client.get(reverse("drinks:list"), {"sort": "price_low"})
        price_high_response = self.client.get(reverse("drinks:list"), {"sort": "price_high"})

        top_rated = list(top_rated_response.context["drinks"])
        price_low = list(price_low_response.context["drinks"])
        price_high = list(price_high_response.context["drinks"])

        self.assertEqual(top_rated[0], self.high_rated_drink)
        self.assertEqual(price_low[0], self.no_review_drink)
        self.assertEqual(price_high[0], self.low_rated_drink)

    def test_ajax_drink_list_returns_partial_template(self):
        response = self.client.get(
            reverse("drinks:list"),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "drinks/_drink_results.html")


class DrinkDetailViewTests(DrinkViewBaseTestCase):
    def test_drink_detail_returns_drink_reviews_and_average(self):
        response = self.client.get(
            reverse("drinks:detail", kwargs={"slug": self.high_rated_drink.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["drink"], self.high_rated_drink)
        self.assertEqual(response.context["reviews"].count(), 2)
        self.assertEqual(response.context["overall"], 4.3)

    def test_drink_detail_returns_none_when_no_reviews_exist(self):
        response = self.client.get(
            reverse("drinks:detail", kwargs={"slug": self.no_review_drink.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["overall"])

    def test_drink_detail_returns_404_for_drink_in_unapproved_shop(self):
        response = self.client.get(
            reverse("drinks:detail", kwargs={"slug": self.pending_drink.slug})
        )

        self.assertEqual(response.status_code, 404)


class AddDrinkViewTests(DrinkViewBaseTestCase):
    def test_add_drink_redirects_anonymous_users_to_login(self):
        response = self.client.get(
            reverse("drinks:add", kwargs={"shop_slug": self.approved_shop.slug})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_non_owner_cannot_add_drink(self):
        self.client.login(username="other", password="testpass123")

        response = self.client.post(
            reverse("drinks:add", kwargs={"shop_slug": self.approved_shop.slug}),
            {
                "name": "Espresso",
                "drink_type": Drink.ESPRESSO,
                "price": "2.50",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("shops:detail", kwargs={"slug": self.approved_shop.slug}),
        )
        self.assertFalse(Drink.objects.filter(name="Espresso", shop=self.approved_shop).exists())

    def test_owner_can_add_drink_to_approved_shop(self):
        self.client.login(username="owner", password="testpass123")

        response = self.client.post(
            reverse("drinks:add", kwargs={"shop_slug": self.approved_shop.slug}),
            {
                "name": "Espresso",
                "drink_type": Drink.ESPRESSO,
                "price": "2.50",
            },
        )

        drink = Drink.objects.get(name="Espresso", shop=self.approved_shop)
        self.assertRedirects(
            response,
            reverse("drinks:detail", kwargs={"slug": drink.slug}),
        )
        self.assertEqual(drink.shop, self.approved_shop)
        self.assertEqual(drink.drink_type, Drink.ESPRESSO)

    def test_staff_user_can_add_drink_even_if_not_owner(self):
        self.client.login(username="staff", password="testpass123")

        response = self.client.post(
            reverse("drinks:add", kwargs={"shop_slug": self.approved_shop.slug}),
            {
                "name": "Cappuccino",
                "drink_type": Drink.CAPPUCCINO,
                "price": "3.20",
            },
        )

        drink = Drink.objects.get(name="Cappuccino", shop=self.approved_shop)
        self.assertRedirects(
            response,
            reverse("drinks:detail", kwargs={"slug": drink.slug}),
        )

    def test_add_drink_returns_404_for_unapproved_shop(self):
        self.client.login(username="owner", password="testpass123")

        response = self.client.get(
            reverse("drinks:add", kwargs={"shop_slug": self.pending_shop.slug})
        )

        self.assertEqual(response.status_code, 404)
