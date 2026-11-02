# Heterogeneous Co-Evolution Learning for Tool-Efficient Search Agents with Zero Labels

L’article étudie les agents de recherche qui alternent raisonnement et consultation de documents externes pour répondre à des questions.
Leur difficulté consiste à déterminer quelles informations chercher, quand lancer une recherche et quand s’arrêter.
Un entraînement fondé sur des questions fixes peut devenir insuffisant à mesure que l’agent progresse.
Récompenser seulement la réponse finale favorise aussi des trajectoires correctes mais encombrées de recherches inutiles.
ZEST-Search propose donc de faire évoluer ensemble les questions d’entraînement et la manière d’utiliser les outils.

Le système repose sur deux rôles : un générateur de tâches et un agent chargé de les résoudre.
Ces rôles peuvent être confiés à des modèles de tailles ou de familles différentes, d’où la notion de coévolution hétérogène.
Un petit modèle peut ainsi produire des exercices utiles à un modèle plus grand, sans reproduire exactement ses connaissances.
L’entraînement commence avec des questions de référence dépourvues de leurs réponses annotées, issues de Natural Questions.
« Sans labels » concerne cette phase : les modèles préentraînés, les documents et les questions existantes restent indispensables.

La génération fonctionne à rebours, en choisissant une réponse cible avant de formuler une nouvelle question.
Le générateur identifie une catégorie pertinente dans la question de référence, puis propose une entité concrète de cette catégorie.
Il ne cherche donc pas nécessairement à répondre à la question initiale, qui sert plutôt de point de départ sémantique.
Une vérification légère contrôle le format de l’entité et sa présence dans les résultats de recherche.
Les candidats retenus deviennent des réponses connues pour construire automatiquement de nouveaux exercices.

Le système explore ensuite des documents pour relier cette entité à d’autres entités mentionnées dans des phrases sources.
Il organise ces associations en chemins de preuves pouvant nécessiter plusieurs étapes de recherche.
Un exemple relie un film à son réalisateur, puis à sa ville d’origine et à son contexte géographique.
Le générateur transforme ce chemin en question, en conservant les indices relationnels sans dévoiler directement la réponse.
La validation et la construction des chemins utilisent recherche documentaire et règles linguistiques, sans appel supplémentaire à un modèle juge.

Les questions acceptées alimentent un réservoir réutilisable, ce qui permet d’élargir progressivement les tâches proposées.
Le générateur reçoit une récompense calculée à partir du taux de réussite actuel de l’agent sur chaque question.
Cette récompense est maximale lorsque l’agent réussit environ une tentative sur deux, et nulle s’il réussit ou échoue systématiquement.
L’objectif est de produire des difficultés accessibles mais stimulantes, plutôt que des exercices triviaux ou systématiquement impossibles.
Les questions invalides sont pénalisées afin de limiter les tâches mal formées et les signaux d’apprentissage peu utiles.

Pour chaque exercice, l’agent produit cinq trajectoires, avec au maximum trois recherches et trois passages récupérés par recherche.
Sa réponse finale est évaluée par correspondance exacte normalisée avec l’entité cible.
Sa récompense combine cette exactitude et une pénalisation du nombre de recherches, normalisée entre les trajectoires d’une même question.
L’économie d’outils ne rapporte ainsi aucun avantage à une réponse incorrecte ; entre réponses correctes, les trajectoires plus courtes sont favorisées.
Le générateur et l’agent sont mis à jour par apprentissage par renforcement, pour adapter simultanément difficulté et comportement de recherche.

L’évaluation porte sur sept jeux de questions : NQ, TriviaQA, PopQA, HotpotQA, 2Wiki, MuSiQue et Bamboogle.
Elle mesure la moyenne des scores d’exactitude et le nombre moyen d’actions de recherche correctement interprétées.
Avec un générateur Qwen2.5-7B-Instruct et un agent Qwen2.5-7B-Base, le score moyen passe de 21,8 % à 38,2 %.
Ce gain de 16,4 points s’accompagne d’une diminution des recherches moyennes de 1,59 à 1,16, soit environ 27 %.
Les expériences montrent aussi des progrès avec des générateurs plus petits, des familles différentes et des agents déjà spécialisés dans la recherche.

La baisse du nombre de recherches n’est cependant pas universelle : l’agent de base à trois milliards de paramètres en utilise davantage après entraînement.
Son exactitude progresse fortement, ce qui illustre qu’un agent initialement trop peu utilisateur d’outils peut devoir chercher davantage.
Les ablations montrent qu’une pénalité modérée réduit les recherches avec une faible perte d’exactitude par rapport à l’entraînement sans pénalité.
Une pénalité excessive dégrade davantage les réponses : l’objectif est un compromis contrôlé, pas la suppression systématique de la recherche.
La coévolution améliore également la génération de questions par rapport à un générateur maintenu figé.

Les annexes apportent une limite importante : la validation est surtout structurelle et lexicale, sans vérification complète du sens.
Un chemin accepté ne garantit donc ni la vérité de toutes les relations, ni l’unicité de la réponse, ni la nécessité réelle de plusieurs recherches.
Des contextes de repli non certifiés peuvent être conservés, ce qui impose de distinguer disponibilité des preuves et certification effective.
Les expériences utilisent un corpus Wikipédia de 2018 et des réponses principalement centrées sur des entités, loin de toute la diversité du Web actuel.
Les comparaisons avec certains travaux concurrents ne sont pas entièrement contrôlées, car les modèles, sources et budgets de recherche diffèrent.

Le protocole décrit mobilise seize GPU A100 et six cents étapes d’entraînement : réduire les annotations ne rend pas l’apprentissage gratuit.
Le nombre d’appels aux outils ne mesure pas à lui seul le coût total, la latence ou la consommation de calcul.
La validation économique des exercices constitue un choix pratique, mais laisse subsister un risque de supervision synthétique imparfaite.
L’intérêt de ZEST-Search tient à l’articulation de trois leviers : génération guidée par les sources, difficulté adaptative et récompense attentive aux outils.
L’article montre ainsi comment améliorer conjointement les capacités d’un agent de recherche et son usage des outils, dans les conditions expérimentales étudiées.
