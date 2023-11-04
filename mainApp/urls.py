from django.urls import path
from .views import MahsulotlarListCreateAPIView, MahsulotTurlariListCreateAPIView, MijozlarListCreateAPIView, \
    MahsulotDetailsAPIView, MahsulotTuriDetailsAPIView, MijozDetailsAPIView, SavdoDetailsAPIView, \
    SavdolarListCreateAPIView, ChiqimlarListCreateAPIView, ChiqimDetailsAPIView, UsersListAPIView, UserAPIView, \
    StatsAPIView, StatsSavdolarAPIView, StatsChiqimlarAPIView, StatsMijozlarAPIView

urlpatterns = [
    path('userlar/', UsersListAPIView.as_view()),
    path('user/<int:pk>/', UserAPIView.as_view()),

    path('mahsulot_turlari/', MahsulotTurlariListCreateAPIView.as_view()),
    path('mahsulot_turi/<int:pk>/', MahsulotTuriDetailsAPIView.as_view()),

    path('mahsulotlar/', MahsulotlarListCreateAPIView.as_view()),
    path('mahsulot/<int:pk>/', MahsulotDetailsAPIView.as_view()),

    path('mijozlar/', MijozlarListCreateAPIView.as_view()),
    path('mijoz/<int:pk>/', MijozDetailsAPIView.as_view()),

    path('savdolar/', SavdolarListCreateAPIView.as_view()),
    path('savdo/<int:pk>/', SavdoDetailsAPIView.as_view()),

    path('chiqimlar/', ChiqimlarListCreateAPIView.as_view()),
    path('chiqim/<int:pk>/', ChiqimDetailsAPIView.as_view()),

    path('stats/', StatsAPIView.as_view()),
    path('stats/savdolar/', StatsSavdolarAPIView.as_view()),
    path('stats/chiqimlar/', StatsChiqimlarAPIView.as_view()),
    path('stats/mijozlar/', StatsMijozlarAPIView.as_view()),
]