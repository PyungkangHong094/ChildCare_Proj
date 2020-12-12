from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from Ihelprapp.serializer.PostSerializer import *
from Ihelprapp.serializer.WorkConditionSerializer import *
from Ihelprapp.serializer.MessageSerializer import *
from .forms import ApplicationForm
from django.urls import reverse
import json

# Create your views here.


def checkLogin(request):
    context = {}

    if 'member_no' in request.session:
        context["member_no"] = request.session['member_no']
        context["member_name"] = request.session['member_name']
        context["member_type"] = request.session['member_type']
        # context["member_info"] = request.session['member_info']
    else:
        context["member_no"] = None
        context["member_name"] = None
    return context


def home(request):
    context = checkLogin(request)
    return render(request, 'homepage.html', context)


def about(request):
    context = checkLogin(request)
    return render(request, 'about.html', context)


def application(request):
    context = checkLogin(request)

    sitter_user_instance = Sitter_User.objects.get(id=context["member_no"])
    context["member_id"] = sitter_user_instance.id
    context["member_email"] = sitter_user_instance.email
    context["member_number"] = sitter_user_instance.contact_num
    context["member_bday"] = sitter_user_instance.b_date
    context["member_gender"] = sitter_user_instance.gender
    context["member_cctv"] = sitter_user_instance.cctv
    context["member_criminal"] = sitter_user_instance.crime_history
    context["form"] = ApplicationForm()
    context["flag"] = "0"
    context["result"] = 'Member info'

    if request.method == 'GET':

        request.session['next'] = request.META.get('HTTP_REFERER')
        # application_instance = Application.objects.all().get(id=)

    if request.method == 'POST':

        form = ApplicationForm(request.POST, request.FILES)
        sitter_user_instance = Sitter_User.objects.get(id=context["member_id"])

        data = dict({
            'user': sitter_user_instance,
            'title': request.POST['title'],
            'content': request.POST['content'],
            'attached_file': request.FILES['attached_file']
        })

        next_page = request.session['next']

        if form.is_valid():

            application_instance = Application.objects.create(
                user=data['user'], title=data['title'], content=data['content'], attached_file=data['attached_file'])
            application_instance.save()

        return HttpResponseRedirect(next_page)

    return render(request, 'application.html', context)


def delete_application(request):
    context = checkLogin(request)
    application = request.GET['application_id']
    delete_application = Application.objects.all().get(id=application).delete()
    application_list = Application.objects.all().filter(
        user_id=request.session['member_no']).order_by("date")
    context["application_list"] = application_list

    history = Application_Manager.objects.all().filter(application_id=application)
    if len(history) != 0:
        delete_application_his = Application_Manager.objects.all().filter(
            application_id=application).delete()
        apply_history = Application_Manager.objects.all().get(
            applicant_id=request.session['member_no'])
        context["apply_history"] = apply_history

    return redirect("/mypage", context)


def select_application(request):

    context = checkLogin(request)
    context["application_list"] = get_application_list(context['member_no'])

    return render(request, 'selectApplication.html', context)


def apply(request):

    context = checkLogin(request)

    if request.method == 'GET':
        
        application_id = request.GET['application-id']
        post_id = request.session['view_post_id']
        post_owner_id = request.session['writer_id']
        sitter_user_id = request.session['member_no']

        if application_id != None and post_id != None and post_owner_id != None and sitter_user_id:
            application = Application.objects.all().get(id=application_id)
            post = Parent_Post.objects.all().get(id=post_id)

            if Application_Manager.objects.all().filter(post=post, applicant_id=sitter_user_id) == None:
                applied = Application_Manager.objects.create(post=post, post_owner_id=post_owner_id, application=application, applicant_id=sitter_user_id)
                context["result"] = "Successfully Applied!"

                return redirect("/mypage", context)
            else: 
                context["result"] = "You have already applied to this post"
                return JsonResponse(context, content_type="application/json")

def cancel_apply(request):

    context = checkLogin(request)
    post_applied_id = request.GET['post_applied_id']
    delete_application = Application_Manager.objects.all().get(
        post_id=post_applied_id).delete()
    apply_history = Application_Manager.objects.all().filter(
        applicant_id=request.session['member_no']).order_by("date")
    context["apply_history"] = apply_history

    return redirect("/mypage", context)


def for_parents(request):
    context = checkLogin(request)
    if 'type_of_service' in request.GET:
        type_of_service = request.GET['type_of_service']
        work_period = request.GET['work_period']
        begin_work_time = request.GET['begin_work_time']
        begin_work_time = begin_work_time+'.000000'
        end_work_time = request.GET['end_work_time']
        end_work_time = end_work_time+'.000000'
        location = request.GET['location']
        gender = request.GET['gender']
        payrate = request.GET['payrate']
        # Need to perfect Match for Parent!
        sitter_post_list = Sitter_Post.objects.select_related('work_condition').filter(
            work_condition__type_of_service=type_of_service,
            work_condition__work_period=work_period,
            work_condition__location=location,
            work_condition__begin_work_time=begin_work_time,
            work_condition__end_work_time=end_work_time,
            work_condition__gender=gender,
            work_condition__payrate=payrate)
    else:
        sitter_post_list = Sitter_Post.objects.all().order_by("-post_date")

    context["sitter_list"] = sitter_post_list
    return render(request, 'forParents.html', context)


def for_sitters(request):
    context = checkLogin(request)
    if 'type_of_service' in request.GET:
        type_of_service = request.GET['type_of_service']

        work_period = request.GET['work_period']
        begin_work_time = request.GET['begin_work_time']
        begin_work_time = begin_work_time+'.000000'
        end_work_time = request.GET['end_work_time']
        end_work_time = end_work_time+'.000000'
        location = request.GET['location']
        gender = request.GET['gender']
        payrate = request.GET['payrate']
        # Need to perfect Match for Parent!
        parent_post_list = Parent_Post.objects.select_related('work_condition').filter(
            work_condition__type_of_service=type_of_service,
            work_condition__work_period=work_period,
            work_condition__location=location,
            work_condition__begin_work_time=begin_work_time,
            work_condition__end_work_time=end_work_time,
            work_condition__gender=gender,
            work_condition__payrate=payrate)
    else:
        parent_post_list = Parent_Post.objects.all().order_by("-post_date")

    context["Parent_list"] = parent_post_list
    return render(request, 'forSitters.html', context)


def login(request):

    return render(request, 'logIn.html')


def review(request):

    context = checkLogin(request)
    request.session['reviewReceiver'] = request.GET['other']
    context['reviewReceiver'] = request.GET['other']

    return render(request, 'review.html', context)


@csrf_exempt
def write_review(request):
    context = checkLogin(request)
    request_body = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':
        review_serializer = ReviewSerializer(data=request_body['review'])
        if review_serializer.is_valid():
            review_instance = review_serializer.save()

    context["result"] = "Successfully rated and reviewed!"
    return JsonResponse(context, content_type="application/json")


def messages(request):
    context = checkLogin(request)

    user_id = context['member_no']
    user_type = get_user_type(request.session['member_type'])

    message_history_ = Message_History.objects.all().filter(
        owner_id=str(user_id)+user_type)

    if message_history_ != None:
        unread_msg = message_history_.filter(
            message_status='U').order_by("-sent_date")
        read_msg = message_history_.filter(
            message_status='R').order_by("-sent_date")

        context['unread'] = get_name_and_date(unread_msg)
        context['read'] = get_name_and_date(read_msg)

    return render(request, 'messages.html', context)


def get_name_and_date(message_history_):
    message_data = {}
    counter = 0

    for data in message_history_:
        sender = data.other_owner_id
        date = data.sent_date
        other_owner = data.other_owner_id
        sender_id = sender[:len(sender)-1]
        sender_user_type = sender[len(sender)-1:]

        if sender_user_type == 'S':
            sender_data = Sitter_User.objects.all().get(id=sender_id)

        else:
            sender_data = Parent_User.objects.all().get(id=sender_id)

        sender_name = sender_data.name

        sender_name = sender_data.name
        message_data[counter] = dict(
            {'name': sender_name, 'date': date, 'other_owner_id': other_owner})
        counter += 1

    return message_data


def get_conversation(sender, receiver):
    context = {}
    message_list = Message.objects.all()
    a = message_list.filter(sender_id=sender,
                            receiver_id=receiver)
    b = message_list.filter(sender_id=receiver,
                            receiver_id=sender)
    conversation = a.union(b).order_by("sent_date")
    conversation_data = {}
    counter = 0

    for data in conversation:
        sender = data.sender_id
        date = data.sent_date
        content = data.message_content
        sender_id = sender[:len(sender)-1]
        sender_user_type = sender[len(sender)-1:]

        if sender_user_type == 'S':
            sender_data = Sitter_User.objects.all().get(id=sender_id)
        else:
            sender_data = Parent_User.objects.all().get(id=sender_id)

        sender_name = sender_data.name
        conversation_data[counter] = dict(
            {'name': sender_name, 'date': date, 'content': content})
        counter += 1

    context["conversation"] = conversation_data
    return context


@csrf_exempt
def view_message(request):
    context = checkLogin(request)
    userId = request.session['member_no']
    user_type = get_user_type(request.session['member_type'])

    other_id = request.GET['other']
    request.session['the_other'] = other_id

    if request.GET['status'] == 'Unread':
        context = unread(str(userId)+user_type, other_id)

    context = get_conversation(str(userId)+user_type, other_id)
    return render(request, 'viewMessage.html', context)


@csrf_exempt
def mark_as_read(request):
    context = checkLogin(request)
    userId = request.session['member_no']
    other_id = request.GET['other']
    user_type = get_user_type(request.session['member_type'])

    context = unread(str(userId)+user_type, other_id)
    # return render(request, 'messages.html', context)
    return redirect("/messages", context)


def unread(sender, receiver):
    context = {}
    message_history_ = Message_History.objects.all().get(
        owner_id=sender, other_owner_id=receiver)
    message_history_.message_status = 'R'
    message_history_.save()
    message_history_ = Message_History.objects.all().filter(owner_id=sender)
    if len(message_history_) != 0:
        unread_msg = message_history_.filter(message_status='U')
        read_msg = message_history_.filter(message_status='R')

    # context["unread_msg"] = unread_msg
    # context["read_msg"] = read_msg
    context['unread'] = get_name_and_date(unread_msg)
    context['read'] = get_name_and_date(read_msg)
    return context


def get_user_type(user_type):
    if user_type == 'Sitter':
        user_type = 'S'
    else:
        user_type = 'P'
    return user_type


@csrf_exempt
def view_my_post_list(request):
    context = checkLogin(request)

    user_id = context['member_no']
    user_type = context["member_type"]

    if user_type == "Parent":
        context['post_list'] = Parent_Post.objects.all().filter(
            writer_id=user_id)

    elif user_type == "Sitter":
        context['post_list'] = Sitter_Post.objects.all().filter(
            writer_id=user_id)

    else:
        print("Invalid user type: " + user_type)

    return render(request, 'myPosts.html', context)


def post_page(request):
    context = checkLogin(request)
    return render(request, 'postPage.html', context)


def qna(request):
    context = checkLogin(request)
    question_list = Qna.objects.all().order_by("-date")
    context["question_list"] = question_list
    return render(request, 'qna.html', context)


def sign_up(request):
    return render(request, 'signUp.html')


def sitters_signup(request):
    return render(request, 'sitters_signup.html')


def parents_signup(request):
    return render(request, 'parents_signup.html')


def view_post(request, post_id, post_type):
    context = checkLogin(request)

    if request.method == 'GET':
        post_id = post_id
        post_type = post_type
        if post_type == 'S':

            post_detail = Sitter_Post.objects.get(id=post_id)
            context["post_detail"] = post_detail
            context["post_type"] = post_type
            request.session['writer_id'] = str(post_detail.writer_id)
            request.session['post_type'] = post_type
            context['gender'] = getGender(post_detail.work_condition.gender)
            context['service'] = getService(
                post_detail.work_condition.type_of_service)
            context['period'] = getPeriod(
                post_detail.work_condition.work_period)
            return render(request, 'viewPost.html', context)

        elif post_type == 'P':

            post_detail = Parent_Post.objects.all().get(id=post_id)
            context["post_detail"] = post_detail
            context["post_type"] = post_type
            request.session['view_post_id'] = str(post_id)
            request.session['writer_id'] = str(post_detail.writer_id)
            request.session['post_type'] = post_type
            context['gender'] = getGender(post_detail.work_condition.gender)
            context['service'] = getService(
                post_detail.work_condition.type_of_service)
            context['period'] = getPeriod(
                post_detail.work_condition.work_period)
            return render(request, 'viewPost.html', context)

        else:
            return render(request, '/', "Error")


def view_my_post(request):
    context = checkLogin(request)
    post_type = get_user_type(request.session['member_type'])
    post_id = request.GET['mypost_id']

    if post_type == 'S':

        post_detail = Sitter_Post.objects.get(id=post_id)
        context["post_detail"] = post_detail
        context["post_type"] = post_type
        request.session['writer_id'] = str(post_detail.writer_id)
        request.session['post_type'] = post_type
        context['gender'] = getGender(post_detail.work_condition.gender)
        context['service'] = getService(
            post_detail.work_condition.type_of_service)
        context['period'] = getPeriod(
            post_detail.work_condition.work_period)
        return render(request, 'viewPost.html', context)

    elif post_type == 'P':

        post_detail = Parent_Post.objects.all().get(id=post_id)
        context["post_detail"] = post_detail
        context["post_type"] = post_type
        request.session['view_post_id'] = str(post_id)
        request.session['writer_id'] = str(post_detail.writer_id)
        request.session['post_type'] = post_type
        context['gender'] = getGender(post_detail.work_condition.gender)
        context['service'] = getService(
            post_detail.work_condition.type_of_service)
        context['period'] = getPeriod(
            post_detail.work_condition.work_period)
        return render(request, 'viewPost.html', context)

    else:
        return render(request, '/', "Error")


def getGender(input_):
    if input_ == 'f':
        return 'Female'
    elif input_ == 'm':
        return 'Male'
    else:
        return 'Do not want to show'


def getService(input_):
    if input_ == 'H':
        return 'House Sitter'
    elif input_ == 'P':
        return 'Play Sitter'
    elif input_ == 'L':
        return 'Learning Sitter'
    elif input_ == 'D':
        return 'Day care'
    else:
        return 'Else'


def getPeriod(input_):
    if input_ == 'S':
        return 'Short (1day - 1month)'
    elif input_ == 'M':
        return 'Medium (1month - 6month)'
    else:
        return 'Long (6month - 1year)'


def ask_question(request):
    context = checkLogin(request)
    return render(request, 'askQuestion.html')


def post_job(request):
    context = checkLogin(request)
    return render(request, 'postJob.html', context)


def edit_my_post(request):
    context = checkLogin(request)
    my_post_id = request.GET['mypost_id']
    edit_post = Mypost.objects.all().get(mypost_id=my_post_id)
    context["edit_post"] = edit_post
    return render(request, 'editMyPost.html', context)


def search(request, post_type):
    post_type = post_type
    input_ = request.POST.get('input_', "")

    if post_type == 'P':
        parent_post_list = Parent_Post.objects.all().order_by('-post_date')
        if input_:
            parent_post_list = parent_post_list.filter(title__icontains=input_)
        return render(request, 'forSitters.html', {'Parent_list': parent_post_list, 'input_': input_})
    else:
        sitter_post_list = Sitter_Post.objects.all().order_by('-post_date')
        if input_:
            sitter_post_list = sitter_post_list.filter(title__icontains=input_)
            print(sitter_post_list)
        return render(request, 'forParents.html', {'sitter_list': sitter_post_list, 'input_': input_})


def view_applicant(request):
    context = checkLogin(request)
    my_post_id = request.GET['mypost_id']

    applicant_list = Application_Manager.objects.filter(
        post_id=my_post_id).order_by("date")
    applicant_list = applicant_list.select_related('application')
    context["applicant_list"] = applicant_list
    return render(request, 'viewApplicant.html', context)


def delete_my_post(request):
    context = checkLogin(request)
    my_post_id = request.GET['mypost_id']
    user_type = get_user_type(request.session['member_type'])

    if user_type == 'S':
        work_cond = Work_Condition.objects.get(
            id=Sitter_Post.objects.get(id=my_post_id).work_condition_id).delete()
        post_list = Sitter_Post.objects.all().order_by("-post_date")
        context["post_list"] = post_list
        return redirect("/mypost", context)

    elif user_type == 'P':
        work_cond = Work_Condition.objects.get(
            id=Parent_Post.objects.get(id=my_post_id).work_condition_id).delete()
        post_list = Parent_Post.objects.all().order_by("-post_date")
        context["post_list"] = post_list

        history = Application_Manager.objects.all().filter(post_id=my_post_id)
        if len(history) != 0:
            delete_application_his = Application_Manager.objects.all().filter(
                post_id=my_post_id).delete()
        return redirect("/mypost", context)

    else:
        return render(request, '/', "Error")


@csrf_exempt
def ask_created(request):
    context = checkLogin(request)
    context["member_no"] = request.session['member_no']
    question_title = request.GET['q_title']
    question_text = request.GET['q_text']
    question_list = Qna.objects.create(
        title=question_title, content=question_text, date=datetime.now(), answer='Not replied yet!', writer_id=request.session['member_no'])

    context["result"] = "Successfully Post Question"
    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def send_message(request):
    context = checkLogin(request)
    request_body = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':
        message_serializer = MessageSerializer(data=request_body['message'])
        # print(message_serializer.is_valid())
        # print(message_serializer.errors)
        if message_serializer.is_valid():
            message_instance = message_serializer.save()
            message_history_serializer = MessageHistorySerializer(
                data=request_body['message_history'])
            message_history2_serializer = MessageHistorySerializer(
                data=request_body['message_history2'])

        if message_history_serializer.is_valid():
            message_history_instance = message_history_serializer.save()
        if message_history2_serializer.is_valid():
            message_history2_instance = message_history2_serializer.save()

    context["result"] = "Successfully Sent message"
    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def in_view_send_msg(request):
    context = checkLogin(request)
    if 'member_no' in request.session:
        user_type = request.session['member_type']
        if user_type == "Sitter":
            sender_type = 'S'
            receiver_type = 'P'
        else:
            sender_type = 'P'
            receiver_type = 'S'

    message = request.GET['message_content']
    receiver_id = request.session['the_other']
    sender_id = str(request.session['member_no']) + sender_type
    msg = Message.objects.create(
        sent_date=datetime.now(), sender_id=sender_id, receiver_id=receiver_id, message_content=message)
    msg.save()

    sender_msgHistory = Message_History.objects.all().get(
        owner_id=sender_id, other_owner_id=receiver_id)
    sender_msgHistory.message_status = 'R'
    sender_msgHistory.sent_date = datetime.now()
    sender_msgHistory.save()

    try:
        receiver_msgHistory = Message_History.objects.all().get(
            owner_id=receiver_id, other_owner_id=sender_id)

        receiver_msgHistory.message_status = 'U'
        receiver_msgHistory.sent_date = datetime.now()
        receiver_msgHistory.save()

    except Message_History.DoesNotExist:
        msg_history = Message_History.objects.create(
            sent_date=datetime.now(), owner_id=receiver_id, other_owner_id=sender_id, message_status='U')
        msg_history.save()

    message_history_ = Message_History.objects.all().filter(owner_id=sender_id)
    if len(message_history_) != 0:
        unread_msg = message_history_.filter(
            message_status='U').order_by("-sent_date")
        read_msg = message_history_.filter(
            message_status='R').order_by("-sent_date")

        context['unread'] = get_name_and_date(unread_msg)
        context['read'] = get_name_and_date(read_msg)

    return render(request, 'messages.html', context)


def write_message(request):
    context = checkLogin(request)
    context["writer_id"] = request.session['writer_id']
    context["post_type"] = request.session['post_type']
    return render(request, 'writeMessage.html', context)


def delete_message(request):
    user_type = get_user_type(request.session['member_type'])

    context = checkLogin(request)
    owner_id = str(request.session['member_no']) + user_type
    the_other = request.GET['other']

    deleteMH = Message_History.objects.all().get(
        owner_id=owner_id, other_owner_id=the_other).delete()
    message_history_ = Message_History.objects.all().filter(
        owner_id=owner_id)
    if len(message_history_) != 0:
        unread_msg = message_history_.filter(
            message_status='U').order_by("-sent_date")
        read_msg = message_history_.filter(
            message_status='R').order_by("-sent_date")
        context['unread'] = get_name_and_date(unread_msg)
        context['read'] = get_name_and_date(read_msg)
    return redirect("/messages", context)


def view_question(request):
    context = checkLogin(request)
    id = request.GET['id']
    question_instance = Qna.objects.get(id=id)
    context["q_title"] = question_instance.title
    context["q_content"] = question_instance.content
    context["q_date"] = question_instance.date
    context["answer"] = question_instance.answer
    return render(request, 'viewQuestion.html', context)


@csrf_exempt
def create_post(request):

    request_body = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':

        work_condition_serializer = WorkConditionSerializer(
            data=request_body['work_condition'])

        if work_condition_serializer.is_valid():

            work_condition_instance = work_condition_serializer.save()
            request_body['work_condition'] = work_condition_instance.id

            if request_body['post_type'] == 'parent_post':

                post_serializer = ParentPostSerializer(data=request_body)

                if post_serializer.is_valid():

                    post_instance = post_serializer.save()

                    return JsonResponse({}, content_type="application/json")

            elif request_body['post_type'] == 'sitter_post':

                post_serializer = SitterPostSerializer(data=request_body)

                if post_serializer.is_valid():

                    post_instance = post_serializer.save()

                    return JsonResponse({}, content_type="application/json")

        context["result"] = "The form you have submitted is invalid. Please resubmit with correct information."

        return JsonResponse(context, content_type="application/json")


@csrf_exempt
def update_post(request):

    request_body = JSONParser.parse(request)

    post = PostSerializer(data=request_body)

    if request.method == 'PUT':
        request_body = JSONParser().parse(request)
        post = PostSerializer(data=request_body)
        if post.is_valid():
            post.save()

            return JsonResponse(post.data, status=status.HTTP_200_OK)

    return JsonResponse(post.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def parent_insert(request):
    context = {}

    member_pwd = request.GET['password']
    member_name = request.GET['name']
    member_email = request.GET['email']
    member_number = request.GET['contact_num']
    member_child = request.GET['children_info']

    parent_user_instance = Parent_User.objects.create(name=member_name, password=member_pwd,
                                                      email=member_email, contact_num=member_number,
                                                      children_info=member_child)

    context["result"] = "Successfull"
    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def sitter_insert(request):
    context = {}
    member_email = request.GET['email']
    member_pwd = request.GET['password']
    member_name = request.GET['name']

    member_number = request.GET['contact_num']
    member_bday = request.GET['b_date']
    member_gender = request.GET['gender']

    member_cctv = request.GET['cctv']

    if member_cctv == "true":
        check_cctv = True

    else:
        check_cctv = False

    member_criminal = request.GET['crime_history']

    if member_criminal == "true":
        check_criminal = True

    else:
        check_criminal = False

    context["result"] = "Successfull"

    application = Application.objects.last()
    sitter_user_instance = Sitter_User.objects.create(name=member_name, password=member_pwd,
                                                      email=member_email, contact_num=member_number, b_date=member_bday,
                                                      gender=member_gender, crime_history=check_criminal,
                                                      cctv=check_cctv)

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def parent_idcheck(request):
    context = {}
    if request.method == 'POST':
        memberemail = request.GET['email']
    # print("----")
    # print(memberemail)
    rs = Parent_User.objects.filter(email=memberemail)

    if(len(rs)) > 0:
        context["flag"] = "1"
        context["result"] = "Eamil already exist "
    else:
        context["flag"] = "0"
        context["result"] = "Email you can use it"

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def sitter_idcheck(request):
    context = {}
    if request.method == 'POST':
        memberemail = request.GET['email']

    rs = Sitter_User.objects.filter(email=memberemail)
    if(len(rs)) > 0:
        context["flag"] = "1"
        context["result"] = "Eamil already exist "
    else:
        context["flag"] = "0"
        context["result"] = "Email you can use it"
    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def member_login(request):

    context = {}
    member_email = request.GET['email']
    member_pwd = request.GET['password']

    if 'member_no' in request.session:
        context["flag"] = "1"
        context["result"] = 'Already Log in'

    else:

        try:

            parent_user_instance = Parent_User.objects.get(
                email=member_email, password=member_pwd)

            member_no = parent_user_instance.id
            member_name = parent_user_instance.name

            request.session['member_no'] = member_no
            request.session['member_name'] = member_name
            request.session['member_type'] = "Parent"
            request.session['member_info'] = str(
                member_no) + get_user_type(request.session['member_type'])

            context["flag"] = "0"
            context["result"] = "Parent User Successfully"

        except:

            try:

                sitter_user_instance = Sitter_User.objects.get(
                    email=member_email, password=member_pwd)

                member_no = sitter_user_instance.id
                member_name = sitter_user_instance.name

                request.session['member_no'] = member_no
                request.session['member_name'] = member_name
                request.session['member_type'] = "Sitter"
                request.session['member_info'] = str(
                    member_no) + get_user_type(request.session['member_type'])

                context["flag"] = "0"
                context["result"] = "Sitter User Successfully"

            except:

                context["flag"] = "1"
                context["result"] = "NOT Log in try again"

    return JsonResponse(context, content_type="application/json")


def logout(request):
    request.session.flush()
    return redirect("/")


def mypage(request):

    context = {}
    user_instance = None

    if 'member_no' in request.session:
        context["member_no"] = request.session['member_no']
        context["member_name"] = request.session['member_name']
        context["member_type"] = request.session['member_type']
    else:
        context["member_no"] = None
        context["member_name"] = None

    if 'member_no' in request.session:
        context["user_id"] = request.session['member_no']
        context["user_name"] = request.session['member_name']
        context["user_type"] = request.session['member_type']

        if context["user_type"] == "Parent":
            user_instance = Parent_User.objects.get(id=context["user_id"])

        else:
            user_instance = Sitter_User.objects.get(id=context["user_id"])
            context["user_bday"] = user_instance.b_date
            context["user_gender"] = user_instance.gender
            context["user_CCTV"] = user_instance.cctv
            context["user_criminal"] = user_instance.crime_history
            context["application_list"] = get_application_list(
                context["user_id"])

        context["user_number"] = user_instance.contact_num
        context["user_email"] = user_instance.email
        context["flag"] = "0"
        context["result"] = 'Member info'

    else:
        redirect("/")

    context = get_review_and_rating(context, request.session['member_info'])
    context = get_review_I_made(context, request.session['member_info'])
    context = view_applied_history(context, context["user_id"])

    return render(request, 'myPage.html', context)


def get_review_and_rating(context, member_info):

    review_list = Review.objects.all().filter(
        reviewed_user_id=member_info)

    if len(review_list) > 0:
        context['review_list'] = get_reviewer_and_date(review_list)
        ave_rating = 0

        for i in review_list:
            ave_rating = ave_rating + i.rating

        ave_rating = round((ave_rating / len(review_list)), 2)
        context["ave_rating"] = ave_rating
    else:
        context["ave_rating"] = 0
    return context


def get_review_I_made(context, member_info):

    review_history = Review.objects.all().filter(reviewer_id=member_info)

    if len(review_history) > 0:
        context['review_history'] = get_review_history(review_history)

    return context


def get_review_history(review):

    review_data = {}
    counter = 0

    for data in review:
        reviewed = data.reviewed_user_id
        rating = data.rating
        content = data.review_content
        service_used = data.after_service
        reviewer_id = reviewed[:len(reviewed)-1]
        reviewer_user_type = reviewed[len(reviewed)-1:]
        review_id = data.id

        if reviewer_user_type == 'S':
            reviewer_data = Sitter_User.objects.all().get(id=reviewer_id)
        else:
            reviewer_data = Parent_User.objects.all().get(id=reviewer_id)

        reviewer_name = reviewer_data.name

        review_data[counter] = dict(
            {'name': reviewer_name, 'rating': rating, 'content': content, 'service_used': service_used, 'review_id': review_id})
        counter += 1

    return review_data


def delete_review(request):
    context = checkLogin(request)
    review_id = request.GET['review_id']

    delete_review = Review.objects.all().get(id=review_id).delete()
    context = get_review_I_made(context, request.session['member_info'])
    return redirect("/mypage", context)


def get_reviewer_and_date(review):

    review_data = {}
    counter = 0

    for data in review:
        reviewer = data.reviewer_id
        rating = data.rating
        content = data.review_content
        service_used = data.after_service
        reviewer_id = reviewer[:len(reviewer)-1]
        reviewer_user_type = reviewer[len(reviewer)-1:]

        if reviewer_user_type == 'S':
            reviewer_data = Sitter_User.objects.all().get(id=reviewer_id)
        else:
            reviewer_data = Parent_User.objects.all().get(id=reviewer_id)

        reviewer_name = reviewer_data.name

        review_data[counter] = dict(
            {'name': reviewer_name, 'rating': rating, 'content': content, 'service_used': service_used})
        counter += 1

    return review_data


def get_application_list(user_id):
    application_list = Application.objects.all().filter(
        user_id=user_id).order_by("date")
    return application_list


def view_applied_history(context, user_id):

    apply_history = Application_Manager.objects.all().filter(
        applicant_id=user_id).order_by("date")
    apply_history = apply_history.select_related('post')
    apply_history = apply_history.select_related('application')

    if apply_history != None:
        context['apply_history'] = apply_history

    return context


def view_application(request, application_id):
    context = {}
    user_information = Sitter_User.objects.all().get(
        id=request.session['member_no'])
    context['user_information'] = user_information
    if user_information.gender == 'F':
        context['gender'] = 'Female'
    else:
        context['gender'] = 'Male'
    context['cctv'] = agree_disagree(user_information.cctv)
    context['crime_history'] = agree_disagree(user_information.crime_history)

    application_contents = Application.objects.all().get(id=application_id)
    context['application_contents'] = application_contents
    return render(request, 'viewApplication.html', context)


def agree_disagree(input):
    if input == 'F':
        return 'Disagreed'
    else:
        return 'Agreed'

# update


@csrf_exempt
def member_update(request):

    context = {}

    if 'member_no' in request.session:
        context["member_no"] = request.session['member_no']
        context["member_name"] = request.session['member_name']
        context["member_type"] = request.session['member_type']

    else:
        return redirect("/")

    member_name = request.GET['name']
    member_email = request.GET['email']
    member_number = request.GET['contact_num']

    member_gender = request.GET['gender']
    member_cctv = request.GET['cctv']
    member_criminal = request.GET['crime_history']

    if context["member_type"] == "Parent":

        user_instance = Parent_User.objects.get(id=context["member_no"])

        user_instance.name = member_name
        user_instance.email = member_email
        user_instance.contact_num = member_number
        user_instance.save()

        request.session['member_name'] = member_name
        context["flag"] = "0"
        context["result"] = 'Member update!!!'

        return JsonResponse(context, content_type="application/json")

    else:

        user_instance = Sitter_User.objects.get(id=context["member_no"])

        if member_cctv == "true":
            check_cctv = True

        else:
            check_cctv = False

        if member_criminal == "true":
            check_criminal = True

        else:
            check_criminal = False
        print(check_cctv)
        print(check_criminal)

        user_instance.name = member_name
        user_instance.email = member_email
        user_instance.contact_num = member_number
        user_instance.gender = member_gender
        user_instance.crime_history = check_criminal
        user_instance.cctv = check_cctv
        user_instance.save()

        request.session['member_name'] = member_name

        context["flag"] = "0"
        context["result"] = 'Member update'

        return JsonResponse(context, content_type="application/json")

    return JsonResponse(context, content_type="application/json")


@csrf_exempt
def create_application(request):

    request_body = json.loads(request.body.decode("utf-8"))

    if request.method == 'POST':

        application_serializer = ApplicationSerializer(
            data=request_body['work_condition'])

        if work_condition_serializer.is_valid():

            work_condition_instance = work_condition_serializer.save()

            request_body['work_condition'] = work_condition_instance.id

            if request_body['post_type'] == 'parent_post':

                post_serializer = ParentPostSerializer(data=request_body)

                if post_serializer.is_valid():

                    post_instance = post_serializer.save()

                    return JsonResponse({}, content_type="application/json")

            elif request_body['post_type'] == 'sitter_post':

                post_serializer = SitterPostSerializer(data=request_body)

                if post_serializer.is_valid():

                    post_instance = post_serializer.save()

                    return JsonResponse({}, content_type="application/json")

        context["result"] = "Error!"

        return JsonResponse(context, content_type="application/json")


def forgotpassword(request):

    return render(request, 'forgotpassword.html')


@csrf_exempt
def reset_password(request):
    context = {}

    print("------------")
    # context["member_name"] = request.session['member_name']
    # context["member_type"] = request.session['member_type']

    print("------1------")

    member_email = request.GET['email']
    member_password = request.GET['password']
    member_type = request.GET['membertype']
    print("---------e----------")
    print(member_email)
    print(member_password)
    print(member_type)

    print("-------end---------")
    if member_type == "P":
        user_instance = Parent_User.objects.get(email=member_email)

        user_instance.password = member_password
        user_instance.save()

        context["flag"] = "0"
        context["result"] = 'Reset the password'
        return JsonResponse(context, content_type="application/json")

    else:
        user_instance = Sitter_User.objects.get(email=member_email)

        user_instance.password = member_password
        user_instance.save()
        context["flag"] = "0"
        context["result"] = 'Reset the password'
        return JsonResponse(context, content_type="application/json")

    return JsonResponse(context, content_type="application/json")


# 필터
