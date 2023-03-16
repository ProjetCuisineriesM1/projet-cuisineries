URLs (``urls.py``)
==================

Lien entre l'url entrée et les fonctions du :doc:`views.py </chat/views>`

.. code-block:: python

    urlpatterns = [
        path("", views.index, name="index"),
        path("<str:room_name>/", views.room, name="room"),
        path("group/<str:room_name>/", views.roomGroupe, name="room"),
        path("join/<int:room_name>/", views.join, name="join"),
    ]