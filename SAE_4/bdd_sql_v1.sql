DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS avis;
DROP TABLE IF EXISTS ski;
DROP TABLE IF EXISTS adresse;
DROP TABLE IF EXISTS type_adresse;
DROP TABLE IF EXISTS region;
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

CREATE TABLE region(
    id_region INT AUTO_INCREMENT,
    libelle_region varchar(255),
    PRIMARY KEY(id_region)
);

CREATE TABLE type_adresse(
    id_type_adresse INT AUTO_INCREMENT,
    libelle_type_adresse varchar(255),
    PRIMARY KEY(id_type_adresse)
);

CREATE TABLE adresse(
    id_adresse INT AUTO_INCREMENT,
    libelle_adresse varchar(255),
    type_adresse_id INT,
    region varchar(255),
    user_id INT,
    PRIMARY KEY(id_adresse),
    CONSTRAINT fk_adresse_user FOREIGN KEY (user_id) REFERENCES user (id_user),
    CONSTRAINT fk_adresse_type_adresse FOREIGN KEY(type_adresse_id) REFERENCES type_adresse(id_type_adresse)
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
   CONSTRAINT fk_ski_typeSki FOREIGN KEY (type_ski_id) REFERENCES type_ski (id_type_ski),
   CONSTRAINT fk_ski_fabricant FOREIGN KEY (fabricant_id) REFERENCES fabricant (id_fabricant),
   CONSTRAINT fk_ski_fournisseur FOREIGN KEY (fournisseur_id) REFERENCES fournisseur (id_fournisseur)
);

CREATE TABLE IF NOT EXISTS avis(
    id_avis INT NOT NULL AUTO_INCREMENT,
    commentaire  varchar(500),
    note NUMERIC(2,1),
    user_id INT NOT NULL ,
    ski_id INT NOT NULL ,
    PRIMARY KEY (id_avis),
    CONSTRAINT fk_avis_user FOREIGN KEY (user_id) REFERENCES user(id_user),
    CONSTRAINT fk_avis_ski FOREIGN KEY (ski_id) REFERENCES ski(id_ski)
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
    ski_id INT,
    prix_unit DECIMAL(9,2),
    quantite INT,
    PRIMARY KEY (commande_id,ski_id),
    CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id_commande),
    CONSTRAINT fk_ligne_commande_ski FOREIGN KEY (ski_id) REFERENCES ski(id_ski)
);

CREATE TABLE panier(
    id_panier INT AUTO_INCREMENT,
    date_ajout DATE,
    user_id INT,
    ski_id INT,
    prix_unit DECIMAL(9,2),
    quantite INT,
    PRIMARY KEY (id_panier),
    CONSTRAINT fk_panier_user FOREIGN KEY (user_id) REFERENCES user(id_user),
    CONSTRAINT fk_panier_ski FOREIGN KEY (ski_id) REFERENCES ski(id_ski)
);

LOAD DATA LOCAL INFILE 'region.csv' INTO TABLE region FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'type_adresse.csv' INTO TABLE type_adresse FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'user.csv' INTO TABLE user FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'adresse.csv' INTO TABLE adresse FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'type_ski.csv' INTO TABLE type_ski FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'etat.csv' INTO TABLE etat FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'fournisseur.csv' INTO TABLE fournisseur FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'fabricant.csv' INTO TABLE fabricant FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'ski.csv' INTO TABLE ski FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'avis.csv' INTO TABLE avis FIELDS TERMINATED BY ',';

SELECT * FROM adresse;
SELECT * FROM type_adresse;
SELECT * FROM user;
SELECT * FROM type_ski;
SELECT * FROM etat;
SELECT * FROM fournisseur;
SELECT * FROM fabricant;
SELECT * FROM avis;
SELECT * FROM ski;