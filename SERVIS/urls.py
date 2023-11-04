from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from mainApp.views import ChangeInfoView, CustomTokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="Avto service API Documentation",
        default_version="v1",
        description="Admin panel - /admin/ linkida \n"
                    "login: admin123, password: 123\n",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="tursunovotabekkuva@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainApp.urls')),

    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-info/', ChangeInfoView.as_view(), name='change_info'),

    path('', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0)),
]
