from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from drinks.models import Drink
from reviews.models import ShopReview
from .models import Shop


class ShopModelTests(TestCase):
    def test_shop_generates_slug_from_name(self):
        shop = Shop.objects.create(name="River Bean", is_approved=True)

        self.assertEqual(shop.slug, "river-bean")

    def test_duplicate_shop_names_get_unique_slugs(self):
        first = Shop.objects.create(name="Daily Grind", is_approved=True)
        second = Shop.objects.create(name="Daily Grind", is_approved=True)

        self.assertEqual(first.slug, "daily-grind")
        self.assertEqual(second.slug, "daily-grind-1")

    def test_slug_falls_back_when_slugify_is_empty(self):
        shop = Shop.objects.create(name="!!!", is_approved=True)

        self.assertTrue(shop.slug)
        self.assertEqual(len(shop.slug), 8)

    def test_string_representation_is_shop_name(self):
        shop = Shop.objects.create(name="Southside Sips", is_approved=True)

        self.assertEqual(str(shop), "Southside Sips")


class ShopViewBaseTestCase(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="owner", password="testpass123")
        self.other_user = User.objects.create_user(username="other", password="testpass123")

        self.high_rated_shop = Shop.objects.create(
            name="Bean There",
            location="Glasgow",
            description="Specialty coffee",
            owner=self.owner,
            submitted_by=self.owner,
            is_approved=True,
        )
        self.low_rated_shop = Shop.objects.create(
            name="Campus Cafe",
            location="Paisley",
            description="Student friendly",
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

        ShopReview.objects.create(user=self.owner, shop=self.high_rated_shop, overall_score=5)
        ShopReview.objects.create(user=self.other_user, shop=self.high_rated_shop, overall_score=4)

        reviewer_three = User.objects.create_user(username="reviewer3", password="testpass123")
        reviewer_four = User.objects.create_user(username="reviewer4", password="testpass123")
        ShopReview.objects.create(user=reviewer_three, shop=self.low_rated_shop, overall_score=2)
        ShopReview.objects.create(user=reviewer_four, shop=self.low_rated_shop, overall_score=3)


class ShopListViewTests(ShopViewBaseTestCase):
    def test_shop_list_shows_only_approved_shops(self):
        response = self.client.get(reverse("shops:list"))

        shops = list(response.context["shops"])
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.high_rated_shop, shops)
        self.assertIn(self.low_rated_shop, shops)
        self.assertNotIn(self.pending_shop, shops)

    def test_shop_list_filters_by_query_on_name_and_location(self):
        response = self.client.get(reverse("shops:list"), {"q": "glasgow"})

        shops = list(response.context["shops"])
        self.assertEqual(shops, [self.high_rated_shop])

    def test_shop_list_filters_by_minimum_rating(self):
        response = self.client.get(reverse("shops:list"), {"rating": "4"})

        shops = list(response.context["shops"])
        self.assertEqual(shops, [self.high_rated_shop])

    def test_shop_list_ignores_invalid_rating_filter(self):
        response = self.client.get(reverse("shops:list"), {"rating": "not-a-number"})

        shops = list(response.context["shops"])
        self.assertEqual(len(shops), 2)

    def test_shop_list_can_sort_by_rating_descending(self):
        response = self.client.get(reverse("shops:list"), {"sort": "rating"})

        shops = list(response.context["shops"])
        self.assertEqual(shops[0], self.high_rated_shop)
        self.assertEqual(shops[1], self.low_rated_shop)


class ShopDetailViewTests(ShopViewBaseTestCase):
    def setUp(self):
        super().setUp()
        self.drink = Drink.objects.create(
            name="Flat White",
            shop=self.high_rated_shop,
            drink_type=Drink.FLAT_WHITE,
            price="3.50",
        )

    def test_shop_detail_returns_shop_drinks_reviews_and_average(self):
        response = self.client.get(
            reverse("shops:detail", kwargs={"slug": self.high_rated_shop.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["shop"], self.high_rated_shop)
        self.assertIn(self.drink, list(response.context["drinks"]))
        self.assertEqual(response.context["shop_reviews"].count(), 2)
        self.assertEqual(response.context["avg_shop_rating"], 4.5)

    def test_shop_detail_returns_404_for_unapproved_shop(self):
        response = self.client.get(
            reverse("shops:detail", kwargs={"slug": self.pending_shop.slug})
        )

        self.assertEqual(response.status_code, 404)


class AddShopViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="adder", password="testpass123")

    def test_add_shop_redirects_anonymous_users_to_login(self):
        response = self.client.get(reverse("shops:add"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_add_shop_creates_unapproved_shop_for_logged_in_user(self):
        self.client.login(username="adder", password="testpass123")

        response = self.client.post(
            reverse("shops:add"),
            {
                "name": "North Roast",
                "location": "Glasgow",
                "description": "A new cafe submission",
            },
        )

        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        shop = Shop.objects.get(name="North Roast")
        self.assertEqual(shop.owner, self.user)
        self.assertEqual(shop.submitted_by, self.user)
        self.assertFalse(shop.is_approved)


class EditShopViewTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(username="editor", password="testpass123")
        self.other_user = User.objects.create_user(username="intruder", password="testpass123")
        self.shop = Shop.objects.create(
            name="Old Name",
            location="Glasgow",
            description="Original description",
            owner=self.owner,
            submitted_by=self.owner,
            is_approved=True,
        )

    def test_non_owner_cannot_edit_shop(self):
        self.client.login(username="intruder", password="testpass123")

        response = self.client.post(
            reverse("shops:edit", kwargs={"slug": self.shop.slug}),
            {
                "name": "Changed Name",
                "location": "Glasgow",
                "description": "Should not save",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.name, "Old Name")

    def test_owner_can_edit_shop_and_resubmits_for_approval(self):
        self.client.login(username="editor", password="testpass123")

        response = self.client.post(
            reverse("shops:edit", kwargs={"slug": self.shop.slug}),
            {
                "name": "Updated Name",
                "location": "Paisley",
                "description": "Updated description",
            },
        )

        self.assertRedirects(
            response,
            reverse("shops:detail", kwargs={"slug": self.shop.slug}),
            fetch_redirect_response=False,
        )
        self.shop.refresh_from_db()
        self.assertEqual(self.shop.name, "Updated Name")
        self.assertEqual(self.shop.location, "Paisley")
        self.assertFalse(self.shop.is_approved)
