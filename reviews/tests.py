from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from drinks.models import Drink
from shops.models import Shop
from .models import DrinkReview, ShopReview


class ReviewModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="testpass123")
        self.shop = Shop.objects.create(name="Bean Works", is_approved=True)
        self.drink = Drink.objects.create(
            name="Flat White",
            shop=self.shop,
            drink_type=Drink.FLAT_WHITE,
            price="3.40",
        )

    def test_drink_review_overall_returns_rounded_average(self):
        review = DrinkReview.objects.create(
            user=self.user,
            drink=self.drink,
            taste=5,
            temperature=4,
            value=4,
            presentation=5,
            strength=3,
            comment="Very balanced.",
        )

        self.assertEqual(review.overall, 4.2)

    def test_drink_review_string_representation(self):
        review = DrinkReview.objects.create(
            user=self.user,
            drink=self.drink,
            taste=4,
            temperature=4,
            value=4,
            presentation=4,
            strength=4,
        )

        self.assertEqual(str(review), f"{self.user} -> {self.drink}")

    def test_shop_review_string_representation(self):
        review = ShopReview.objects.create(
            user=self.user,
            shop=self.shop,
            overall_score=5,
            review_text="Excellent service.",
        )

        self.assertEqual(str(review), f"{self.user} -> {self.shop}")

    def test_drink_review_unique_per_user_and_drink(self):
        DrinkReview.objects.create(
            user=self.user,
            drink=self.drink,
            taste=4,
            temperature=4,
            value=4,
            presentation=4,
            strength=4,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                DrinkReview.objects.create(
                    user=self.user,
                    drink=self.drink,
                    taste=3,
                    temperature=3,
                    value=3,
                    presentation=3,
                    strength=3,
                )

    def test_shop_review_unique_per_user_and_shop(self):
        ShopReview.objects.create(
            user=self.user,
            shop=self.shop,
            overall_score=4,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ShopReview.objects.create(
                    user=self.user,
                    shop=self.shop,
                    overall_score=5,
                )


class ReviewViewBaseTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="reviewer", password="testpass123")
        self.other_user = User.objects.create_user(username="other", password="testpass123")

        self.approved_shop = Shop.objects.create(
            name="Southside Roasters",
            location="Glasgow",
            description="Specialty coffee and cakes",
            owner=self.other_user,
            submitted_by=self.other_user,
            is_approved=True,
        )
        self.pending_shop = Shop.objects.create(
            name="Hidden Grounds",
            location="Edinburgh",
            description="Pending moderation",
            owner=self.other_user,
            submitted_by=self.other_user,
            is_approved=False,
        )

        self.approved_drink = Drink.objects.create(
            name="Cappuccino",
            shop=self.approved_shop,
            drink_type=Drink.CAPPUCCINO,
            price="3.60",
        )
        self.pending_drink = Drink.objects.create(
            name="Mocha",
            shop=self.pending_shop,
            drink_type=Drink.MOCHA,
            price="4.10",
        )


class AddDrinkReviewViewTests(ReviewViewBaseTestCase):
    def test_add_drink_review_redirects_anonymous_users_to_login(self):
        response = self.client.get(
            reverse("reviews:add_drink", kwargs={"drink_id": self.approved_drink.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_get_add_drink_review_creates_default_review_once(self):
        self.client.login(username="reviewer", password="testpass123")

        first_response = self.client.get(
            reverse("reviews:add_drink", kwargs={"drink_id": self.approved_drink.id})
        )
        second_response = self.client.get(
            reverse("reviews:add_drink", kwargs={"drink_id": self.approved_drink.id})
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        review = DrinkReview.objects.get(user=self.user, drink=self.approved_drink)
        self.assertEqual(DrinkReview.objects.filter(user=self.user, drink=self.approved_drink).count(), 1)
        self.assertEqual(review.taste, 3)
        self.assertEqual(review.temperature, 3)
        self.assertEqual(review.value, 3)
        self.assertEqual(review.presentation, 3)
        self.assertEqual(review.strength, 3)
        self.assertEqual(first_response.context["drink"], self.approved_drink)

    def test_post_add_drink_review_updates_existing_review(self):
        DrinkReview.objects.create(
            user=self.user,
            drink=self.approved_drink,
            taste=3,
            temperature=3,
            value=3,
            presentation=3,
            strength=3,
        )
        self.client.login(username="reviewer", password="testpass123")

        response = self.client.post(
            reverse("reviews:add_drink", kwargs={"drink_id": self.approved_drink.id}),
            {
                "taste": 5,
                "temperature": 4,
                "value": 4,
                "presentation": 5,
                "strength": 4,
                "comment": "Really smooth and creamy.",
            },
        )

        self.assertRedirects(
            response,
            reverse("drinks:detail", kwargs={"slug": self.approved_drink.slug}),
        )
        review = DrinkReview.objects.get(user=self.user, drink=self.approved_drink)
        self.assertEqual(review.taste, 5)
        self.assertEqual(review.temperature, 4)
        self.assertEqual(review.value, 4)
        self.assertEqual(review.presentation, 5)
        self.assertEqual(review.strength, 4)
        self.assertEqual(review.comment, "Really smooth and creamy.")

    def test_add_drink_review_returns_404_for_unapproved_shop_drink(self):
        self.client.login(username="reviewer", password="testpass123")

        response = self.client.get(
            reverse("reviews:add_drink", kwargs={"drink_id": self.pending_drink.id})
        )

        self.assertEqual(response.status_code, 404)


class AddShopReviewViewTests(ReviewViewBaseTestCase):
    def test_add_shop_review_redirects_anonymous_users_to_login(self):
        response = self.client.get(
            reverse("reviews:add_shop", kwargs={"shop_slug": self.approved_shop.slug})
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_get_add_shop_review_creates_default_review_once(self):
        self.client.login(username="reviewer", password="testpass123")

        first_response = self.client.get(
            reverse("reviews:add_shop", kwargs={"shop_slug": self.approved_shop.slug})
        )
        second_response = self.client.get(
            reverse("reviews:add_shop", kwargs={"shop_slug": self.approved_shop.slug})
        )

        self.assertEqual(first_response.status_code, 200)
        self.assertEqual(second_response.status_code, 200)
        review = ShopReview.objects.get(user=self.user, shop=self.approved_shop)
        self.assertEqual(ShopReview.objects.filter(user=self.user, shop=self.approved_shop).count(), 1)
        self.assertEqual(review.overall_score, 3)
        self.assertEqual(first_response.context["shop"], self.approved_shop)

    def test_post_add_shop_review_updates_existing_review(self):
        ShopReview.objects.create(user=self.user, shop=self.approved_shop, overall_score=3)
        self.client.login(username="reviewer", password="testpass123")

        response = self.client.post(
            reverse("reviews:add_shop", kwargs={"shop_slug": self.approved_shop.slug}),
            {
                "overall_score": 5,
                "review_text": "Great atmosphere and quick service.",
            },
        )

        self.assertRedirects(
            response,
            reverse("shops:detail", kwargs={"slug": self.approved_shop.slug}),
        )
        review = ShopReview.objects.get(user=self.user, shop=self.approved_shop)
        self.assertEqual(review.overall_score, 5)
        self.assertEqual(review.review_text, "Great atmosphere and quick service.")

    def test_add_shop_review_returns_404_for_unapproved_shop(self):
        self.client.login(username="reviewer", password="testpass123")

        response = self.client.get(
            reverse("reviews:add_shop", kwargs={"shop_slug": self.pending_shop.slug})
        )

        self.assertEqual(response.status_code, 404)
