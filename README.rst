Zerabot
=======

Idée de base du projet
----------------------

Le but du projet est de réaliser un Slackbot que l'utilisateur
peut interroger l'application Twitch pour savoir si un streamer est en ligne.
L'utilisateur pourrait interroger le bot avec une commande comme
`@nomDuBot: streams toto` et le bot lui répondrait simplement par
`yes` ou `no` dépendant si toto est en train de streamer un vidéo.

Objectif secondaire
-------------------

Pour aller plus loin, il faudrait que le bot annonce aux utilisateurs
lors qu'un streamer est en ligne avec un message comme `Zerator is online !`
avec éventuellement un lien, une image, le jeu auquel il joue, etc.

La liste de veille des utilisateurs pourrait être une liste dans un fichier
JSON que l'on parse et stocke dans un ditcionnaire au démarrage du bot.

Déroulement du développement
----------------------------

Cette section liste les étape prévues pour le développement du bot.

1. Script console Python signalant que tel ou tel streamer commence à streamer par un simple print.

2. Questionner le bot et obtenir la réponse pour savoir si le streamer est en ligne.

3. Intégration du script dans le bot.

4. Veille permanante au démarrage du bot

5. Ajout d'un streamer à la liste de veille.

Problèmes potentiels
------------------

Voici les problèmes que nous avons confrontés.

- Requêtes sur l'API Twitch en asynchrone

- Traitement des messages (parsage, filtrage pour éviter les boucles infinies)

- Aide utilisateur

- Veille sur l'API Twitch

Etat actuel du bot et utilisation
---------------------------------

Une fois le bot installé, il est possible de le lancer avec la commande
"zerabot" depuis la ligne de commande.

Le bot fournit peut répondre à la commande "@monBot: streams" toto et fournit une
aide avec la commande "@monBot: help".

Configuration
-------------

Il faut placer un fichier de configuration config.py dans le dossier zerabot
du projet pour que le bo soit utilisable. En voici un exemple:

.. code:: python

  """ Configuration file containing bot configuration like token """

  TOKEN="xxxx-123456789-XXXXXXXXXXXXXXXXXX"
