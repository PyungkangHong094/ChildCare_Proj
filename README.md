# I.Helpr_Child Care Service

Ji Won Choi – Project manager

Sujeong Youn – Lead programmer

Pyungkang Hong – Designer, Product owner

In this day and age, the number of double-income families is increasing, and many parents are seeking childcare services. Parents want a guardian whom they can trust. So, they either ask around to find within the circle of people that they know or find one through agencies. However, these methods require unnecessary time and effort if the preferences between the guardian and parents are not met. To alleviate all this problem, we are proposing a web app that can provide:

- Parents can choose an employee from a bigger pool of people with few mouse clicks :
 Parents will be able to post a job opening with the conditions stated, then employees seeking a job will apply for the job. Among the list of applications, parents can decide whom they want to hire and send a message through messenger to decide when to start the work and talk about the work details.
- Grading system and review will ensure the credibility of the employee :
   Parents will be able to rate the guardians and leave a review of the work that they did after their work is done. Thus, other parents can refer to the reviews and rating before they decide.

# How to build the project 
IDE : visual studio code
OS: Windows 10

For all these instructions, all team members are using Windows so we intend to work on Windows. However, we have included some comments for mac/linux users. 
To check out the list of outstanding bugs and report a bug, users will use GitHub issues. 

There are two ways to build and test the software. 
After installing Django(Step 1 ~ Step 2) in the virtual environment, you can just pull the code from GitHub and then run. 
You can follow all the steps (Step 1 ~ 4)

Every command will be written in vscode terminal. 
## 1. Set up virtual environment
Enter the command below at the desired location, directory will be created with the name you entered.
python -m venv _______ (your virtual environment directory name, ex. myvenv)  
# ![cse1](https://user-images.githubusercontent.com/53274042/97192628-6e498f00-17eb-11eb-9425-faed3489fa4b.PNG)

## 2. Run the virtual environment and install the Django.
    1) To run the virtual environment, enter the following command.
                - For mac/linux: source myvenv/bin/activate 
                - For windows: source myvenv/Scripts/activate
                  (If you got an error message with ‘source’, check whether your terminal is opened as ‘PowerShell’ and change it to Cmd or Git Bash. (Ctrl + Shift + P -> type Command Prompt or Git Bash). If it still does not work, try “myvenv\Scripts\activate” )
  
# ![2](https://user-images.githubusercontent.com/53274042/97192645-71dd1600-17eb-11eb-8612-7779f4df55e5.PNG)

(All the work should be done in the virtual environment: (myvenv))  
# ![3](https://user-images.githubusercontent.com/53274042/97192661-76093380-17eb-11eb-8194-47c3354ecaeb.PNG)


https://tutorial.djangogirls.org/ko/django_start_project/, https://itinerant.tistory.com/63 ]

    2) pip install Django==3.1.2
    
# ![4](https://user-images.githubusercontent.com/53274042/97192665-76a1ca00-17eb-11eb-9242-d1c878ce94a5.PNG)

## 3. Move to your project folder and run a server 
     1) Move to your project and enter ‘django-admin startproject (Project name ex. Ihelpr)’
     Then a new directory that you named is created and inside there will be files below will be created

# ![5](https://user-images.githubusercontent.com/53274042/97192669-773a6080-17eb-11eb-96d2-1103643fda66.PNG)

Reference link: 
https://ssungkang.tistory.com/entry/Django-02-Django-%EC%8B%9C%EC%9E%91-Hello-World-%EC%B6%9C%EB%A0%A5?category=320582

    2) To run a server, 
    enter ‘python (directories/ if you are not in where manage.py is) manage.py runserver’  
  # ![6](https://user-images.githubusercontent.com/53274042/97196595-ffbb0000-17ef-11eb-9d48-85fd068e8d5e.PNG)


    3) Entering http://127.0.0.1:8000/ link to your browser will show below screen  
  # ![7](https://user-images.githubusercontent.com/53274042/97196599-00ec2d00-17f0-11eb-95f4-d0cff64ca4b2.PNG)


    4) You can turn off the server through ctrl + c (but we will keep the server on throughout this process)

## 4. Creating an app and connect it to the server you have built 

     1) As for this app, create an app using the command below.
     python manage.py startapp (name of this app ex. Ihelprapp)
     This command will create a directory that says Ihelprapp and you will be able to see different python files inside.
# ![8](https://user-images.githubusercontent.com/53274042/97196603-00ec2d00-17f0-11eb-9f8a-06a1eaf37e6a.PNG)


     2) And then, you have to connect the app with the project.
    Go to settings.py of your project directory and add your app under Installed_spps.
# ![9](https://user-images.githubusercontent.com/53274042/97196606-0184c380-17f0-11eb-9684-f26105da90b0.PNG)


    3) Add Templates (HTML files) and displaying pages
    Create a directory called ‘templates’ within your app folder.
    And place your html files inside that folder. 
# ![10](https://user-images.githubusercontent.com/53274042/97196607-0184c380-17f0-11eb-8778-0175bc4b32e9.PNG)
    4) Add urlpatterns in url.py
    Add ‘from django.conf.urls import url’ and ‘import Ihelprapp.views’ 
    Add all the urls in ‘urlpatterns’ as below format
# ![11](https://user-images.githubusercontent.com/53274042/97196608-021d5a00-17f0-11eb-9da0-af0702f86651.PNG)
    5) Create views in views.py 
    Add all the html views as below format
# ![12](https://user-images.githubusercontent.com/53274042/97196609-021d5a00-17f0-11eb-912d-365a89868ab2.PNG)
    6) To apply CSS on html files in Django
    In settings.py, add below code
# ![13](https://user-images.githubusercontent.com/53274042/97196610-02b5f080-17f0-11eb-8185-479af7114772.PNG)
    And create a static directory within the app folder. 
    (Personally I added a directory called css and added my css there for other static files that will be added later in the project.)
 # ![14](https://user-images.githubusercontent.com/53274042/97196618-05184a80-17f0-11eb-8806-50f5eac5ab08.PNG)
    7) Then change the link to css in each html like below
 # ![15](https://user-images.githubusercontent.com/53274042/97196620-05184a80-17f0-11eb-9b58-eeb7d2358245.PNG)
   
    Also, you have to 'Import os' at the top
   
    To add an image in the page, use the following code.

Reference link:  https://docs.djangoproject.com/en/3.1/howto/static-files/ 


## 5. Test 
You can check to see if the URLs of the pages are correctly connected by refreshing the page through the link of the server you hosted. (http://127.0.0.1:8000/)
# ![16](https://user-images.githubusercontent.com/53274042/97196622-05b0e100-17f0-11eb-82f4-559f0322a3fb.PNG)


## 6. How to Deploy
### 1) Download and Install Heroku CLI
- Windows 
Get the installer file from the link below:
https://devcenter.heroku.com/articles/getting-started-with-python#set-up

- macOS
```shell
$ brew install heroku/brew/heroku
```

- Linux
```shell
 $ sudo snap install heroku --classic
```

### 2) Login to heroku

```shell
$ heroku login
heroku: Press any key to open up the browser to login or q to exit
Warning: If browser does not open, visit
https://cli-auth.heroku.com/auth/browser/***
heroku: Waiting for login...
Logging in... done
Logged in as me@example.com
```

### 3) Prepare the app

```shell
$ git clone https://github.com/jiwonchoi2/Child-Care-Service.git
```

### 4) Deploy to Heroku
                
```shell
$ heroku create ihelprapp
Creating app... done, ⬢ ihelprapp
https://ihelprapp.herokuapp.com/ | https://git.heroku.com/ihelprapp.git
```
The app name on heroku is created randomly. This can be changed on the Heroku website. 
        
Now, to deploy our website, we have to push our project code on to the git link https://git.heroku.com/ihelprapp.git
        
```git
$ git add .
$ git commit -m "Initial commit" 
$ git push heroku master
```

Executing above commands will deploy our project. However, this isn't the end of our deployment process!

### 5) Migrating our data
        
```shell
$ heroku run python manage.py migrate
```

This is the end of deploying process! The result can seen by entering the link "https://ihelprapp.herokuapp.com/"


