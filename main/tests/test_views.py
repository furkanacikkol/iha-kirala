from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import IHA, Rental

class MainViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_superuser(username='testuser', password='testpassword')

        # Create a test IHA
        self.iha = IHA.objects.create(
            brand='TestBrand',
            model='TestModel',
            weight='200',
            range='100',
            payload_capacity='250',
            max_speed='500',
            category='TestCategory'
        )

        # Create a test Rental
        self.rental = Rental.objects.create(
            iha=self.iha,
            user=self.user,
            start_datetime='2023-01-01T00:00:00',
            end_datetime='2023-01-02T00:00:00'
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to the homepage

    def test_iha_list_view(self):
        response = self.client.get(reverse('iha-list'))
        self.assertEqual(response.status_code, 200)

    # Add more test cases for other views as needed

    def test_insert_iha_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('insert-iha'), {
            'brand': 'NewBrand',
            'model': 'NewModel',
            'weight': '10',
            'range': '20',
            'payload_capacity': '30',
            'max_speed': '40',
            'category': 'NewCategory',
        },follow=True)
        self.assertEqual(response.status_code, 200)  # Beklenen durum 302, çünkü yönlendirme yapılıyor

    def test_edit_iha_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('edit-iha', args=[self.iha.id]), {
            'brand': 'UpdatedBrand',
            'model': 'UpdatedModel',
            'weight': '250',
            'range': '400',
            'payload_capacity': '300',
            'max_speed': '1000',
            'category': 'UpdatedCategory',
        })
        self.assertEqual(response.status_code, 302)  # Redirects to iha-list


    def test_delete_iha_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete-iha', args=[self.iha.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to iha-list

    def test_iha_rental_list_view(self):
        response = self.client.get(reverse('iha-rental-list'))
        self.assertEqual(response.status_code, 200)

    # Add more test cases for other views as needed

    def test_iha_rental_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('iha-rental'), {'iha_id': self.iha.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'İHA kiralama başarılı!')

    # Add more test cases for other views as needed

    def test_cancel_rental_view(self):
        self.client.force_login(self.user)
        response = self.client.post(reverse('cancel-rental'), {'rental_id': self.rental.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'İHA kiralama başarılıyla iptal edildi.')

    # Add more test cases for other views as needed

    def test_user_rentals_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('user-rentals'))
        self.assertEqual(response.status_code, 200)

    def test_rental_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('rental-list'))
        self.assertEqual(response.status_code, 200)
