DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS ski;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS type_ski;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXiSTS fournisseur;
DROP TABLE IF EXISTS fabricant;

CREATE TABLE fabricant(
    id_fabricant INT AUTO_INCREMENT,
    nom_fabricant VARCHAR(50),
    PRIMARY KEY (id_fabricant)
);

CREATE TABLE fournisseur(
    id_fournisseur INT AUTO_INCREMENT,
    nom_fournisseur VARCHAR(50),
    PRIMARY KEY (id_fournisseur)
);

CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(50),
    PRIMARY KEY (id_etat)
);

CREATE TABLE type_ski(
   id_type_ski INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_type_ski)
);

CREATE TABLE user(
    id_user INT AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(255),
    role VARCHAR(50),
    est_actif tinyint(1),
    email VARCHAR(50),
    PRIMARY KEY(id_user)
);

CREATE TABLE ski(
   id_ski INT AUTO_INCREMENT,
   type_ski_id INT,
   longueur DECIMAL(8,2),
   prix_ski DECIMAL(9,2),
   stock INT,
   image VARCHAR(50),
   fabricant_id INT,
   fournisseur_id INT,
   PRIMARY KEY(id_ski),
   CONSTRAINT fk_ski_fabricant FOREIGN KEY (fabricant_id) REFERENCES fabricant (id_fabricant),
   CONSTRAINT fk_ski_fournisseur FOREIGN KEY (fournisseur_id) REFERENCES fournisseur (id_fournisseur)
);

CREATE TABLE commande(
    id_commande INT AUTO_INCREMENT,
    user_id INT,
    etat_id INT,
    date_achat DATE,
    PRIMARY KEY (id_commande),
    CONSTRAINT fk_commande_user FOREIGN KEY (user_id) REFERENCES user (id_user),
    CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat(id_etat)
);

CREATE TABLE ligne_commande(
    commande_id INT,
    article_id INT,
    prix_unit DECIMAL(9,2),
    quantite INT,
    PRIMARY KEY (commande_id,article_id),
    CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    CONSTRAINT fk_ligne_commande_article FOREIGN KEY (article_id) REFERENCES Ski(id_ski)
);

CREATE TABLE panier(
    id_panier INT AUTO_INCREMENT,
    date_ajout DATETIME,
    user_id INT,
    article_id INT,
    prix_unit DECIMAL(9,2),
    quantite INT,
    PRIMARY KEY (id_panier),
    CONSTRAINT fk_panier_user FOREIGN KEY (user_id) REFERENCES user(id_user),
    CONSTRAINT fk_panier_article FOREIGN KEY (article_id) REFERENCES Ski(id_ski)
);

LOAD DATA LOCAL INFILE 'user.csv' INTO TABLE user FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'type_ski.csv' INTO TABLE type_ski FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'etat.csv' INTO TABLE etat FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'fournisseur.csv' INTO TABLE fournisseur FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'fabricant.csv' INTO TABLE fabricant FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'ski.csv' INTO TABLE ski FIELDS TERMINATED BY ',';

SELECT * FROM user;
SELECT * FROM type_ski;
SELECT * FROM etat;
SELECT * FROM fournisseur;
SELECT * FROM fabricant;
SELECT * FROM ski;
