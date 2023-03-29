Installation
==================

Prérequis
**********

.. code-block:: bash

    sudo apt update
    sudo apt upgrade


Installez et configurez `PostgreSQL <https://www.postgresql.org/>`_.

Installez Python et pip avec la commande suivante :

.. code-block:: bash

    sudo apt install python3 python3-pip

.. note::
    Voici la liste des modules Python à installer : :py:mod:`django`, :py:mod:`attrs`, :py:mod:`channels`, :py:mod:`channels_redis`, :py:mod:`daphne`, :py:mod:`django-chartjs`, :py:mod:`django-import-export`, :py:mod:`python-dotenv`, :py:mod:`docker`, :py:mod:`django-webpush`, :py:mod:`cycler`, :py:mod:`decorator`, :py:mod:`git-ext`, :py:mod:`matplotlib`, :py:mod:`networkx`, :py:mod:`numpy`, :py:mod:`olefile`, :py:mod:`Pillow`, :py:mod:`pyparsing`, :py:mod:`python-dateutil`, :py:mod:`pytz`, :py:mod:`PyWavelets`, :py:mod:`scikit-image`, :py:mod:`scipy`, :py:mod:`six`, :py:mod:`tqdm`.

Installez les modules Python nécessaires au fonctionnements du site :

.. code-block:: bash

    python3 -m pip install attrs channels channels_redis daphne django django-chartjs django-import-export python-dotenv docker django-webpush cycler decorator git-ext matplotlib networkx numpy olefile Pillow pyparsing python-dateutil pytz PyWavelets scikit-image scipy six tqdm

Lancer le docker avec la commande suivante:

.. code-block:: bash

    sudo docker run -p 6379:6379 -d redis:5

Création du projet
********************

.. code-block:: bash

    git clone https://github.com/ProjetCuisineriesM1/projet-cuisineries.git

    cd site_cuisineries
    ln -s ../static/ ./

Paramétrage
***************

Créer un fichier nommé ``.env`` contenant les données suivantes:

.. code-block:: bash

    SECRET_KEY=<VOTRE SECRET KEY>
    DB_NAME=<DB_NAME>
    DB_USER=<DB_USER>
    DB_PASS=<DB_PASS>

Vous pouvez générer votre clé secrète à partir du site `Djecrety.ir <https://djecrety.ir/>`_.

.. code-block:: bash

    python3 manage.py makemigrations
    python3 manage.py migrate

.. code-block:: bash

    python3 manage.py createsuperuser

Exécution
************

.. code-block:: bash
    
    python3 manage.py runserver

Accéder à http://localhost:8000/admin/site_cuisineries/membre et se mettre le rôle administrateur