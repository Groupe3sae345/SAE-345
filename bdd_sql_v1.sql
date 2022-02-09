DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS type_ski;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS ski;

CREATE TABLE ski(
   id_ski INT AUTO_INCREMENT,
   type_ski_id INT,
   longueur DECIMAL(8,2),
   fabricant VARCHAR(50),
   fournisseur VARCHAR(50),
   PRIMARY KEY(id_ski)
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

INSERT INTO user (id_user, email, username, password, role, est_actif) VALUES (NULL, 'admin@admin.fr', 'admin', 'sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a', 'ROLE_admin', 1);
INSERT INTO user  (id_user, email, username, password, role, est_actif) VALUES (NULL, 'client@client.fr', 'client', 'sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4', 'ROLE_client', 1);
INSERT INTO user  (id_user, email, username, password, role, est_actif) VALUES (NULL, 'client2@client2.fr', 'client2', 'sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3', 'ROLE_client', 1);
LOAD DATA LOCAL INFILE 'type_ski.csv' INTO TABLE type_ski FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'etat.csv' INTO TABLE etat FIELDS TERMINATED BY ',';
LOAD DATA LOCAL INFILE 'ski.csv' INTO TABLE ski FIELDS TERMINATED BY ',';

SELECT * FROM user;
SELECT * FROM type_ski;
SELECT * FROM etat;
SELECT * FROM ski;
