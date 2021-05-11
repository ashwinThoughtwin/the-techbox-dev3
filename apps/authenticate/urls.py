from django.urls import path
from .views import LoginView,SignupView,logout_request,SetLanguage
from rest_framework_simplejwt import views as jwt_views



urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('signup', SignupView.as_view(), name="signup"),
    path("logout/",logout_request, name="logout"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('set_language/',SetLanguage.as_view(), name='set_language')
]
