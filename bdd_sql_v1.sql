DROP TABLE IF EXISTS Ski;
DROP TABLE IF EXISTS Type_ski;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS etat;

CREATE TABLE ski(
   id_ski INT AUTO_INCREMENT,
   type_ski_id INT,
   longueur DECIMAL(8,2),
   modele VARCHAR(50),
   fabricant VARCHAR(50),
   fournisseur VARCHAR(50),
   PRIMARY KEY(id_ski)
);

CREATE TABLE type_ski(
   id_type_ski INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_type_ski)
);

CREATE TABLE user(
    id_user INT AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50),
    est_actif tinyint(1),
    pseudo VARCHAR(50),
    email VARCHAR(50),
    PRIMARY KEY(id_user)
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
    CONSTRAINT fk_panier_user FOREIGN KEY (user_id) REFERENCES user (id_panier),
    CONSTRAINT fk_panier_article FOREIGN KEY (article_id) REFERENCES Ski(id_ski)
);

CREATE TABLE etat(
    id_etat INT AUTO_INCREMENT,
    libelle VARCHAR(50),
    PRIMARY KEY (id_etat)
);

LOAD DATA LOCAL INFILE 'type_ski.csv' INTO TABLE type_ski FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'etat.csv' INTO TABLE etat FIELDS TERMINATED BY ',';
