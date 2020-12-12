from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.


class User(models.Model):
    name = models.CharField(db_column='name', max_length=25)
    email = models.EmailField(db_column='email', max_length=254, unique=True)
    contact_num = models.CharField(db_column='contact_num', max_length=25)
    password = models.CharField(db_column='password', max_length=50, null=True)

    class Meta:
        abstract = True
        db_table = 'user'


class Sitter_User(User):
    GENDER_OPTIONS = (
        ('F', 'Female'),
        ('M', 'Male'),
    )
    gender = models.CharField(
        db_column='gender', max_length=1, choices=GENDER_OPTIONS)
    b_date = models.DateTimeField(db_column='b_date')
    cctv = models.BooleanField(db_column='cctv', default=False)
    crime_history = models.BooleanField(
        db_column='crime_history', default=False)

    class Meta:
        db_table = 'sitter_user'


class Parent_User(User):
    children_info = models.CharField(db_column='children_info', max_length=400)

    class Meta:
        db_table = 'parent_user'


class Application(models.Model):
    user = models.ForeignKey(
        Sitter_User, on_delete=models.CASCADE, primary_key=False, null=True)
    title = models.CharField(db_column='title', max_length=80)
    content = models.TextField(db_column='content')
    # filefield vs filepathfield ?
    attached_file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(
        allowed_extensions=['pdf', "doc", 'docx', 'jpg', 'jpeg', 'png'])])
    date = models.DateTimeField(db_column='date', auto_now_add=True, null=True)

    class Meta:
        db_table = 'application'


class Work_Condition(models.Model):
    SERVICE_OPTION = (
        ('H', 'House Sitter'),
        ('P', 'Play Sitter'),
        ('L', 'Learning Sitter'),
        ('D', 'Day Care'),
        ('E', 'Else'),
    )
    GENDER_OPTION = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('E', 'Else')
    )
    WORK_PERIOD_OPTION = (
        ('S', 'Short (one day to one month)'),
        ('M', 'Medium (one month to six months)'),
        ('L', 'Long (six months to one year)'),
    )
    type_of_service = models.CharField(
        db_column='type_of_service', max_length=1, choices=SERVICE_OPTION)
    work_period = models.CharField(
        db_column='work_period', max_length=1, choices=WORK_PERIOD_OPTION)
    begin_work_time = models.TimeField(
        db_column='begin_work_time', auto_now=False, auto_now_add=False)
    end_work_time = models.TimeField(
        db_column='end_work_time', auto_now=False, auto_now_add=False)
    location = models.CharField(db_column='location', max_length=80)
    gender = models.CharField(
        db_column='gender', max_length=1, choices=GENDER_OPTION)
    payrate = models.IntegerField(db_column='payrate')

    class Meta:
        db_table = 'work_condition'


class Post(models.Model):
    post_date = models.DateTimeField(db_column='post_date', auto_now_add=True)
    writer_id = models.IntegerField(db_column='writer_id')
    writer_name = models.CharField(
        db_column='writer_name', max_length=80, null=True)
    title = models.CharField(db_column='title', max_length=80)
    content = models.TextField(db_column='content')

    class Meta:
        abstract = True
        db_table = 'post'


# Post uploaded to For Parents page
class Sitter_Post(Post):
    work_condition = models.OneToOneField(
        Work_Condition, on_delete=models.CASCADE, primary_key=False)

    class Meta:
        db_table = 'sitter_post'


# Post uploaded to For Sitter page
class Parent_Post(Post):
    work_condition = models.OneToOneField(
        Work_Condition, on_delete=models.CASCADE, primary_key=False)

    class Meta:
        db_table = 'parent_post'


class Application_Manager(models.Model):
    post = models.ForeignKey(
        Parent_Post, on_delete=models.CASCADE, primary_key=False, null=True)
    post_owner_id = models.IntegerField(db_column='post_owner_id')
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, primary_key=False, null=True)
    applicant_id = models.IntegerField(db_column='applicant_id')
    date = models.DateTimeField(db_column='date', auto_now_add=True, null=True)

    class Meta:
        unique_together = (('post', 'applicant_id'))
        db_table = 'application_manager'


class Review(models.Model):
    rating = models.DecimalField(
        db_column='rating', max_digits=2, decimal_places=1)
    reviewer_id = models.CharField(db_column='reviewer_id', max_length=20)
    reviewed_user_id = models.CharField(
        db_column='reviewed_user_id', max_length=20)
    review_content = models.TextField(db_column='review_content')
    after_service = models.BooleanField(
        db_column='after_service', default=False)

    class Meta:
        db_table = 'review'


class Message(models.Model):
    sent_date = models.DateTimeField(db_column='sent_date', auto_now_add=True)
    sender_id = models.CharField(db_column='sender_id', max_length=20)
    receiver_id = models.CharField(db_column='receiver_id', max_length=20)
    message_content = models.TextField(db_column='message_content')

    class Meta:
        db_table = 'message'


class Message_History(models.Model):
    MESSAGE_STATUS_OPTIONS = (
        ('R', 'Read'),
        ('U', 'Unread'),
    )
    sent_date = models.DateTimeField(db_column='sent_date', auto_now_add=True)
    message_status = models.CharField(
        db_column='message_status', max_length=1, choices=MESSAGE_STATUS_OPTIONS, default='U')
    owner_id = models.CharField(db_column='owner_id', max_length=20)
    other_owner_id = models.CharField(
        db_column='other_owner_id', max_length=20)

    class Meta:
        unique_together = (('owner_id', 'other_owner_id'))
        db_table = 'message_history'


class Qna(models.Model):
    title = models.CharField(db_column='title', max_length=80)
    content = models.TextField(db_column='content')
    answer = models.TextField(db_column='answer')
    writer_id = models.IntegerField(db_column='writer_id')
    date = models.DateTimeField(db_column='written_date', auto_now_add=True)

    class Meta:
        db_table = 'qna'
