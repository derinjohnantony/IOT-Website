from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/new/savegroup", views.savegroup, name="savegroup"),
    path("dashboard/listgroup/new/savegroup", views.savegroup, name="savegroup"),
    path("dashboard/new/saveitem", views.saveitem, name="saveitem"),
    path("dashboard/listgroup/new/saveitem", views.saveitem, name="saveitem"),
    path("dashboard/listgroup/<gpid>", views.listgroup, name="listgroup"),
    path("dashboard/deletegroup/<gpid>", views.deletegroup, name="deletegroup"),
    path("dashboard/deleteitem/<gpid>", views.deleteitem, name="deleteitem"),

    path("dashboard/changestatus/<gpid>", views.changestatus, name="changestatus"),
    path("dashboard/changepassword", views.changepassword, name="changepassword"),
    path("signup", views.signup, name="signup"),
    path("signin", views.signin, name="signin"),
    path("dashboard/new/logout", views.logout_view, name="logout"),
    path("dashboard/listgroup/new/logout", views.logout_view, name="logout"),
]