# Film_sorter


Film_sorter est un outil permettant de ranger un disque dur ou un répertoire et de créer une base de données "Film_sorter.db" référençant tous les films de ce disque ou répertoire.
Dans une ligne de la base de données, il y a les métadonnées du film - pour l'identification -, son titre formaté, sa durée, ses pistes de langage et ses pistes de sous-titres.

Il faudra attribuer à chaque disque un numéro unique, et il est important de marquer physiquement le numéro du disque.

Afin que le développeur puisse suivre l'évolution de la base de données, la base de données est automatiquement uploadée sur le repo github à la fin de chaque enregistrement. Pour cela, il faut un token d'autorisation d'accès. Le token est écrit dans un fichier .txt qui s'appelle token_path.txt. Pour fonctionner, le programme doit savoir où se trouve ce fichier. Normalement il le sait par défaut. Mais en cas de problème, c'est possible qu'il vous le demande, auquel cas il faudra entrer le chemin complet.
Il en est de même pour le chemin vers la base de données.

Quand vous lancerez le fichier .exe, un terminal s'ouvre dans lequel vous pouvez entrer les informations nécessaires et consulter les résultats de votre recherhce. Si vous allez au bout du programme, il suffit d'appuyer sur entrée pour quitter le programme. Si vous voulez le quittez en cours de route, appuyez sur Ctrl + c.

Le programme est intrusif, c'est à dire qu'il modifie le contenu du disque en le réorganisant. Normalement, l'intervention est minimale - surtout pour soft_record_launcher -, et le risque de suppression de fichier, ou de changement irréversible, est nul. Néanmoins, il est recommandé de tester d'abord le code sur des disques ou répertoires à faible enjeu, et de vérifier que tout se passe bien.

L'outil a été codé de manière à gérer correctement toutes les exceptions potentielles, mais il est possible que certaines aient été oubliées. En cas de problème ou de question sur le fonctionnement de l'outil, merci de contacter le développeur à l'addresse mail suivante : colin.drouineau@gmail.com.


Il y a 3 fichiers .exe suffisants à l'utilisation complète de l'outil. Ils sont sont situés dans le dossier situé à \Film_sorter_exes\dist

1) record_launcher.exe :
  - Parcourt le disque ;
  - Enregistre les films dans la base de données ;
  - Déplace tous les films vers la racine du disque, en formattant leur nom (formatage basique) ;
  - Supprime les doublons de films (déplacés vers une "Corbeille" à la racine) ;
  - Déplace tous les répertoires et fichiers (non films) à la racine dans un fichier 'Other', lui aussi à la racine ;
  - Crée ou updates dans 'Other' un fichier 'Film_sorter.txt' avec le numéro du disque et les dates d'exécution d'un programme d'enregistrement pour ce disque.

2) soft_record_launcher.exe
  - Parcourt le disque ;
  - Enregistre les films dans la base de données ;
  - Déplace tous les films vers un répertoire "Film_sorter_films" à la racine du disque, en formatant leur nom (formatage basique) ;
  - Supprime les doublons de films (déplacés vers une "Corbeille" à la racine) ;
  - Crée ou updates dans 'Other' un fichier 'Film_sorter.txt' avec le numéro du disque et les dates d'exécution d'un programme d'enregistrement pour ce disque.

3) research_launcher.exe
  - Vous demande le titre du film que vous cherchez, et/ou la fourchette de durées qui vous intéresse ;
  - Parcourt les films et affiche dans le terminal ceux qui correspondent le plus à votre recherche ;
  - Le classement est fait en fonction de la distance entre le titre entré et le titre du film ;
  - Dans le terminal sont affichés : le titre du film, la durée du film, les pistes de langage, les pistes de sous-titres.

Dans ce même dossier, avec le même nom mais avec l'extension .bat, on peut lancer ces programmes dans un mode qui permet de voir le message d'erreur s'il en est : la console ne se ferme pas automatiquement.


Nous espérons que vous aurez une bonne expérience avec Film_sorter !