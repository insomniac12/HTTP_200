from django.test import TestCase
from .models import StudentDetail,FacultyDetail
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django.test import Client
from .forms import UserForm,StudentForm,FacultyForm

#models test

class StudentTest(TestCase):
    
    def setUp(self):
        self.user=User.objects.create(username='Shivangi',password='1234')
        StudentDetail.objects.create(year=3,branch='IT',univ_roll_no=1309113001,contact_no=9813728934 ,father_name='',mother_name='',address='',course='B.Tech',display_to_others='',user=self.user)
    
        
    def test_create_student(self):
        user=User.objects.get(username='Shivangi')
        student_details=StudentDetail.objects.get(user=user)
        self.assertEqual(student_details.year,3)
        
class FacultyTest(TestCase):
    
    def setUp(self):
        self.user=User.objects.create(username='Ajay',password='5678')
        FacultyDetail.objects.create(designation="teacher",department="IT",contact_no=9988213123,address="Indirapuram",alternate_email='abc@gmail.com',display_to_others='',user=self.user)
        
    def test_create_faculty(self):
        user=User.objects.get(username='Ajay')
        faculty_details=FacultyDetail.objects.get(user=user)
        self.assertEqual(faculty_details.department,'IT')
    
    
        
#forms test
class form_test(TestCase):
    def test_user_form(self):
        form_data={'username':'Shivangi','first_name':'Shivangi','last_name':'','email':'shivi.bajpai1@gmail.com'}
        form=UserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_student_form(self):
        form_data={'year':3,'branch':"IT",'univ_roll_no':1309113001,'contact_no':9813728934,'father_name':'','mother_name':'','address':'','course':"BT",'display_to_others':''}
        form=StudentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_faculty_form(self):
        form_data={'designation':"teacher",'department':"IT",'contact_no':9988213123,'address':"Indirapuram",'alternate_email':'abc@gmail.com','display_to_others':''}
        form=FacultyForm(data=form_data)
        self.assertTrue(form.is_valid())
   
   
 #views test       
class HomeTest(TestCase):
    
    def setUp(self):
        #self.user=User.objects.create(username='Shivangi',password='1234')
        #StudentDetail.objects.create(year=3,branch='IT',univ_roll_no=1309113001,contact_no=9813728934 ,father_name='',mother_name='',address='',course='B.Tech',display_to_others='',user=self.user)
        self.c=Client()
        
    def test_Home(self):
        url=reverse('home')
        response=self.c.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')
        
class UserProfileTest(TestCase):
    
    def setUp(self):
        self.user=User.objects.create(username='Shivangi')
        self.student_detail=StudentDetail.objects.create(year=3,branch='IT',univ_roll_no=1309113001,contact_no=9813728934 ,father_name='',mother_name='',address='',course='B.Tech',display_to_others='',user=self.user)
        self.faculty_detail=FacultyDetail.objects.create(designation="teacher",department="IT",contact_no=9988213123,address="Indirapuram",alternate_email='abc@gmail.com',display_to_others='',user=self.user)
        self.c=Client()
        
#tests if user is not logged in
    
    def test_user_profile_empty(self):
        #self.c.login(username='Shivangi',password='1234')
        url=reverse('user-profile',kwargs={'user_id':'Shivangi'})
        response=self.c.get(url)
        self.assertEqual(response.status_code,302)
        
#tests if student is logged in   
    
    def test_user_studentprofile(self):
        user = User.objects.get(username='Shivangi')
        user.set_password('1234')
        user.save()
        student_group=Group.objects.get(name='StudentGroup')
        student_group.user_set.add(user)
        self.c.login(username='Shivangi', password='1234')
        url=reverse('user-profile',kwargs={'user_id':'Shivangi'})
        response=self.c.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'user_profile.html')
        self.assertEqual(response.context['user_type'],'student')
        self.assertEqual(response.context['user_list'],user)
        self.assertEqual(response.context['detail_list'],self.student_detail)

#tests if faculty is logged in

    def test_user_facultyprofile(self):
        user = User.objects.get(username='Shivangi')
        user.set_password('1234')
        user.save()
        faculty_group=Group.objects.get(name='FacultyGroup')
        faculty_group.user_set.add(user)
        self.c.login(username='Shivangi', password='1234')
        url=reverse('user-profile',kwargs={'user_id':'Shivangi'})
        response=self.c.get(url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'user_profile.html')
        self.assertEqual(response.context['user_type'],'faculty')
        self.assertEqual(response.context['user_list'],user)
        self.assertEqual(response.context['detail_list'],self.faculty_detail)
