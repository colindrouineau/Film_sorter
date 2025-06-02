# Film_sorter


Film_sorter est un outil permettant de ranger un disque dur ou un répertoire et de créer une base de données "Film_sorter.db" référençant tous les films de ce disque ou répertoire.
Dans une ligne de la base de données, il y a les métadonnées du film, pour l'identification, son titre formaté, sa durée, ses pistes de langage et ses pistes de sous-titres.

Il faudra attribuer à chaque disque un numéro unique.

Il y a 3 fichiers .exe suffisant à l'utilisation complète de l'outil.

1) record_launcher.exe :
  - Parcourt le disque ;
  - Enregistre les films dans la base de données ;
  - Déplace tous les films vers la racine du disque, en formattant leur nom (formattage basique) ;
  - Supprime les doublons de films (compressés dans une Corbeille à la racine)
  - Déplace tous les répertoires et fichiers (non films) à la racine dans un fichier 'Other', lui aussi à la racine.
  - Crée dans 'Other' un fichier 'Film_sorter.txt' avec le numéro du disque et les dates d'exécution d'un programme d'enregistrement pour ce disque.

2) soft_record_launcher.exe
  - Parcourt le disque ;
  - Enregistre les films dans la base de données ;
  - Déplace tous les films vers la racine du disque, en formattant leur nom (formattage basique) ;
  - Supprime les doublons de films (compressés dans une Corbeille à la racine)
  - Déplace tous les répertoires et fichiers (non films) à la racine dans un fichier 'Other', lui aussi à la racine.
  - Crée dans 'Other' un fichier 'Film_sorter.txt' avec le numéro du disque et les dates d'exécution d'un programme d'enregistrement pour ce disque.