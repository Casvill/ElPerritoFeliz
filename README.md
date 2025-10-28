
Para Ejecutar el proyecto localmente: 


python manage.py runserver

El cual montara el servicio django y permitirá visualizar el sitio web en 

http://127.0.0.1:8000/

Para acceder al panel administrativo:
ejecutar

python manage.py createsuperuser

diligenciar:
Username:
Password: 
Password (again): 
 
 Si se siguieron correctamente los pasos la consola mostrará:
 
Superuser created successfully.

ahora accedemos al panel administrativo en:

http://127.0.0.1:8000/admin/


Arbol de archivos:

SRC:.
│   .env
│   .gitignore
│   ElPerritoFeliz.md
│   manage.py
│   requirements.txt
│   
├───api
│   │   urls.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           urls.cpython-312.pyc
│           __init__.cpython-312.pyc
│           
├───attendance
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_alter_condicionfisica_options_and_more.py
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           0001_initial.cpython-312.pyc
│   │           0002_alter_condicionfisica_options_and_more.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │           
│   └───__pycache__
│           admin.cpython-312.pyc
│           apps.cpython-312.pyc
│           models.cpython-312.pyc
│           __init__.cpython-312.pyc
│           
├───canines
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           0001_initial.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │           
│   └───__pycache__
│           admin.cpython-312.pyc
│           apps.cpython-312.pyc
│           models.cpython-312.pyc
│           tests.cpython-312.pyc
│           __init__.cpython-312.pyc
│           
├───clients
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           __init__.cpython-312.pyc
│   │           
│   └───__pycache__
│           admin.cpython-312.pyc
│           apps.cpython-312.pyc
│           models.cpython-312.pyc
│           tests.cpython-312.pyc
│           __init__.cpython-312.pyc
│           
├───dashboard
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   tests.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           __init__.cpython-312.pyc
│   │           
│   └───__pycache__
│           admin.cpython-312.pyc
│           apps.cpython-312.pyc
│           models.cpython-312.pyc
│           __init__.cpython-312.pyc
│           
├───ElPerritoFeliz
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   views.py
│   │   wsgi.py
│   │   __init__.py
│   │   
│   └───__pycache__
│           settings.cpython-312.pyc
│           urls.cpython-312.pyc
│           views.cpython-312.pyc
│           wsgi.cpython-312.pyc
│           __init__.cpython-312.pyc
│           
├───enrollments
│   │   admin.py
│   │   apps.py
│   │   models.py
│   │   serializers.py
│   │   tests.py
│   │   views.py
│   │   __init__.py
│   │   
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   0002_matricula_canino.py
│   │   │   0003_rename_canino_matricula_id_canino.py
│   │   │   __init__.py
│   │   │   
│   │   └───__pycache__
│   │           0001_initial.cpython-312.pyc
│   │           0002_matricula_canino.cpython-312.pyc
│   │           0003_rename_canino_matricula_id_canino.cpython-312.pyc
│   │           __init__.cpython-312.pyc
│   │           
│   └───__pycache__
│           admin.cpython-312.pyc
│           apps.cpython-312.pyc
│           models.cpython-312.pyc
│           __init__.cpython-312.pyc
└───users
    │   admin.py
    │   apps.py
    │   models.py
    │   serializers.py
    │   tests.py
    │   urls.py
    │   __init__.py
    │   
    ├───views
    │   │   login_views.py
    │   │   register_views.py
    │   │   
    │   └───__pycache__
    │           login_views.cpython-312.pyc
    │           register_views.cpython-312.pyc
    │           
    └───__pycache__
            admin.cpython-312.pyc
            apps.cpython-312.pyc
            models.cpython-312.pyc
            serializers.cpython-312.pyc
            urls.cpython-312.pyc
            __init__.cpython-312.pyc
