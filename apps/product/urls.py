
from django.urls import path,include
from .views import Index,EmpListView,ItemListView,AddEmployee,EmpDelete,EmpUpdate,ItemDelete,ItemAssigns,ItemAssignsDelete,ItemListApiView,ItemAssignApiView
from rest_framework.routers import DefaultRouter
from . import views
from django.utils.translation import gettext_lazy as _

router = DefaultRouter()
router.register('assign-item',views.ItemAssignApiView)
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('',Index.as_view(),name = 'home'),
    path('api/assign/',include(router.urls)),
    path('emplist/', EmpListView.as_view(),name = 'emplist'),
    path("update/<int:pk>/", EmpUpdate.as_view(), name="update"),
    path('delete/<int:pk>/', EmpDelete.as_view(), name="delete"),
    path('addemp/', AddEmployee.as_view(), name="addemployee"),
    path('itemlist/', ItemListView.as_view(), name="itemlist"),
    path('itemdelete/',ItemDelete.as_view(), name="itemdelete"),
    path("item-assign/", ItemAssigns.as_view(), name="item-assign"),
    path('delete-items/<int:pk>',ItemAssignsDelete.as_view(), name="delete-items"),
    path('api/item',ItemListApiView.as_view(), name = 'get-items'),
    path('api/item/<int:pk>/',ItemListApiView.as_view(),name='single-items'),
    path('charge', views.Charge.as_view(), name='charge'),
    path('success/', views.Success.as_view(), name='success'),
    path('purchase/', views.PurchasePage.as_view(), name='purchase'),
]