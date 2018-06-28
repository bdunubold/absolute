"""Views for a01 app."""

import datetime

from django.http import Http404
from django.http import HttpResponseRedirect
from django.db import IntegrityError, transaction
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from django.views.generic import TemplateView

from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import PermissionRequiredMixin

from a01.models import Student
from a01.models import CourseType
from a01.models import Course
from a01.models import Contract
from a01.models import Class
from a01.models import Teacher
from a01.models import CourseTeachers
from a01.models import TeacherSalary
from a01.models import Transaction
from a01.models import StudentLevel
from a01.models import Worker

from a01.choices import CONTRACT_INCOME
from a01.choices import CLASS_CHANGE_INCOME
from a01.choices import SALARY_EXPENSE
from a01.choices import NON_FREE
from a01.choices import FREE

from a01.forms import CourseTypeForm
from a01.forms import CourseForm
from a01.forms import ContractForm
from a01.forms import ContractPaymentForm
from a01.forms import ContractClassChangeForm
from a01.forms import TeacherForm
from a01.forms import TeacherCourseFormSet
from a01.forms import TeacherSalaryFormSet
from a01.forms import TeacherSalaryDateForm
from a01.forms import TransactionForm
from a01.forms import ContractfromStudentForm
from a01.forms import StudentLevelForm
from a01.forms import StudentForm
from a01.forms import StudentNoLevelForm
from a01.forms import WorkerForm
from a01.forms import WorkerSalaryFormSet

from a01.forms import CourseFilter
from a01.forms import ContractFilter
from a01.forms import StudentFilter
from a01.forms import SalaryFilter
from a01.forms import TransactionFilter
from a01.forms import StudentLevelFilter


class CustomDeleteView(DeleteView):
    """Using this class in order to not fully delete."""

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(CustomDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        if obj.flag is False:
            raise Http404

        return context

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.flag = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class FilterMixin(object):
    """Overrided method to filter."""

    def get_queryset_filters(self):
        """Filter querysets."""
        filters = {}
        for item in self.allowed_filters:
            if item in self.request.GET:
                if self.request.GET.get('flag') and self.request.GET.get('flag') == 'on':
                        filters[self.allowed_filters['flag']] = True
                else:
                    filters[self.allowed_filters[item]] = self.request.GET[item]
        return filters

    def get_queryset(self):
        """Get queryset."""
        data = super(FilterMixin, self).get_queryset().filter(**self.get_queryset_filters())

        paginator = Paginator(data, 20)

        page = self.request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        return data


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentDetailView(PermissionRequiredMixin, TemplateView):
    """Detailed information of Student."""

    permission_required = 'a01.s_composer'
    template_name = 'a01/student_detail.html'

    def get_context_data(self, **kwargs):
        """Function for context."""
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        stud = get_object_or_404(Student, pk=kwargs.get('id'))
        context['obj'] = stud
        context['classes'] = stud.sclasses.all()
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentView(PermissionRequiredMixin, TemplateView):
    """Display Student's data."""

    template_name = 'a01/student_list.html'
    permission_required = 'a01.s_composer'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(StudentView, self).get_context_data(**kwargs)
        f = StudentFilter(self.request.GET, queryset=Student.objects.all())
        context['filter'] = f

        return context

################################################################################


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentAddView(PermissionRequiredMixin, FormView):
    """View to add data into StudentLevelModel."""

    template_name = 'a01/student_add.html'
    form_class = StudentForm
    success_url = '/a01/student/'
    permission_required = 'a01.s_composer'

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data
        fname = data.get('fname')
        lname = data.get('lname')
        register = data.get('register')
        phone = data.get('phone')
        birthday = data.get('birthday')

        st = Student()
        st.fname = fname
        st.lname = lname
        st.register = register
        st.phone = phone
        st.birthday = birthday
        st.save()

        return super(StudentAddView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentEditView(PermissionRequiredMixin, UpdateView):
    """View to add data int levels StudentLevelModel."""

    model = Student
    template_name = 'a01/student_add.html'
    form_class = StudentForm
    success_url = '/a01/student/'
    permission_required = 'a01.s_composer'

    def get_object(self, queryset=None):
        """Handling GET objects."""
        obj = get_object_or_404(Student, pk=self.kwargs.get('id'))
        return obj


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model StudentLevel."""

    template_name = 'a01/student_delete.html'
    model = Student
    success_url = '/a01/student/'
    permission_required = 'a01.s_composer'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(StudentDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseTypeListView(PermissionRequiredMixin, FilterMixin, ListView):
    """View list of course types."""

    template_name = 'a01/course_type_list.html'
    model = CourseType
    context_object_name = 'ct_list'
    permission_required = 'a01.main'

    allowed_filters = {
        'level': 'level__icontains',
        'flag': 'flag__exact',
    }

    def get_queryset(self):
        """Queryset."""
        return CourseType.objects.filter(flag=True)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseTypeAddView(PermissionRequiredMixin, FormView):
    """View to add data into CourseTypeModel."""

    template_name = 'a01/course_type_add.html'
    form_class = CourseTypeForm
    success_url = '/a01/course_type/'
    permission_required = 'a01.main'

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data
        price = data.get('price', 0)
        level = data.get('level')
        info = data.get('info')
        length = data.get('length')
        hourly_price = data.get('hourly_price')

        ct = CourseType()
        ct.price = price
        ct.level = level
        ct.info = info
        ct.length = length
        ct.hourly_price = hourly_price

        ct.save()

        return super(CourseTypeAddView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseTypeEditView(PermissionRequiredMixin, UpdateView):
    """View to add data into CourseTypeModel."""

    model = CourseType
    template_name = 'a01/course_type_add.html'
    form_class = CourseTypeForm
    success_url = '/a01/course_type/'
    permission_required = 'a01.main'

    def get_object(self, queryset=None):
        """Handling GET objects."""
        obj = get_object_or_404(CourseType, pk=self.kwargs.get('id'))
        return obj


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseTypeDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model CourseType."""

    template_name = 'a01/delete_ctype.html'
    model = CourseType
    success_url = '/a01/course_type/'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(CourseTypeDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj.level
        return context

################################################################################


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseListView(PermissionRequiredMixin, TemplateView):
    """View list of courses."""

    template_name = 'a01/course_list.html'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(CourseListView, self).get_context_data(**kwargs)
        f = CourseFilter(self.request.GET, queryset=Course.objects.all())
        context['filter'] = f

        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseAddView(PermissionRequiredMixin, FormView):
    """View to add data into Course Model."""

    template_name = 'a01/course_add.html'
    form_class = CourseForm
    success_url = '/a01/course/'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(CourseAddView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['teacher_form'] = TeacherCourseFormSet(self.request.POST)
        else:
            context['teacher_form'] = TeacherCourseFormSet()

        return context

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data

        context = self.get_context_data()
        teacher_form = context['teacher_form']

        ctype = data['ctype']
        start_date = data['start_date']
        info = data['info']

        ct = Course()
        ct.ctype = ctype
        ct.start_date = start_date
        ct.info = info
        ct.save()

        if teacher_form.is_valid():
            objects = []

            for form in teacher_form:
                teacher = form.cleaned_data.get('teacher')
                lesson = form.cleaned_data.get('lesson')
                if teacher:
                    objects.append(CourseTeachers(teacher=teacher, course=ct, lesson=lesson))

            try:
                with transaction.atomic():
                    CourseTeachers.objects.filter(teacher=teacher, course=ct).delete()
                    CourseTeachers.objects.bulk_create(objects)

            except IntegrityError:
                return redirect(reverse('course_add'))

        return super(CourseAddView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseEditView(PermissionRequiredMixin, UpdateView):
    """View to add data into CourseModel."""

    model = Course
    template_name = 'a01/course_add.html'
    form_class = CourseForm
    success_url = '/a01/course/'
    permission_required = 'a01.main'

    def get_object(self, queryset=None):
        """Handling GET objects."""
        obj = get_object_or_404(Course, pk=self.kwargs.get('id'))
        return obj

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(CourseEditView, self).get_context_data(**kwargs)
        obj = get_object_or_404(Course, pk=self.kwargs.get('id'))
        object_list = CourseTeachers.objects.filter(course=obj)
        initial_data = []

        for each in object_list:
            data = {
                'teacher': each.teacher,
                'lesson': each.lesson
            }
            initial_data.append(data)

        if self.request.POST:
            context['teacher_form'] = TeacherCourseFormSet(self.request.POST, initial=initial_data)
        else:
            context['teacher_form'] = TeacherCourseFormSet(initial=initial_data)

        return context

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        context = self.get_context_data()
        teacher_form = context['teacher_form']

        if teacher_form.is_valid():
            objects = []

            for form in teacher_form:
                teacher = form.cleaned_data.get('teacher')
                lesson = form.cleaned_data.get('lesson')
                if teacher:
                    objects.append(CourseTeachers(teacher=teacher, course=self.object, lesson=lesson))

            try:
                with transaction.atomic():
                    CourseTeachers.objects.filter(course=self.object).delete()
                    CourseTeachers.objects.bulk_create(objects)

            except IntegrityError:
                return redirect(reverse('course_add'))

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class CourseDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model Course."""

    template_name = 'a01/course_delete.html'
    model = Course
    success_url = '/a01/course/'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(CourseDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context


class CourseDetailView(PermissionRequiredMixin, TemplateView):
    """Detailed information of Contract."""

    template_name = 'a01/course_detail.html'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Function for context."""
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        con = get_object_or_404(Course, pk=kwargs.get('id'))

        contracts = Contract.objects.filter(course=con)

        classes = con.cclasses.all()
        teachers = con.cteachers.all()
        context['obj'] = con
        context['contracts'] = contracts
        context['teachers'] = teachers
        context['total_student'] = classes.count()
        return context

################################################################################


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class ContractListView(PermissionRequiredMixin, TemplateView):
    """View list of Contracts."""

    template_name = 'a01/contract_list.html'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(ContractListView, self).get_context_data(**kwargs)
        f = ContractFilter(self.request.GET, queryset=Contract.objects.all())
        context['filter'] = f

        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class ContractAddView(PermissionRequiredMixin, FormView):
    """Main view to add Contract."""

    template_name = 'a01/contract_add.html'
    form_class = ContractForm
    success_url = '/a01/contract/'
    permission_required = 'a01.main'

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data

        fname = data['fname']
        lname = data['lname']
        register = data['register']
        phone = data['phone']
        birthday = data['birthday']
        course = data['course']
        payment = data['payment']
        txn_method = data['txn_method']
        minus_length = data['minus_length']
        contract_number = data['contract_number']
        off_percent = data['off_percent']
        description = data['description']
        con_date = data['con_date']

        st = Student()
        st.fname = fname
        st.lname = lname
        st.register = register
        st.birthday = birthday
        st.phone = phone
        st.save()

        con = Contract()
        con.contract_number = contract_number
        con.date = con_date
        con.student = st
        con.course = course
        con.minus_length = minus_length
        con.total_payment = payment
        con.off_percent = off_percent
        con.description = description

        total_price = course.price
        hourly_price = course.hourly_price

        real_length = course.ctype.length - minus_length

        if 100 >= off_percent > 0:
            off_price = total_price * off_percent / 100
            total_price = total_price - off_price

            hourly_price = round(total_price / course.ctype.length)

        if minus_length == 0:
            con.req_payment = total_price
        else:
            con.req_payment = hourly_price * real_length
        con.save()

        txn = Transaction()
        txn.contract = con
        txn.txn_type = CONTRACT_INCOME
        txn.amount = payment
        txn.txn_date = con_date
        txn.txn_method = txn_method
        txn.save()

        cls = Class()
        cls.student = st
        cls.course = course
        cls.save()

        return super(ContractAddView, self).form_valid(form)


class ContractPaymentView(PermissionRequiredMixin, FormView):
    """Used for additional contract payment."""

    template_name = 'a01/contract_payment.html'
    form_class = ContractPaymentForm
    success_url = '/a01/contract/'
    permission_required = 'a01.main'

    def get_initial(self):
        """Giving initial date as Today."""
        return {"txn_date": datetime.datetime.now()}

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data
        payment = data.get('payment', 0)
        txn_date = data.get('txn_date')
        txn_method = data.get('txn_method')
        description = data.get('description')
        con_id = self.kwargs.get('id')

        con = get_object_or_404(Contract, pk=con_id)

        txn = Transaction()
        txn.contract = con
        txn.txn_type = CONTRACT_INCOME
        txn.amount = payment
        txn.txn_date = txn_date
        txn.txn_method = txn_method
        txn.description = description
        txn.save()

        con.total_payment = con.total_payment + payment
        con.save()

        return super(ContractPaymentView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class ContractDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model Contract."""

    template_name = 'a01/contract_delete.html'
    model = Contract
    success_url = '/a01/contract/'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(ContractDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        cls = Class.objects.filter(course=self.object.course, student=self.object.student).first()
        cls.delete()
        self.object.flag = False
        self.object.save()
        return HttpResponseRedirect(success_url)



class ContractDetailView(PermissionRequiredMixin, TemplateView):
    """Detailed information of Contract."""

    template_name = 'a01/contract_detail.html'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Function for context."""
        context = super(ContractDetailView, self).get_context_data(**kwargs)
        con = get_object_or_404(Contract, pk=kwargs.get('id'))
        context['obj'] = con
        context['payment'] = con.req_payment - con.total_payment
        context['id'] = kwargs.get('id')
        context['txns'] = con.ctxns.all()
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class ContractClassChangeView(PermissionRequiredMixin, FormView):
    """View to add data into CourseTypeModel."""

    template_name = 'a01/contract_class_change.html'
    success_url = '/a01/contract/'
    form_class = ContractClassChangeForm
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Function for context."""
        context = super(ContractClassChangeView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs.get('id')
        return context

    def get_form_kwargs(self):
        """Sending kwargs into form."""
        id = self.kwargs.get('id')
        kwargs = super().get_form_kwargs()
        kwargs.update(id=id)
        return kwargs

    def form_valid(self, form):
        """Called after valid data."""
        id = self.kwargs.get('id')

        data = form.cleaned_data
        course = data.get('course', 0)
        txn_method = data.get('txn_method')
        class_change = data.get('class_change')
        description = data.get('description')

        con = get_object_or_404(Contract, pk=id)
        initial_class = con.course

        class_obj = Class.objects.filter(course=con.course, student=con.student).first()
        class_obj.course = course
        class_obj.save()
        con.course = course
        con.save()
        from django.utils import timezone
        now = timezone.now()
        if class_change == FREE:
            return super(ContractClassChangeView, self).form_valid(form)
        if initial_class.start_date < now:
            txn = Transaction()
            txn.contract = con
            txn.txn_type = CLASS_CHANGE_INCOME
            txn.amount = 88000
            txn.txn_method = txn_method
            txn.description = description
            txn.txn_date = datetime.datetime.now()
            txn.save()

        return super(ContractClassChangeView, self).form_valid(form)


################################################################################

@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TeacherListView(PermissionRequiredMixin, FilterMixin, ListView):
    """List of all teachers."""

    template_name = 'a01/teacher_list.html'
    model = Teacher
    context_object_name = 'list'
    permission_required = 'a01.main'

    allowed_filters = {
        'fname': 'fname__icontains',
        'register': 'register__startswith',
        'phone': 'phone__icontains',
        'flag': 'flag__exact',
    }


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TeacherAddView(PermissionRequiredMixin, FormView):
    """To add Teachers."""

    template_name = 'a01/teacher_add.html'
    form_class = TeacherForm
    success_url = '/a01/teacher/'
    permission_required = 'a01.main'

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data

        fname = data.get('fname')
        lname = data.get('lname')
        register = data.get('register')
        phone = data.get('phone')
        birthday = data.get('birthday')
        hourly_wage = data.get('hourly_wage')

        tch = Teacher()
        tch.fname = fname
        tch.lname = lname
        tch.register = register
        tch.phone = phone
        tch.birthday = birthday
        tch.hourly_wage = hourly_wage
        tch.save()

        return super(TeacherAddView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TeacherEditView(PermissionRequiredMixin, UpdateView):
    """View to add data into TeacherModel."""

    model = Teacher
    template_name = 'a01/teacher_add.html'
    form_class = TeacherForm
    success_url = '/a01/teacher/'
    permission_required = 'a01.main'

    def get_object(self, queryset=None):
        """Handling GET objects."""
        obj = get_object_or_404(Teacher, pk=self.kwargs.get('id'))
        return obj


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TeacherDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model Teacher."""

    template_name = 'a01/delete_teacher.html'
    model = Teacher
    success_url = '/a01/teacher/'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(TeacherDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TeacherDetailView(PermissionRequiredMixin, TemplateView):
    """Detailed information of Teacher."""

    template_name = 'a01/teacher_detail.html'
    permission_required = 'a01.main'

    def get_context_data(self, **kwargs):
        """Function for context."""
        context = super(TeacherDetailView, self).get_context_data(**kwargs)
        tch = get_object_or_404(Teacher, pk=kwargs.get('id'))
        context['obj'] = tch
        context['courses'] = tch.tcourses.all()
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TeacherSalaryCalculatorView(PermissionRequiredMixin, FormView):
    """View to add data into CourseTypeModel."""

    template_name = 'a01/salary_calculator.html'
    form_class = TeacherSalaryDateForm
    success_url = '/a01/teacher/salary/detail'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(TeacherSalaryCalculatorView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['salary_form'] = TeacherSalaryFormSet(self.request.POST)
        else:
            context['salary_form'] = TeacherSalaryFormSet()

        print('')

        return context

    def form_valid(self, form):
        """Called after valid data."""
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        mshift = form.cleaned_data['mshift']
        context = self.get_context_data()
        salary_form = context['salary_form']

        t_objs = TeacherSalary.objects.filter(month=month, year=year, mshift=mshift).exclude(teacher=None)

        teachers = []

        now = datetime.datetime.now()

        for each in t_objs:
            teachers.append(each.teacher)

        if salary_form.is_valid():
            objects = []
            txn_objs = []
            for each in salary_form:
                teacher = each.cleaned_data.get('teacher')
                if teacher in teachers:
                    continue
                hour = each.cleaned_data.get('hour')
                salary = teacher.hourly_wage * hour
                if teacher and hour:
                    objects.append(TeacherSalary(teacher=teacher, year=year, worked_hour=hour, month=month, mshift=mshift, salary=salary))
                    txn_objs.append(Transaction(amount=salary, txn_type=SALARY_EXPENSE, txn_date=now))

            try:
                with transaction.atomic():
                    TeacherSalary.objects.bulk_create(objects)
                    Transaction.objects.bulk_create(txn_objs)

            except IntegrityError:
                return redirect(reverse('teacher'))

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TeacherSalaryDetailView(PermissionRequiredMixin, TemplateView):
    """View list of Salaries."""

    template_name = 'a01/teacher_salary_detail.html'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(TeacherSalaryDetailView, self).get_context_data(**kwargs)
        f = SalaryFilter(self.request.GET, queryset=TeacherSalary.objects.all())
        context['filter'] = f

        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TransactionListView(PermissionRequiredMixin, TemplateView):
    """View list of Transactions."""

    template_name = 'a01/transaction_list.html'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(TransactionListView, self).get_context_data(**kwargs)
        f = TransactionFilter(self.request.GET, queryset=Transaction.objects.all())

        income = 0
        expense = 0

        for each in f.qs:
            if each.txn_type.endswith('INCOME'):
                income += each.amount
            elif each.txn_type.endswith('EXPENSE'):
                expense += each.amount

        context['income'] = income
        context['expense'] = expense

        context['filter'] = f
        context['type_list'] = ['INCOME', 'EXPENSE']
        context['expense_list'] = ['SEXPENSE', 'EXPENSE']

        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TransactionAddView(PermissionRequiredMixin, FormView):
    """View to add data into TransactionModel."""

    template_name = 'a01/transaction_add.html'
    form_class = TransactionForm
    success_url = '/a01/transaction/'
    permission_required = 'a01.accounting'

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data
        amount = data.get('amount', 0)
        txn_type = data.get('txn_type')
        txn_date = data.get('txn_date')
        txn_method = data.get('txn_method')
        info = data.get('info')

        txn = Transaction()
        txn.amount = amount
        txn.txn_type = txn_type
        txn.txn_date = txn_date
        txn.txn_method = txn_method
        txn.info = info

        txn.save()

        return super(TransactionAddView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TransactionEditView(PermissionRequiredMixin, UpdateView):
    """View to add data into CourseTypeModel."""

    model = Transaction
    template_name = 'a01/transaction_add.html'
    form_class = TransactionForm
    success_url = '/a01/transaction/'
    permission_required = 'a01.accounting'

    def get_object(self, queryset=None):
        """Handling GET objects."""
        obj = get_object_or_404(Transaction, pk=self.kwargs.get('id'))
        return obj


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TransactionDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model CourseType."""

    template_name = 'a01/transaction_delete.html'
    model = Transaction
    success_url = '/a01/transaction/'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(TransactionDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class TransactionVerifyView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model CourseType."""

    template_name = 'a01/transaction_verify.html'
    model = Transaction
    success_url = '/a01/transaction/'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(TransactionVerifyView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context

    def delete(self, request, *args, **kwargs):
        """Overwritten delete function."""
        self.object = self.get_object()
        success_url = self.get_success_url()

        self.object.verified = True
        self.object.save()

        return HttpResponseRedirect(success_url)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class ContractFromStudentView(PermissionRequiredMixin, FormView):
    """View to add data into TransactionModel."""

    template_name = 'a01/contract_student_add.html'
    form_class = ContractfromStudentForm
    success_url = '/a01/student/'
    permission_required = 'a01.s_composer'

    def get_form_kwargs(self):
        """Sending kwargs into form."""
        id = self.kwargs.get('id')
        kwargs = super().get_form_kwargs()
        kwargs.update(id=id)
        return kwargs

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data
        payment = data.get('payment', 0)
        course = data.get('course')
        minus_length = data.get('minus_length')
        txn_method = data.get('txn_method')
        contract_number = data.get('contract_number')
        off_percent = data['off_percent']
        description = data['description']
        con_date = data['con_date']

        obj = get_object_or_404(Student, pk=self.kwargs.get('id'))

        con = Contract()
        con.course = course
        con.date = con_date
        con.total_payment = payment
        con.minus_length = minus_length
        con.contract_number = contract_number
        con.off_percent = off_percent
        con.description = description
        con.student = obj

        total_price = course.price
        hourly_price = course.hourly_price

        if 100 >= off_percent > 0:
            off_price = total_price * off_percent / 100
            total_price = total_price - off_price

            hourly_price = round(total_price / course.ctype.length)

        real_length = course.ctype.length - minus_length
        if minus_length == 0:
            con.req_payment = total_price
        else:
            con.req_payment = hourly_price * real_length

        con.save()

        txn = Transaction()
        txn.contract = con
        txn.txn_type = CONTRACT_INCOME
        txn.amount = payment
        txn.txn_date = con_date
        txn.txn_method = txn_method
        txn.save()

        cls = Class()
        cls.student = obj
        cls.course = course
        cls.save()

        return super(ContractFromStudentView, self).form_valid(form)

################################################################################


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class WorkerListView(PermissionRequiredMixin, FilterMixin, ListView):
    """List of all workers."""

    template_name = 'a01/worker_list.html'
    model = Worker
    context_object_name = 'list'
    permission_required = 'a01.accounting'

    allowed_filters = {
        'fname': 'fname__icontains',
        'register': 'register__startswith',
        'phone': 'phone__icontains',
        'flag': 'flag__exact',
    }

    def get_queryset(self):
        """Queryset."""
        return Worker.objects.filter(flag=True)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class WorkerAddView(PermissionRequiredMixin, FormView):
    """To add worker."""

    template_name = 'a01/worker_add.html'
    form_class = WorkerForm
    success_url = '/a01/worker/'
    permission_required = 'a01.accounting'

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data

        fname = data.get('fname')
        lname = data.get('lname')
        register = data.get('register')
        phone = data.get('phone')
        birthday = data.get('birthday')
        monthly_wage = data.get('monthly_wage')

        tch = Worker()
        tch.fname = fname
        tch.lname = lname
        tch.register = register
        tch.phone = phone
        tch.birthday = birthday
        tch.monthly_wage = monthly_wage
        tch.save()

        return super(WorkerAddView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class WorkerEditView(PermissionRequiredMixin, UpdateView):
    """View to add data into WorkerModel."""

    model = Worker
    template_name = 'a01/worker_add.html'
    form_class = WorkerForm
    success_url = '/a01/worker/'
    permission_required = 'a01.accounting'

    def get_object(self, queryset=None):
        """Handling GET objects."""
        obj = get_object_or_404(Worker, pk=self.kwargs.get('id'))
        return obj


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class WorkerDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model Worker."""

    template_name = 'a01/delete_worker.html'
    model = Worker
    success_url = '/a01/worker/'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(WorkerDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class WorkerDetailView(PermissionRequiredMixin, TemplateView):
    """Detailed information of Teacher."""

    template_name = 'a01/worker_detail.html'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Function for context."""
        context = super(WorkerDetailView, self).get_context_data(**kwargs)
        tch = get_object_or_404(Worker, pk=kwargs.get('id'))
        context['obj'] = tch
        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class WorkerSalaryCalculatorView(PermissionRequiredMixin, FormView):
    """View to add data into CourseTypeModel."""

    template_name = 'a01/worker_salary_calculator.html'
    form_class = TeacherSalaryDateForm
    success_url = '/a01/worker/salary/detail'
    permission_required = 'a01.accounting'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(WorkerSalaryCalculatorView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['salary_form'] = WorkerSalaryFormSet(self.request.POST)
        else:
            context['salary_form'] = WorkerSalaryFormSet()

        print('')

        return context

    def form_valid(self, form):
        """Called after valid data."""
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
        mshift = form.cleaned_data['mshift']
        context = self.get_context_data()
        salary_form = context['salary_form']

        t_objs = TeacherSalary.objects.filter(month=month, year=year, mshift=mshift).exclude(worker=None)

        workers = []

        now = datetime.datetime.now()

        for each in t_objs:
            workers.append(each.worker)

        if salary_form.is_valid():
            objects = []
            txn_objs = []
            for each in salary_form:
                worker = each.cleaned_data.get('worker')
                if worker in workers:
                    continue
                wage = each.cleaned_data.get('wage')
                if worker and wage:
                    objects.append(TeacherSalary(worker=worker, year=year, month=month, mshift=mshift, salary=wage))
                    txn_objs.append(Transaction(amount=wage, txn_type=SALARY_EXPENSE, txn_date=now))

            try:
                with transaction.atomic():
                    TeacherSalary.objects.bulk_create(objects)
                    Transaction.objects.bulk_create(txn_objs)

            except IntegrityError:
                return redirect(reverse('worker'))

        return HttpResponseRedirect(self.get_success_url())


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentLevelListView(PermissionRequiredMixin, TemplateView):
    """View list of Student levels."""

    template_name = 'a01/student_level_list.html'
    permission_required = 'a01.s_composer'

    def get_context_data(self, **kwargs):
        """Context data."""
        context = super(StudentLevelListView, self).get_context_data(**kwargs)
        f = StudentLevelFilter(self.request.GET, queryset=StudentLevel.objects.all())
        context['filter'] = f

        return context


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentLevelAddView(PermissionRequiredMixin, FormView):
    """View to add data into StudentLevelModel."""

    template_name = 'a01/student_level_add.html'
    form_class = StudentNoLevelForm
    success_url = '/a01/student/'
    permission_required = 'a01.s_composer'

    def form_valid(self, form):
        """Called after valid data."""
        data = form.cleaned_data

        student = get_object_or_404(Student, pk=self.kwargs.get('id'))

        level = data.get('level')
        date = data.get('date')
        course = data.get('course')

        stl = StudentLevel()
        stl.student = student
        stl.level = level
        stl.date = date
        stl.course = course
        stl.save()

        if course:
            cls = Class()
            cls.student = student
            cls.course = course
            cls.save()

        return super(StudentLevelAddView, self).form_valid(form)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentLevelEditView(PermissionRequiredMixin, UpdateView):
    """View to add data int levels StudentLevelModel."""

    model = StudentLevel
    template_name = 'a01/student_level_add.html'
    form_class = StudentLevelForm
    success_url = '/a01/student_level/'
    permission_required = 'a01.s_composer'

    def get_object(self, queryset=None):
        """Handling GET objects."""
        obj = get_object_or_404(Student, pk=self.kwargs.get('id'))
        return obj


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class StudentLevelDeleteView(PermissionRequiredMixin, CustomDeleteView):
    """Deleting data row from Model StudentLevel."""

    template_name = 'a01/student_level_delete.html'
    model = StudentLevel
    success_url = '/a01/student_level/'
    permission_required = 'a01.s_composer'

    def get_context_data(self, **kwargs):
        """Context control."""
        context = super(StudentLevelDeleteView, self).get_context_data(**kwargs)
        obj = context.get('object')
        context['object'] = obj
        return context

    def delete(self, request, *args, **kwargs):
        """Overwritten delete function."""
        self.object = self.get_object()
        success_url = self.get_success_url()

        Class.objects.filter(student=self.object.student, course=self.object.course).delete()

        return HttpResponseRedirect(success_url)


@method_decorator(login_required(redirect_field_name='home'), name='dispatch')
class WorkerSalaryDetailView(TeacherSalaryDetailView):
    """View list of Salaries."""

    template_name = 'a01/worker_salary_detail.html'
