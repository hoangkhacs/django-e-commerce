from django.test import TestCase

# Create your tests here.
Category.objects.filter(category_name='Văn Học').get_descendants(include_self=True)
