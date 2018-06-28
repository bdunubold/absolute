"""All adding and editing forms for app a01."""

import datetime
from django import forms
from a01.models import CourseType
from a01.models import Class
from a01.models import Course
from a01.models import Teacher
from a01.models import Contract
from a01.models import Student
from a01.models import TeacherSalary
from a01.models import Transaction
from a01.models import StudentLevel
from a01.models import Worker
from django.forms import formset_factory
from django.forms.formsets import BaseFormSet
import django_filters

from a01.choices import MONTHS
from a01.choices import FORM_CHOICES
from a01.choices import LEVEL_CHOICES
from a01.choices import TXN_METHODS
from a01.choices import SHIFTS
from a01.choices import CLASS_CHANGE_CHOICES
from a01.choices import NON_FREE


class CustomBaseFormSet(BaseFormSet):
    """Using validation."""

    def clean(self):
        """
        Add validation to check that no two links have the same anchor or URL.
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        teachers = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                teacher = form.cleaned_data['teacher']

                if teacher in teachers:
                    duplicates = True
                teachers.append(teacher)

                if duplicates:
                    raise forms.ValidationError(
                        'Нэг багшийг 1 л сонгох боломжтой.',
                        code='duplicate_teachers'
                    )


class WorkerCustomBaseFormSet(BaseFormSet):
    """Using validation."""

    def clean(self):
        """
        Add validation to check that no two links have the same anchor or URL.
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        workers = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                worker = form.cleaned_data['worker']

                if worker in workers:
                    duplicates = True
                workers.append(worker)

                if duplicates:
                    raise forms.ValidationError(
                        'Нэг ажилтаныг 1 л сонгох боломжтой.',
                        code='duplicate_workers'
                    )


class CourseForm(forms.ModelForm):
    """Form for Course."""

    class Meta:
        """Meta."""

        model = Course
        fields = ['ctype', 'start_date', 'info']

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(CourseForm, self).__init__(*args, **kwargs)
        self.fields['ctype'].widget.attrs['class'] = 'form-control'
        self.fields['ctype'].queryset = CourseType.objects.filter(flag=True)
        self.fields['start_date'].widget.attrs['class'] = 'form-control datetimepicker'
        self.fields['info'].widget.attrs['class'] = 'form-control'


class CourseTypeForm(forms.ModelForm):
    """Form for CourseType."""

    class Meta:
        """Meta."""

        model = CourseType
        fields = ['price', 'level', 'info', 'length', 'hourly_price']

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(CourseTypeForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['level'].widget.attrs['class'] = 'form-control'
        self.fields['info'].widget.attrs['class'] = 'form-control'
        self.fields['length'].widget.attrs['class'] = 'form-control'
        self.fields['hourly_price'].widget.attrs['class'] = 'form-control'
        self.fields['hourly_price'].widget.attrs['readonly'] = True


class TeacherCourseForm(forms.Form):
    """Form set."""

    teacher = forms.ModelChoiceField(label='Багш', queryset=Teacher.objects.filter(flag=True))
    lesson = forms.CharField(label="Сэдэв")

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(TeacherCourseForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].widget.attrs['class'] = 'form-control'
        self.fields['lesson'].widget.attrs['class'] = 'form-control'


TeacherCourseFormSet = formset_factory(TeacherCourseForm, formset=CustomBaseFormSet)


class ContractForm(forms.Form):
    """Form to register all information necessary for Contract."""

    fname = forms.CharField(label="Нэр")
    lname = forms.CharField(label="Эцэг/эх - ийн нэр")
    register = forms.CharField(label="Регистрийн дугаар", required=False)
    phone = forms.CharField(label="Утас")
    birthday = forms.DateTimeField(label="Төрсөн өдөр", required=False)
    con_date = forms.DateTimeField(label="Гэрээний огноо", initial=datetime.date.today().strftime('%m/%d/%Y'))
    course = forms.ModelChoiceField(label='Анги', queryset=Course.objects.filter(flag=True))
    payment = forms.IntegerField(label="Төлж буй төлбөр")
    minus_length = forms.IntegerField(label="Хасагдсан цаг", initial=0)
    off_percent = forms.IntegerField(label="Хямдрал", required=False, initial=0)
    description = forms.CharField(label="Тайлбар", required=False)
    txn_method = forms.ChoiceField(choices=TXN_METHODS, label="Төрөл")
    contract_number = forms.CharField(label="Гэрээний дугаар")

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(ContractForm, self).__init__(*args, **kwargs)

        for each in self.fields:
            self.fields[each].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control datetimepicker'
        self.fields['con_date'].widget.attrs['class'] = 'form-control datetimepicker'


class ContractPaymentForm(forms.Form):
    """Form used for additional payment."""

    payment = forms.IntegerField(label="Төлж буй төлбөр")
    txn_date = forms.DateTimeField(label="Гүйлгээний огноо")
    txn_method = forms.ChoiceField(choices=TXN_METHODS, label="Төрөл")
    description = forms.CharField(label="Тайлбар", required=False)

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(ContractPaymentForm, self).__init__(*args, **kwargs)
        self.fields['payment'].widget.attrs['class'] = 'form-control'
        self.fields['txn_method'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['txn_date'].widget.attrs['class'] = 'form-control datetimepicker'


class ContractClassChangeForm(forms.Form):
    """Form used for changing courses payment."""

    course = forms.ModelChoiceField(label='Анги', queryset=Course.objects.filter(flag=True))
    txn_method = forms.ChoiceField(choices=TXN_METHODS, label="Төрөл")
    class_change = forms.ChoiceField(choices=CLASS_CHANGE_CHOICES, label="Төлбөртэй эсэх", initial=NON_FREE)
    description = forms.CharField(label="Тайлбар", required=False)

    def clean(self):
        """Cleaning data."""
        cleaned_data = self.cleaned_data

        course = cleaned_data.get('course')

        con = Contract.objects.filter(id=self.obj_id).first()

        if (con.course == course):
            raise forms.ValidationError("ALERT !")
        else:
            return cleaned_data

    def __init__(self, id=None, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(ContractClassChangeForm, self).__init__(*args, **kwargs)
        self.fields['course'].widget.attrs['class'] = 'form-control'
        self.fields['class_change'].widget.attrs['class'] = 'form-control'
        self.fields['txn_method'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.obj_id = id


class TeacherForm(forms.ModelForm):
    """Form used to save Teacher."""

    class Meta:
        """Meta."""

        model = Teacher
        fields = [
            'fname',
            'lname',
            'register',
            'phone',
            'birthday',
            'hourly_wage',
        ]

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(TeacherForm, self).__init__(*args, **kwargs)

        for each in self.fields:
            self.fields[each].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control datetimepicker'


class TeacherSalaryDateForm(forms.Form):
    """Filter form."""

    year = forms.IntegerField(label="Он")
    month = forms.ChoiceField(label="Сар", choices=MONTHS)
    mshift = forms.ChoiceField(label="Ээлж", choices=SHIFTS)

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(TeacherSalaryDateForm, self).__init__(*args, **kwargs)
        self.fields['year'].widget.attrs['class'] = 'form-control'
        self.fields['month'].widget.attrs['class'] = 'form-control'
        self.fields['mshift'].widget.attrs['class'] = 'form-control'


class TeacherSalaryForm(forms.Form):
    """Form set."""

    teacher = forms.ModelChoiceField(label='Багш', queryset=Teacher.objects.filter(flag=True))
    hour = forms.IntegerField(label="Ажилсан цаг")

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(TeacherSalaryForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].widget.attrs['class'] = 'form-control'
        self.fields['hour'].widget.attrs['class'] = 'form-control'


TeacherSalaryFormSet = formset_factory(TeacherSalaryForm, formset=CustomBaseFormSet)


class WorkerSalaryForm(forms.Form):
    """Form set."""

    worker = forms.ModelChoiceField(label='Ажилтан', queryset=Worker.objects.filter(flag=True))
    wage = forms.IntegerField(label="Ажилсан цаг")

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(WorkerSalaryForm, self).__init__(*args, **kwargs)
        self.fields['worker'].widget.attrs['class'] = 'form-control'
        self.fields['wage'].widget.attrs['class'] = 'form-control'


WorkerSalaryFormSet = formset_factory(WorkerSalaryForm, formset=WorkerCustomBaseFormSet)


class CourseFilter(django_filters.FilterSet):
    """Filter for course."""

    ctype = django_filters.ModelChoiceFilter(queryset=CourseType.objects.filter(flag=True))
    flag = django_filters.BooleanFilter()

    class Meta:
        """Meta."""

        model = Course

        fields = {
            'start_date': ['lt', 'gt'],
            'ctype': ['exact'],
            'flag': ['exact'],
        }


class ContractFilter(django_filters.FilterSet):
    """Filter for course."""

    student__fname = django_filters.CharFilter(lookup_expr='icontains', label="Сурагчийн нэр")
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.filter(flag=True))
    flag = django_filters.BooleanFilter()

    class Meta:
        """Meta."""

        model = Contract

        fields = {
            'date': ['lt', 'gt'],
            'student__fname': ['exact'],
            'course': ['exact'],
            'flag': ['exact'],
        }


class StudentFilter(django_filters.FilterSet):
    """Filter for course."""

    fname = django_filters.CharFilter(lookup_expr='icontains', label="Нэр")
    register = django_filters.CharFilter(lookup_expr='icontains', label="Регистерийн дугаар")
    phone = django_filters.CharFilter(lookup_expr='icontains', label="Утас")

    class Meta:
        """Meta."""

        model = Student

        fields = [
            'fname',
            'register',
            'phone'
        ]


class SalaryFilter(django_filters.FilterSet):
    """Filter for course."""

    teacher__fname = django_filters.CharFilter(lookup_expr='icontains', label="Багшийн нэр")

    class Meta:
        """Meta."""

        model = TeacherSalary
        fields = ['teacher__fname', 'year', 'month']


class TransactionFilter(django_filters.FilterSet):
    """Filter for course."""

    class Meta:
        """Meta."""

        model = Transaction

        fields = {
            'txn_date': ['lt', 'gt'],
            'txn_type': ['exact'],
        }


class TransactionForm(forms.ModelForm):
    """Form for Transaction."""

    txn_type = forms.ChoiceField(choices=FORM_CHOICES, label="Төрөл")

    class Meta:
        """Meta."""

        model = Transaction
        fields = ['amount', 'txn_type', 'txn_date', 'info', 'txn_method']

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['class'] = 'form-control'
        self.fields['txn_type'].widget.attrs['class'] = 'form-control'
        self.fields['info'].widget.attrs['class'] = 'form-control'
        self.fields['txn_method'].widget.attrs['class'] = 'form-control'
        self.fields['txn_date'].widget.attrs['class'] = 'form-control datetimepicker'


class ContractfromStudentForm(forms.Form):
    """Form to register all information necessary for Contract."""

    course = forms.ModelChoiceField(label='Анги', queryset=Course.objects.filter(flag=True))
    payment = forms.IntegerField(label="Төлж буй төлбөр")
    con_date = forms.DateTimeField(label="Гэрээний огноо", initial=datetime.date.today().strftime('%m/%d/%Y'))
    txn_method = forms.ChoiceField(choices=TXN_METHODS, label="Төрөл")
    contract_number = forms.CharField(label="Гэрээний дугаар")
    minus_length = forms.IntegerField(label="Хасагдсан цаг", initial=0)
    off_percent = forms.IntegerField(label="Хямдрал", required=False, initial=0)
    description = forms.CharField(label="Тайлбар", required=False)

    def clean(self):
        """Cleaning data."""
        cleaned_data = self.cleaned_data

        course = cleaned_data.get('course')

        student = Student.objects.filter(id=self.obj_id).first()

        cls = Class.objects.filter(course=course, student=student)

        if cls:
            raise forms.ValidationError("Энэ сурагч энэ ангид гэрээ хийгдсэн байна.")
        else:
            return cleaned_data

    def __init__(self, id=None, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(ContractfromStudentForm, self).__init__(*args, **kwargs)

        for each in self.fields:
            self.fields[each].widget.attrs['class'] = 'form-control'
        self.obj_id = id
        self.fields['con_date'].widget.attrs['class'] = 'form-control datetimepicker'


class StudentLevelFilter(django_filters.FilterSet):
    """Filter for course."""

    student__fname = django_filters.CharFilter(lookup_expr='icontains', label="Оюутаны нэр")

    class Meta:
        """Meta."""

        model = StudentLevel

        fields = {
            'date': ['lt', 'gt'],
            'student__fname': ['exact'],
        }


class StudentNoLevelForm(forms.ModelForm):
    """Form for StudentLevel."""

    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Түвшин")

    class Meta:
        """Meta."""

        model = StudentLevel
        fields = ['level', 'date', 'course']

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(StudentNoLevelForm, self).__init__(*args, **kwargs)
        self.fields['course'].widget.attrs['class'] = 'form-control'
        self.fields['level'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control datetimepicker'


class StudentLevelForm(forms.ModelForm):
    """Form for StudentLevel."""

    level = forms.ChoiceField(choices=LEVEL_CHOICES, label="Түвшин")

    class Meta:
        """Meta."""

        model = StudentLevel
        fields = ['student', 'level', 'date', 'course']

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(StudentLevelForm, self).__init__(*args, **kwargs)
        self.fields['student'].widget.attrs['class'] = 'form-control'
        self.fields['course'].widget.attrs['class'] = 'form-control'
        self.fields['level'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control datetimepicker'


class StudentForm(forms.ModelForm):
    """Form for Student."""

    class Meta:
        """Meta."""

        model = Student
        fields = [
            'fname', 'lname', 'register', 'phone', 'birthday'
        ]

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(StudentForm, self).__init__(*args, **kwargs)
        for each in self.fields:
            self.fields[each].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control datetimepicker'


class WorkerForm(forms.ModelForm):
    """Form used to save Worker."""

    class Meta:
        """Meta."""

        model = Worker
        fields = [
            'fname',
            'lname',
            'register',
            'phone',
            'birthday',
            'monthly_wage',
        ]

    def __init__(self, *args, **kwargs):
        """Redefined __init__ in order to customize form."""
        super(WorkerForm, self).__init__(*args, **kwargs)

        for each in self.fields:
            self.fields[each].widget.attrs['class'] = 'form-control'
        self.fields['birthday'].widget.attrs['class'] = 'form-control datetimepicker'
