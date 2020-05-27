from rest_framework import routers
from report_app import views as report_views
from accounts_app import views as accounts_views


router = routers.DefaultRouter()
router.register('index', report_views.ReportViewSet)
router.register(r'operations', report_views.OperationViewSet)
router.register(r'risks', report_views.RisksViewSet)
router.register(r'users', accounts_views.UsersViewSet)
router.register(r'profile', accounts_views.ProfileViewSet)




