Admin (``admin.py``)
====================

Définition des paramètres du panneau d'administration

Les différentes classes d'administrations sont enregistrés dans le système et liées avec les classes :doc:`Models </site_cuisineries/models>` avec la ligne suivante :

.. code-block:: python

    admin.site.register(Model, ModelAdmin)

Classe ``MembreAdmin``
**********************
.. autoclass:: site_cuisineries.admin.MembreAdmin
    :members:
    :show-inheritance:

Classe ``VacationAdmin``
************************
.. autoclass:: site_cuisineries.admin.VacationAdmin
    :members:
    :show-inheritance:

Classe ``InscriptionAdmin``
***************************
.. autoclass:: site_cuisineries.admin.InscriptionAdmin
    :members:
    :show-inheritance:
    
Classe ``ReunionAdmin``
***********************
.. autoclass:: site_cuisineries.admin.ReunionAdmin
    :members:
    :show-inheritance:

Classe ``ContrepartieAdmin``
****************************
.. autoclass:: site_cuisineries.admin.ContrepartieAdmin
    :members:
    :show-inheritance:

Classe ``ChoixAdmin``
*********************
.. autoclass:: site_cuisineries.admin.ChoixAdmin
    :members:
    :show-inheritance: