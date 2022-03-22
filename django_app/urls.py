from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('check/token/',views.check_token, name="check_token"),

    path('login/', obtain_auth_token),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),

    path('purchased_courses/<str:token>/', views.purchased_courses, name='purchased_courses'),
    path('explore_course/', views.explore_course, name='explore_course'),
    path('watch/video/<int:id>/', views.watch_video, name='watch_video'),
    
    path('start/payment/', views.start_payment, name="payment"),
    path('payment/success/',views.handle_payment_success, name="payment_success"),

    path('purchasing/course/details/', views.purchasing_course_details, name='purchasing_course_details'),

    # path('course_detail_view/<int:id>/', views.course_detail_view, name='course_detail_view'),
    # path('star_rating/', views.star_rating, name='star_rating'),

    # ========================= Comments ==================================
    path('comments/<int:course_id>/',views.comments,name='comments'),
    path('add_comment/',views.add_comment,name='add_comment'),
    path('edit_comment/<int:comment_id>/',views.edit_comment,name='edit_comment'),
    path('delete_comment/<int:comment_id>/',views.delete_comment,name='delete_comment'),
]