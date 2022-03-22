from django.contrib import admin
from django.urls import path, include
from rest_framework import views
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def api_over_view(request):
    data = [
        {
            'DEFAULT ADMIN PANEL': '/admin/',
        },
        {
            'STUDENT': '',
            'Login': '/api/v1/student/login/',
            'Register': '/api/v1/student/register/',
            'Logout': '/api/v1/student/logout/',
            'Check token': '/api/v1/student/check/token/',
            'Home': '/api/v1/student/home/',
            'Explore course view': '/api/v1/student/explore_course/',
            'Watch video': '/api/v1/student/watch/video/<int:id>/',
            'Purchased courses': '/api/v1/student/purchased_courses/<token>/',
            'Purchasing course details': '/api/v1/student/purchasing/course/details/',
            'Start payment': '/api/v1/student/start/payment/',
            'Handle payment': '/api/v1/student/payment/success/',

            # 'Course detail view': '/api/v1/student/course_detail_view/<id>/',
            # 'Star rating': '/api/v1/student/star_rating/',
            # 'Search filter': '/api/v1/student/search_filter/<keyword>/',
            # 'Comments': '/api/v1/student/comments/<courseid>/',
            # 'Add comment': '/api/v1/student/add_comment/<courseid>/',
            # 'Edit comment': '/api/v1/student/edit_comment/<courseid>/',
            # 'Delete comment': '/api/v1/student/delete_comment/<courseid>/',
            # 'Cart': '/api/v1/student/cart/<token>/',
            # 'Add to cart': '/api/v1/student/add_to_cart/<courseid>/',
            # 'Delete cart': '/api/v1/student/delete_cart/',
        }

        # {
            # 'ADMIN':'',
            # 'Dashboard': '/api/v1/admin/dashboard/',
            # 'Course': '/api/v1/admin/course/',
            # 'Add course': '/api/v1/admin/add_course/',
            # 'Edit course': '/api/v1/admin/edit_course/<id>/',
            # 'Delete course': '/api/v1/admin/delete_course/<id>/',
            # 'University': '/api/v1/admin/university/',
            # 'Add university': '/api/v1/admin/add_university/',
            # 'Edit university': '/api/v1/admin/edit_university/<id>/',
            # 'Delete university': '/api/v1/admin/delete_university/<id>/',
            # 'Comments': '/api/v1/admin/comments/',
            # 'View branch': '/api/v1/admin/view_branch/',
            # 'Add branch': '/api/v1/admin/add_branch/',
            # 'Edit branch': '/api/v1/admin/edit_branch/<id>/',
            # 'Delete branch': '/api/v1/admin/delete_branch/<id>/',
            # 'Admin login': '/api/v1/admin/admin_login/',
            # 'Users': '/api/v1/admin/users/',
            # 'Block user': '/api/v1/admin/block_user/<token>/',
            # 'Unblock user': '/api/v1/admin/unblock_user/<token>/',
        # }
    ]
    return Response(data, status=200)

urlpatterns = [
    path('', api_over_view, name="api_over_view"),
    path('admin/', admin.site.urls),
    path('api/v1/student/', include('django_app.urls')),
    # path('api/v1/admin/', include('admin_panel.urls')),
    # path('api/v1/accounts/', include('allauth.urls')),
]
