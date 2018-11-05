# tucad
TU Computer-Aided Diagnosis for Chest X-Ray and Fundus Photography + OCT (Optical Coherence Tomography)

------
## Installation ##
### [Windows](https://docs.djangoproject.com/en/2.1/howto/windows/) ###
`virtualenv` and `virtualenvwrapper` provide a dedicated environment for each Django project you create. Install by typing
```
pip install virtualenvwrapper-win
```
Then create a virtual environment for your project:
```
mkvirtualenv myproject
```
If you start a new command prompt, you will need to activate the environment again using:
```
workon myproject
```

### Linux (Tested on [Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-django-and-set-up-a-development-environment-on-ubuntu-16-04)) ###
To install `virtualenv`, we will use the `pip3` command, as shown below:
```
pip3 install virtualenv
virtualenv --version
```
While inside the `django-apps` directory, create your virtual environment. Let call it env.
```
virtualenv env
```
Activate the virtual environment with the following command:
```
. env/bin/activate
```

### Dependencies ###
- Django 2.1
- PyTorch 0.2.0

To install dependency, type:
```
pip install django
conda install pytorch=0.2.0 cuda80 -c pytorch
pip install torchvision==0.1.9
conda install -c conda-forge scikit-image
pip install scikit-image seaborn
pip install sklearn
```


------
### Run ###
Change into the outer project directory, and run `makemigrations` to tell Django that you've made some changes to your models and that you'd like the changes to be stored as a migration.
```Python
python manage.py makemigrations
```
`migrate` command that will run the migrations for you and manage your database schema automatically.
```Python
python manage.py migrate
```
Run the following commands to start the server
```Python
python manage.py runserver
```

------
### Requirements ###
Test on Django 2.1 Python 3.6

------
### Dockerize ###
Follow this [tutorial](https://medium.com/backticks-tildes/how-to-dockerize-a-django-application-a42df0cb0a99)
Use the given `requirements.txt` or create one by typing
```
pip freeze > requirements.txt
```
To list all the libraries in the environment.

Next, install `Docker compose` following this [link](https://docs.docker.com/compose/install/#install-compose)
Then, build and run the container with the command:
```
docker-compose up
```
If there is any error and you need to build the docker image again, type:
```
docker build -t tucad_web .
```
Finally, the web app for development should start at http://0.0.0.0:8000/


