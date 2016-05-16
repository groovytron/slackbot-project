Zerabot
=======

Idée de base du projet
----------------------

Le but du projet est de réaliser un Slackbot que l'utilisateur
peut interroger le site Twitch pour savoir si un streamer est en ligne.
L'utilisateur pourrait interroger le bot avec une commande comme
`isOnline? Zerator` et le bot lui répondrait simplement par
`yes` ou `no`.

Pour aller plus loin, il faudrait que le bot annonce aux utilisateurs
lors qu'un streamer (liste de veille) est en ligne avec un message
comme `Zerator is online !` avec éventuelle un lien, une image, le
jeu auquel il joue, etc.

Déroulement du développement
----------------------------

1. Questionner le bot et obtenir la réponse pour savoir si le streamer est en ligne.

2. Script console Python signalant que tel ou tel streamer commence à streamer par un simple print.

3. Intégration du script dans le bot.

4. Ajout d'un streamer à la liste de veille.

Premiers problèmes
------------------

- Veille et réponse aux requêtes en asynchrone.
