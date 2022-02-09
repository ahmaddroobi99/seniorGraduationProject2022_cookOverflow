from ProfilePage.viewsets import CookerViewset
from rest_framework import routers

router = routers.DefaultRouter()
router.register('cooker', CookerViewset, basename='cooker')