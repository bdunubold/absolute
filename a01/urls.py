"""Urls for app a01."""
from django.conf.urls import url

from .views import StudentView
from .views import StudentDetailView
from .views import StudentAddView
from .views import StudentEditView
from .views import StudentDeleteView

from .views import CourseTypeListView
from .views import CourseTypeAddView
from .views import CourseTypeEditView
from .views import CourseTypeDeleteView

from .views import CourseListView
from .views import CourseAddView
from .views import CourseEditView
from .views import CourseDeleteView
from .views import CourseDetailView

from .views import ContractListView
from .views import ContractAddView
from .views import ContractPaymentView
from .views import ContractDeleteView
from .views import ContractDetailView
from .views import ContractClassChangeView
from .views import ContractFromStudentView

from .views import TeacherListView
from .views import TeacherAddView
from .views import TeacherEditView
from .views import TeacherDeleteView
from .views import TeacherDetailView
from .views import TeacherSalaryCalculatorView
from .views import TeacherSalaryDetailView

from .views import TransactionListView
from .views import TransactionAddView
from .views import TransactionEditView
from .views import TransactionDeleteView

from .views import StudentLevelListView
from .views import StudentLevelAddView
from .views import StudentLevelEditView
from .views import StudentLevelDeleteView
from .views import TransactionVerifyView


from .views import WorkerListView
from .views import WorkerAddView
from .views import WorkerEditView
from .views import WorkerDeleteView
from .views import WorkerDetailView
from .views import WorkerSalaryCalculatorView
from .views import WorkerSalaryDetailView


urlpatterns = [
    url(r'^student/$', StudentView.as_view(), name='student'),
    url(r'^student/(?P<id>[0-9]+)/$', StudentDetailView.as_view(), name='detail'),
    url(r'^student/add/$', StudentAddView.as_view(), name='student_add'),
    url(r'^student/edit/(?P<id>[0-9]+)/$', StudentEditView.as_view(), name='student_edit'),
    url(r'^student/delete/(?P<pk>[0-9]+)/$', StudentDeleteView.as_view(), name='student_delete'),
    url(r'^student/contract/(?P<id>[0-9]+)/$', ContractFromStudentView.as_view(), name='student_contract'),

    url(r'^course_type/$', CourseTypeListView.as_view(), name='course_type'),
    url(r'^course_type/add/$', CourseTypeAddView.as_view(), name='course_type_add'),
    url(r'^course_type/edit/(?P<id>[0-9]+)/$', CourseTypeEditView.as_view(), name='course_type_edit'),
    url(r'^course_type/delete/(?P<pk>[0-9]+)/$', CourseTypeDeleteView.as_view(), name='course_type_delete'),

    url(r'^course/$', CourseListView.as_view(), name='course'),
    url(r'^course/add/$', CourseAddView.as_view(), name='course_add'),
    url(r'^course/edit/(?P<id>[0-9]+)/$', CourseEditView.as_view(), name='course_edit'),
    url(r'^course/delete/(?P<pk>[0-9]+)/$', CourseDeleteView.as_view(), name='course_delete'),
    url(r'^course/(?P<id>[0-9]+)/$', CourseDetailView.as_view(), name='course_detail'),

    url(r'^contract/$', ContractListView.as_view(), name='contract'),
    url(r'^contract/add/$', ContractAddView.as_view(), name='contract_add'),
    url(r'^contract/payment/(?P<id>[0-9]+)/$', ContractPaymentView.as_view(), name='contract_payment'),
    url(r'^contract/delete/(?P<pk>[0-9]+)/$', ContractDeleteView.as_view(), name='contract_delete'),
    url(r'^contract/(?P<id>[0-9]+)/$', ContractDetailView.as_view(), name='contract_detail'),
    url(r'^contract/change/(?P<id>[0-9]+)/$', ContractClassChangeView.as_view(), name='contract_change'),

    url(r'^teacher/$', TeacherListView.as_view(), name='teacher'),
    url(r'^teacher/(?P<id>[0-9]+)/$', TeacherDetailView.as_view(), name='teacher_detail'),
    url(r'^teacher/add/$', TeacherAddView.as_view(), name='teacher_add'),
    url(r'^teacher/edit/(?P<id>[0-9]+)/$', TeacherEditView.as_view(), name='teacher_edit'),
    url(r'^teacher/delete/(?P<pk>[0-9]+)/$', TeacherDeleteView.as_view(), name='teacher_delete'),

    url(r'^teacher/salary/$', TeacherSalaryCalculatorView.as_view(), name='teacher_salary'),
    url(r'^teacher/salary/detail/$', TeacherSalaryDetailView.as_view(), name='teacher_salary_detail'),

    url(r'^transaction/$', TransactionListView.as_view(), name='transaction'),
    url(r'^transaction/add/$', TransactionAddView.as_view(), name='transaction_add'),
    url(r'^transaction/edit/(?P<id>[0-9]+)/$', TransactionEditView.as_view(), name='transaction_edit'),
    url(r'^transaction/delete/(?P<pk>[0-9]+)/$', TransactionDeleteView.as_view(), name='transaction_delete'),
    url(r'^transaction/verify/(?P<pk>[0-9]+)/$', TransactionVerifyView.as_view(), name='transaction_verify'),


    url(r'^student_level/$', StudentLevelListView.as_view(), name='student_level'),
    url(r'^student_level/add/(?P<id>[0-9]+)/$', StudentLevelAddView.as_view(), name='student_level_add'),
    url(r'^student_level/edit/(?P<id>[0-9]+)/$', StudentLevelEditView.as_view(), name='student_level_edit'),
    url(r'^student_level/delete/(?P<pk>[0-9]+)/$', StudentLevelDeleteView.as_view(), name='student_level_delete'),


    url(r'^worker/$', WorkerListView.as_view(), name='worker'),
    url(r'^worker/(?P<id>[0-9]+)/$', WorkerDetailView.as_view(), name='worker_detail'),
    url(r'^worker/add/$', WorkerAddView.as_view(), name='worker_add'),
    url(r'^worker/edit/(?P<id>[0-9]+)/$', WorkerEditView.as_view(), name='worker_edit'),
    url(r'^worker/delete/(?P<pk>[0-9]+)/$', WorkerDeleteView.as_view(), name='worker_delete'),
    url(r'^worker/calculator/$', WorkerSalaryCalculatorView.as_view(), name='worker_calculator'),
    url(r'^worker/salary/detail/$', WorkerSalaryDetailView.as_view(), name='worker_salary_detail'),

]
