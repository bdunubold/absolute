"""Models of student registration."""

from django.db import models
from a01.choices import TXN_TYPES
from a01.choices import MONTHS
from a01.choices import LEVEL_CHOICES
from a01.choices import TXN_METHODS
from a01.choices import SHIFTS


class Student(models.Model):
    """Student's model."""

    fname = models.CharField(verbose_name='Нэр', max_length=50)
    lname = models.CharField(verbose_name='Овог', max_length=50, null=True, blank=True)
    register = models.CharField(verbose_name='Регистрийн дугаар', max_length=10, null=True, blank=True)
    phone = models.CharField(verbose_name='Утасны дугаар', max_length=20)
    birthday = models.DateField(verbose_name='Төрсөн өдөр', null=True, blank=True)
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)


    def __str__(self):
        """String representation of model."""
        if self.lname:
            return self.lname[0].upper() + "." + self.fname
        return self.fname

    class Meta:
        """meta."""

        default_permissions = ()

        verbose_name = "Сурагч"
        permissions = (
            ('s_composer', 'Сурагчтай холбоотой бүх юм'),
        )


class Worker(models.Model):
    """Model of Worker."""

    fname = models.CharField(verbose_name='Нэр', max_length=50)
    lname = models.CharField(verbose_name='Овог', max_length=50)
    register = models.CharField(verbose_name='Регистрийн дугаар', max_length=10, unique=True)
    phone = models.CharField(verbose_name='Утасны дугаар', max_length=20)
    birthday = models.DateField(verbose_name='Төрсөн он сар өдөр')
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)
    monthly_wage = models.PositiveIntegerField(verbose_name='Цагын ажлын хөлс')


    def __str__(self):
        """String representation of model."""
        if self.lname:
            return self.lname[0].upper() + "." + self.fname
        return self.fname

    class Meta:
        """Meta."""

        default_permissions = ()

        verbose_name = "Ажилтан"


class Teacher(models.Model):
    """Model of Teacher."""

    fname = models.CharField(verbose_name='Нэр', max_length=50)
    lname = models.CharField(verbose_name='Овог', max_length=50)
    register = models.CharField(verbose_name='Регистрийн дугаар', max_length=10, unique=True)
    phone = models.CharField(verbose_name='Утасны дугаар', max_length=20)
    birthday = models.DateField(verbose_name='Төрсөн он сар өдөр')
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)
    hourly_wage = models.PositiveIntegerField(verbose_name='Цагын ажлын хөлс')


    def __str__(self):
        """String representation of model."""
        if self.lname:
            return self.lname[0].upper() + "." + self.fname
        return self.fname

    class Meta:
        """Meta."""

        default_permissions = ()

        verbose_name = "Багш"


class TeacherSalary(models.Model):
    """Teacher salary."""

    teacher = models.ForeignKey(Teacher, verbose_name='Багш', blank=True, null=True, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, verbose_name='Багш', blank=True, null=True, on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(verbose_name='Сарын цалин')
    worked_hour = models.PositiveIntegerField(verbose_name='Ажилсан цаг', default=40)
    year = models.PositiveIntegerField(verbose_name='Цалин бодсон он')
    month = models.CharField(verbose_name='Цалин бодсон сар', max_length=10, choices=MONTHS)
    mshift = models.CharField(verbose_name='Ээлж', max_length=10, choices=SHIFTS)


    class Meta:
        """Meta."""

        default_permissions = ()

    @property
    def get_month(self):
        """Overriding txn_type."""
        for each in MONTHS:
            if each[0] == self.month:
                return each[1]
        return ''

    @property
    def get_shift(self):
        """Overriding txn_type."""
        for each in SHIFTS:
            if each[0] == self.mshift:
                return each[1]
        return ''


class CourseType(models.Model):
    """Model for level's of courses."""

    price = models.PositiveIntegerField(verbose_name='Үнэ')
    length = models.PositiveIntegerField(verbose_name='Нийт орох цаг')
    hourly_price = models.PositiveIntegerField(verbose_name='Цагын төлбөр')
    level = models.CharField(verbose_name='Ангийн түвшин', max_length=50)
    info = models.CharField(verbose_name='Тайлбар', max_length=200, blank=True, null=True)
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)


    def __str__(self):
        """String representation of model."""
        return self.level

    class Meta:
        """meta."""

        default_permissions = ()
        verbose_name = "Хичээлийн төрөл"


class Course(models.Model):
    """Model to store current ongoing course."""

    ctype = models.ForeignKey(CourseType, verbose_name='Түвшин', on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='Эхэлсэн цаг өдөр')
    info = models.CharField(verbose_name='Тайлбар', max_length=200, blank=True, null=True)
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)


    def __str__(self):
        """String representation of model."""
        try:
            return self.ctype.level + ", " + str(self.start_date).split('+')[0]
        except:
            return self.ctype.level

    @property
    def price(self):
        """Return price of ctype."""
        return self.ctype.price

    @property
    def hourly_price(self):
        """Return price of ctype."""
        return self.ctype.hourly_price

    class Meta:
        """meta."""

        default_permissions = ()
        permissions = (
            ('main', 'Үндсэн ажиллагаа.'),
        )
        verbose_name = "Хичээл"


class CourseTeachers(models.Model):
    """Teachers who are teaching current course."""

    teacher = models.ForeignKey(Teacher, verbose_name='Багш', related_name="tcourses", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Хичээл', related_name="cteachers", on_delete=models.CASCADE)
    lesson = models.CharField(verbose_name='Сэдэв', max_length=100)


    class Meta:
        """meta."""

        default_permissions = ()


class Class(models.Model):
    """Model of student attending course of which Teacher."""

    student = models.ForeignKey(Student, verbose_name='Сурагч', related_name="sclasses", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Хичээл', related_name="cclasses", on_delete=models.CASCADE)


    class Meta:
        """meta."""

        default_permissions = ()
        verbose_name = "Анги"


class Contract(models.Model):
    """Model to store contracts that are made with students."""

    student = models.ForeignKey(Student, verbose_name='Сурагч', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Хичээл', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Гэрээний огноо')
    minus_length = models.PositiveIntegerField(verbose_name='Хасагдсан цаг')
    total_payment = models.PositiveIntegerField(verbose_name='Нийт төлбөр')
    req_payment = models.PositiveIntegerField(verbose_name='Төлбөл зохих төлбөр')
    off_percent = models.PositiveIntegerField(verbose_name='Хямдралын хувь', default=0)
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)
    contract_number = models.CharField(verbose_name="Гэрээний дугаар", max_length=50, blank=True, null=True)
    description = models.CharField(verbose_name="Тайлбар", max_length=50, blank=True, null=True)


    class Meta:
        """meta."""

        default_permissions = ()
        verbose_name = "Гэрээ"

    def __str__(self):
        """String representation of model."""
        return "Гэрээний дугаар: " + str(self.contract_number) + ", " + str(self.date)

    def remainder_payment(self):
        return self.req_payment - self.total_payment


class Transaction(models.Model):
    """All tnxs made by absolute."""

    amount = models.PositiveIntegerField(verbose_name='Дүн')
    txn_type = models.CharField(verbose_name='Төрөл', max_length=20, choices=TXN_TYPES)
    txn_method = models.CharField(verbose_name='Гүйлгээ хийгдсэн арга', max_length=20, choices=TXN_METHODS, null=True, blank=True)
    txn_date = models.DateTimeField(verbose_name='Огноо')
    info = models.CharField(verbose_name='Тайлбар', max_length=200, default='')
    contract = models.ForeignKey(Contract, verbose_name='Гэрээ', related_name="ctxns", null=True, blank=True, on_delete=models.CASCADE)
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)
    verified = models.BooleanField(verbose_name='Баталгаажсан эсэх', default=False)


    class Meta:
        """Meta."""

        default_permissions = ()
        permissions = (
            ('accounting', 'Төлбөр тооцоотой холбоотой.'),
        )

    @property
    def get_txn_method(self):
        """Overriding txn_type."""
        for each in TXN_METHODS:
            if each[0] == self.txn_method:
                return each[1]
        return ''

    @property
    def get_txn_type(self):
        """Overriding txn_type."""
        for each in TXN_TYPES:
            if each[0] == self.txn_type:
                return each[1]
        return ''

    def __str__(self):
        """String representation of model."""
        return str(self.txn_date) + ", " + self.info


class StudentLevel(models.Model):
    """English level of student."""

    student = models.ForeignKey(Student, verbose_name='Сурагч', related_name="levels", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='Хичээл', blank=True, null=True, on_delete=models.CASCADE)
    level = models.CharField(verbose_name='Хэлний түвшин', max_length=20, choices=LEVEL_CHOICES)
    date = models.DateField(verbose_name='Огноо')
    flag = models.BooleanField(verbose_name='Идэвхитэй эсэх', default=True)


    @property
    def get_level(self):
        """Overriding txn_type."""
        for each in LEVEL_CHOICES:
            if each[0] == self.level:
                return each[1]
        return ''

    class Meta:
        """Meta."""

        default_permissions = ()
