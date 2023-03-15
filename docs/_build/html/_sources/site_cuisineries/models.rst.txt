Models (``models.py``)
======================

Définition des différentes classes/tables du projet

Classe ``Membre``
*****************
.. autoclass:: site_cuisineries.models.Membre
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``Competence``
*********************
.. autoclass:: site_cuisineries.models.Competence
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``Attente``
******************
.. autoclass:: site_cuisineries.models.Attente
    :members: __str__
    :undoc-members:
    :show-inheritance:
    
Classe ``Vacation``
*******************
.. autoclass:: site_cuisineries.models.Vacation
    :members: __str__, nb_inscrits, complet, places_dispo, credits, heures, inscrits
    :undoc-members:
    :show-inheritance:

Classe ``Contrepartie``
***********************
.. autoclass:: site_cuisineries.models.Contrepartie
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``Reunion``
******************
.. autoclass:: site_cuisineries.models.Reunion
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``Inscription``
**********************
.. autoclass:: site_cuisineries.models.Inscription
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``Choix``
****************
.. autoclass:: site_cuisineries.models.Choix
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``Conversation``
***********************
.. autoclass:: site_cuisineries.models.Conversation
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``Message``
******************
.. autoclass:: site_cuisineries.models.Message
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``MessageGroup``
***********************
.. autoclass:: site_cuisineries.models.MessageGroup
    :members: __str__
    :undoc-members:
    :show-inheritance:

Classe ``ConversationRead1o1``
******************************
.. autoclass:: site_cuisineries.models.ConversationRead1o1
    :members: is_new_message, nb_not_read
    :undoc-members:
    :show-inheritance:

Classe ``ConversationReadGroup``
********************************
.. autoclass:: site_cuisineries.models.ConversationReadGroup
    :members: is_new_message, nb_not_read
    :undoc-members:
    :show-inheritance: