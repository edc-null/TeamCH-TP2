<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Projet – Gestion de contacts</title>
</head>
<body>

<h1>Projet 1 – Gestion de contacts</h1>

<h2>Description</h2>
<p>
Application Python développée en <strong>programmation orientée objet (POO)</strong>
permettant la gestion complète de contacts à l’aide d’une interface graphique réalisée
avec <strong>PyQt6</strong> et d’une base de données <strong>SQLite</strong>.
</p>

<p>
L’application offre à l’utilisateur la possibilité d’ajouter, de modifier, de supprimer
et de valider des contacts comprenant un nom, un prénom, un numéro de téléphone et
une adresse courriel. Les données saisies font l’objet d’une validation rigoureuse
effectuée lors de l’enregistrement afin de garantir
l’intégrité et la cohérence des informations stockées.
</p>

<p>
La persistance des données est assurée par une base de données SQLite, manipulée
via une couche d’accès dédiée qui isole la logique SQL du reste de l’application.
</p>

<p>
Le projet intègre également une <strong>page web statique en HTML et CSS</strong>,
accessible depuis la section « Aide et à propos de » de l’interface graphique. 
</p>

<p>
<strong>Concepts utilisés :</strong><br>
Encapsulation, séparation des responsabilités, validation centralisée des données,
programmation orientée objet.
</p>

<p>
<strong>Technologies et modules utilisés :</strong><br>
PyQt6, SQLite, re (expressions régulières), HTML5, CSS3.
</p>

<hr>

<h2>Architecture et conception</h2>

<h3>AddContactWindow</h3>
<p>
Classe responsable de l’interface graphique permettant l’ajout et la modification
d’un contact.
</p>
<ul>
    <li>Affichage des champs de saisie (QLineEdit)</li>
    <li>Gestion des boutons Enregistrer / Annuler</li>
    <li>Validation des champs via la classe <code>Catch</code></li>
    <li>Mise en évidence visuelle des champs invalides</li>
    <li>Positionnement automatique du focus sur le champ en erreur</li>
</ul>

<h3>Contact</h3>
<p>
Classe métier représentant un contact.
Elle encapsule les attributs suivants :
</p>
<ul>
    <li>nom</li>
    <li>prenom</li>
    <li>telephone</li>
    <li>email</li>
</ul>

<h3>Database</h3>
<p>
Classe responsable de l’accès à la base de données SQLite.
</p>
<ul>
    <li>Ajout d’un contact</li>
    <li>Modification d’un contact existant</li>
    <li>Isolation de la logique SQL du reste de l’application</li>
</ul>

<h3>Catch (Validation des entrées)</h3>
<p>
Classe dédiée à la validation des données utilisateur.
Toutes les règles de validation sont centralisées afin de garantir
la cohérence et la maintenabilité du code.
</p>

<hr>

<h2>Validation des champs</h2>

<h3>Nom et prénom</h3>
<ul>
    <li>Obligatoires</li>
    <li>Acceptent les lettres, accents, espaces, tirets et apostrophes</li>
    <li>Exemples valides : <em>Jean-Pierre</em>, <em>O'Connor</em></li>
</ul>

<h3>Numéro de téléphone</h3>
<ul>
    <li>Obligatoire</li>
    <li>Contient uniquement chiffres, espaces, parenthèses et tirets</li>
    <li>Longueur comprise entre 7 et 20 caractères</li>
</ul>

<h3>Adresse courriel</h3>
<ul>
    <li>Obligatoire</li>
    <li>Respecte un format standard (utilisateur@domaine.extension)</li>
    <li>Accepte lettres, chiffres, points, tirets et underscores</li>
</ul>

<hr>

<h2>Fonctionnalités principales</h2>
<ul>
    <li>Ajout de contacts</li>
    <li>Modification de contacts existants</li>
    <li>Validation centralisée des données</li>
    <li>Validation en temps réel avec retour visuel</li>
    <li>Mise en évidence du champ invalide (bordure rouge)</li>
    <li>Placement automatique du curseur sur le champ en erreur</li>
    <li>Messages d’erreur explicites</li>
    <li>Persistance des données via SQLite</li>
</ul>

<hr>

<h2>Exemples d’utilisation</h2>

<h3>Menu principal</h3>
<p>
Le menu principal présente la liste des contacts et les boutons interactifs suivants :
</p>
<ul>
    <li>Ajouter</li>
    <li>Modifier</li>
    <li>Supprimer</li>
    <li>Actualiser</li>
    <li>Aide et à propos de</li>
    <li>Quitter</li>
</ul>
<img src="README images/1.png" alt="Menu" width="802" height="482">

<h3>Ajout d’un contact</h3>
<p>
L’utilisateur saisit les informations du contact.  
Si un champ est invalide :
</p>
<ul>
    <li>Le champ concerné est encadré en rouge</li>
    <li>Le focus est automatiquement placé dessus</li>
    <li>Un message d’erreur explicatif est affiché</li>
</ul>
<img src="README images/22.png" alt="" width="422" height="312">
<img src="README images/222.png" alt="" width="422" height="312">
<img src="README images/2.png" alt="" width="422" height="312">
<img src="README images/3.png" alt="" width="422" height="312">
<img src="README images/33.png" alt="" width="422" height="312">
<img src="README images/4.png" alt="" width="422" height="312">
<img src="README images/5.png" alt="" width="802" height="482">


<h3>Modification d’un contact</h3>
<p>
L'utilisateur doit sélectionner le contact à modifier. 
Ensuite, les données existantes sont préchargées dans le formulaire.
Après validation, les modifications sont enregistrées en base de données.
</p>
<img src="README images/6.png" alt="" width="802" height="482">
<img src="README images/7.png" alt="" width="422" height="312">
<img src="README images/8.png" alt="" width="422" height="312">
<img src="README images/9.png" alt="" width="422" height="312">
<img src="README images/10.png" alt="" width="422" height="312">
<img src="README images/100.png" alt="" width="802" height="482">



<h3>Suppression d’un contact</h3>
<p>
L'utilisateur doit sélectionner le contact à supprimer avant de cliquer sur le bouton.
Ensuite, les données existantes sont supprimées et les modifications sont enregistrées en base de données.
</p>
<img src="README images/23.png" alt="" width="802" height="482">
<img src="README images/24.png" alt="" width="802" height="482">
<img src="README images/25.png" alt="" width="802" height="482">



<h3>Aide et à propos de</h3>
<p>
Bouton menant à une page web rédigée en html et css. Cette page présente un l'informaiton sur l'application et sur les développeurs.
</p>
<img src="README images/26.png" alt="" width="802" height="482">
<img src="README images/27.png" alt="" width="400" height="300">
<img src="README images/28.png" alt="" width="400" height="300">
<hr>

<p>
Projet réalisé par Eric De Celles, Valérie Ouellet et William Bourbonnière dans dans le cadre du cours 420-2PR-BB Programmation orientée objet. Collège Bois-de-Boulogne 15/01/2026
</p>

</body>
</html>
