from django.urls import path
from . import views

urlpatterns = [
    # Login/Register Routes
    path('', views.index),
    path('index', views.index),
    path('register', views.register),
    path('login', views.login),
    path('handle_login', views.handle_login),
    path('logout', views.logout),

    # Pet Motel Routes
    path('add_pet',views.add_pet),
    path('handle_add_pet', views.handle_add_pet),
    path('delete_pet/<int:id>', views.delete_pet),
    path('book_pet_get', views.book_pet_get),
    path('book_pet', views.book_pet),
    path('book_cancel/<int:id>', views.book_cancel),
    # path('invoice_view/<int:id>', views.invoice_view),

]