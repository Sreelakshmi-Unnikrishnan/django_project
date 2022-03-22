from .serializers import *
from .models import *
from rest_framework.decorators import api_view

from rest_framework.authtoken.views import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

from .models import *
from django.contrib.auth import logout as auth_logout

import re
import json
import environ
import razorpay

env = environ.Env()

@api_view(['POST'])
def register(request): 
    if request.method == 'POST':
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            
            user = User.objects.create_user(user_serializer.data['username'], user_serializer.data['email'], user_serializer.data['password'])

            try:
                user = User.objects.get(username=user_serializer.data['username'])
            except:
                return Response({"Error": "Invalid credentials!"}, status=status.HTTP_403_FORBIDDEN) 
        
            token = Token.objects.create(user=user)
            data = {"Token": token.key}
            return Response(data, status=status.HTTP_200_OK)
        data = {'Error':'User already exist!'}
        return Response(data, status=status.HTTP_201_CREATED)
    
@api_view(['GET']) 
def logout(request):
    auth_logout(request)
    data = {'Success': 'Sucessfully logged out'}
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
def home(request): 
    if request.method == 'GET':
        try:
            branch = Department.objects.filter(active=True)
            branch_serializer = DepartmentSerializer(branch, many = True)
            return Response(branch_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_403_FORBIDDEN) 

@api_view(['POST'])
def check_token(request):
    if request.method == 'POST':
        try:
            token = request.data['token']
        except KeyError:
            return Response({"Error": "Token not provided!"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user_token = Token.objects.get(key=token)
            if user_token:
                return Response({"Message": "ok"}, status=status.HTTP_200_OK) 
        except Token.DoesNotExist:
            return Response({"Error": "Invalid token!"}, status=status.HTTP_403_FORBIDDEN) 

@api_view(['POST']) 
def explore_course(request): 
    if request.method == 'POST':
        try:
            university = request.data['university']
        except KeyError:
            return Response({"Error": "Select university"}, status=status.HTTP_403_FORBIDDEN) 

        try:
            department = request.data['department']
        except KeyError:
            return Response({"Error": "Select department"}, status=status.HTTP_403_FORBIDDEN) 

        try:
            semester = request.data['semester']
        except KeyError:
            return Response({"Error": "Select semester"}, status=status.HTTP_403_FORBIDDEN) 

        try:
            subject = request.data['subject']
        except KeyError:
            return Response({"Error": "Select subject"}, status=status.HTTP_403_FORBIDDEN) 

        course = Course.objects.filter(
            university__university__icontains=university, 
            department__department__icontains=department,
            semester__semester__icontains=semester,
            video__subject__subject__icontains=subject,
            active=True)
        print("---", course.count())
        if course.count() <= 0:
            return Response({"Message": "Result not found"}, status=status.HTTP_200_OK)
        course_serializer = CourseSerializer(course, many=True)
        return Response(course_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST']) 
def purchased_courses(request, token):
    if request.method == 'GET':
        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            token = None
            return Response({"Error": "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            purchased_course = PurchasedCourse.objects.filter(user__id=token.user_id).order_by("-id")   
            purchased_course_serializer = PurchasedCourseSerializer(purchased_course, many=True)
            return Response(purchased_course_serializer.data, status=status.HTTP_200_OK) 
        except:
            return Response({"Error": "Somthing went wrong!"}, status=status.HTTP_400_BAD_REQUEST)      
            
    if request.method == 'POST':
        try:
            university = request.data['university']
        except KeyError:
            return Response({"Error": "University not provided!"}, status=status.HTTP_400_BAD_REQUEST) 

        try:
            department = request.data['department']
        except KeyError:
            return Response({"Error": "Department not provided!"}, status=status.HTTP_400_BAD_REQUEST) 
            
        try:
            semester = request.data['semester']
        except KeyError:
            return Response({"Error": "Semester not provided!"}, status=status.HTTP_400_BAD_REQUEST) 
            
        try:
            subject = request.data['subject']
        except KeyError:
            return Response({"Error": "Subject not provided!"}, status=status.HTTP_400_BAD_REQUEST) 
        try:
            module = request.data['module']
        except KeyError:
            return Response({"Error": "Module not provided!"}, status=status.HTTP_400_BAD_REQUEST) 

        try:
            university_query = University.objects.get(university=university)
        except University.DoesNotExist:
            return Response({"Error": "University does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        try:        
            department_query = Department.objects.get(department=department)
        except Department.DoesNotExist:
            return Response({"Error": "department does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        courses = Course.objects.filter(
            university=university_query,
            department=department_query,
            semester=semester,
            subject=subject,
            module=module
            ).order_by('id')

        course_serializer = CourseSerializer(courses, many=True)
        return Response(course_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def purchasing_course_details(request):
    if request.method == 'POST':
        try:
            university = request.data['university']
        except KeyError:
            return Response({"Error": "University not provided!"}, status=status.HTTP_403_FORBIDDEN)

        try:
            branch = request.data['branch']
        except KeyError:
            return Response({"Error": "Branch not provided!"}, status=status.HTTP_403_FORBIDDEN)

        try:
            semester = request.data['semester']
        except KeyError:
            return Response({"Error": "Semester not provided!"}, status=status.HTTP_403_FORBIDDEN)


        courses = Course.objects.filter(university__university=university, branch__title=branch, semester=semester)
        subject_count = 0
        module_count = 0
        videos_count = courses.count()

        subject_dict = {}
        for course in courses:
            subject_dict[course.subject] = 0

        for sb_dic in subject_dict.keys():
            subject_count += 1

        module_dict = {}
        for course in courses:
            module_dict[course.module] = 0

        for sb_dic in module_dict.keys():
            module_count += 1
        
        data = {'subjects': subject_count, 'modules':module_count, 'videos': videos_count}
        return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
def watch_video(request, id):
    try:
        course = Course.objects.get(id=id)
    except Course.DoesNotExist:
        return Response({"Error": "Course does not exist!"}, status=status.HTTP_200_OK)
    course_serializer = CourseSerializer(course)
    return Response(course_serializer.data, status=status.HTTP_200_OK)

environ.Env.read_env()
@api_view(['POST'])
def start_payment(request):
    try:
        token = request.data['token']
    except KeyError:
        return Response({'Error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        university = request.data['university']
    except KeyError:
        return Response({'Error': 'University not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        branch = request.data['branch']
    except KeyError:
        return Response({'Error': 'Branch not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        semester = request.data['semester']
    except KeyError:
        return Response({'Error': 'Semester not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        amount = request.data['amount']
    except KeyError:
        return Response({'Error': 'Amount not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token = Token.objects.get(key=token)
        user = User.objects.get(id=token.user_id)
    except:
        return Response({'Error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
  
    try:
        university_qry = University.objects.get(university=university)
    except University.DoesNotExist:
        return Response({'Error': 'Invalid provided data of university'}, status=status.HTTP_400_BAD_REQUEST)
        
    try:
        branch_qry = Department.objects.get(title=branch)
    except Department.DoesNotExist:
        return Response({'Error': 'Invalid provided data of branch'}, status=status.HTTP_400_BAD_REQUEST)
       
    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
    payment = client.order.create({"amount": int(amount), 
                                   "currency": "INR", 
                                   "payment_capture": "1"})

    order = PurchasedCourse.objects.create(
                                 user=user,
                                 university=university_qry,
                                 branch=branch_qry,
                                 semester=semester, 
                                 order_amount=amount, 
                                 order_payment_id=payment['id'])

    serializer = PurchasedCourseSerializer(order)

    """order response will be 
    {'id': 17, 
    'order_date': '23 January 2021 03:28 PM', 
    'order_product': '**product name from frontend**', 
    'order_amount': '**product amount from frontend**', 
    'order_payment_id': 'order_G3NhfSWWh5UfjQ', # it will be unique everytime
    'isPaid': False}"""

    data = {
        "payment": payment,
        "order": serializer.data
    }
    return Response(data)

@api_view(['POST'])
def handle_payment_success(request):
    res = json.loads(request.data["response"])
    #res = request.POST
    """res will be:
    {'razorpay_payment_id': 'pay_G3NivgSZLx7I9e', 
    'razorpay_order_id': 'order_G3NhfSWWh5UfjQ', 
    'razorpay_signature': '76b2accbefde6cd2392b5fbf098ebcbd4cb4ef8b78d62aa5cce553b2014993c0'}
    """

    ord_id = ""
    raz_pay_id = ""
    raz_signature = ""

    # res.keys() will give us list of keys in res
    for key in res.keys():
        if key == 'razorpay_order_id':
            ord_id = res[key]
        elif key == 'razorpay_payment_id':
            raz_pay_id = res[key]
        elif key == 'razorpay_signature':
            raz_signature = res[key]

    # get order by payment_id which we've created earlier with isPaid=False
    order = PurchasedCourse.objects.get(order_payment_id=ord_id)

    data = {
        'razorpay_order_id': ord_id,
        'razorpay_payment_id': raz_pay_id,
        'razorpay_signature': raz_signature
    }

    client = razorpay.Client(auth=(env('PUBLIC_KEY'), env('SECRET_KEY')))
    # client = razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
    # checking if the transaction is valid or not if it is "valid" then check will return None
    check = client.utility.verify_payment_signature(data)

    if check is not None:
        print("Redirect to error url or error page")
        return Response({'error': 'Something went wrong'})

    # if payment is successful that means check is None then we will turn isPaid=True
    order.isPaid = True
    order.save()

    res_data = {
        'message': 'payment successfully received!'
    }

    return Response(res_data)

"""
=============================================== Comments ==============================================================
"""    

@api_view(['GET'])
def comments(request, course_id):
    if request.method == 'GET':
        try:    
            comment = Comment.objects.filter(course__id=course_id)
            comment_serializer = CommentSerializer(comment, many=True)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST']) 
def add_comment(request):   
    if request.method == 'POST':
        try:
            comment_data = request.data
            comment_serializer = CommentSerializer(data=comment_data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
            return Response(comment_serializer.error, status=status.HTTP_403_FORBIDDEN)  
        except:
            return Response({'Error': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])   
def edit_comment(request, comment_id):
   
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'Error': 'Comment does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'GET':
            comment_serializer = CommentSerializer(comment)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PUT':
            
            comment_data = request.data
            comment_serializer = CommentSerializer(comment, data=comment_data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
            return Response({'Error': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])  
def delete_comment(request, comment_id):  
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(id=comment_id)
            comment.delete()
            return Response({"Success": "Comment deleted"}, status=status.HTTP_410_GONE)
        except:
            return Response({'Error': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)
       

"""
=============================================== Course detail view ==============================================================
"""
@api_view(['GET']) 
def course_detail_view(request, id): 
    if request.method == 'GET':
        try:
            course = Course.objects.get(id=id)
            course_serializer = CourseSerializer(course)
            return Response(course_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "somthing went wrong"}, status=status.HTTP_403_FORBIDDEN) 


"""
=============================================== Star rating ==============================================================
"""
@api_view(['POST'])
def star_rating(request):
    if request.method == 'POST':
        token = request.data['token']
        course_id = request.data['course_id']
        star_rating = request.data['star_rating']

        try:
            token = Token.objects.get(key=token)
        except Token.DoesNotExist:
            return Response({"Error": "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=token.user_id)
        except User.DoesNotExist:
            return Response({"Error": "User does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"Error": "Course does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

        str_rtng = StarRating()
        str_rtng.user = user
        str_rtng.course = course
        str_rtng.star_rating = star_rating
        str_rtng.save()

        # Adding star rating into course
        try:
            str_rtng = StarRating.objects.all()
            max_total = str_rtng.count() * 5
            recieved_total = 0

            for star in str_rtng:
                recieved_total += star.star_rating
            
            one_percentage = max_total / 100
            recieved_percentage = recieved_total // one_percentage
            percentage = 5 / 100 * recieved_percentage

            course.star_rating = round(percentage)
            course.save()
        except ZeroDivisionError:
            return Response({"Success/Error":"Successfully saved star rating, But got an error - ZeroDivisionError"}, status= status.HTTP_200_OK)

        return Response({"Success":"Successfully saved"}, status= status.HTTP_200_OK)
