DROP TABLE IF EXISTS Ski;
DROP TABLE IF EXISTS Type_ski;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS panier;
DROP TABLE IF EXISTS etat;

CREATE TABLE Ski(
   id_ski INT AUTO_INCREMENT,
   type_ski_id INT,
   Longueur DECIMAL(8,2),
   Modele VARCHAR(50),
   Fabricant VARCHAR(50),
   Fournisseur VARCHAR(50),
   PRIMARY KEY(id_ski)
);

CREATE TABLE Type_ski(
   id_type_ski INT AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(id_type_ski)
);

CREATE TABLE user(
    id INT AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(50),
    est_actif tinyint(1),
    pseudo VARCHAR(50),
    email VARCHAR(50),
    PRIMARY KEY(id)
);

CREATE TABLE commande(
    id INT AUTO_INCREMENT,
    user_id INT,
    etat_id INT,
    date_achat DATE,
    PRIMARY KEY (id),
    CONSTRAINT fk_commande_user FOREIGN KEY (user_id) REFERENCES user (id),
    CONSTRAINT fk_commande_etat FOREIGN KEY (etat_id) REFERENCES etat(id)
);

CREATE TABLE ligne_commande(
    commande_id INT,
    article_id INT,
    prix_unit DECIMAL(9,2),
    quantite INT,
    PRIMARY KEY (commande_id,article_id),
    CONSTRAINT fk_ligne_commande_commande FOREIGN KEY (commande_id) REFERENCES commande(id),
    CONSTRAINT fk_ligne_commande_article FOREIGN KEY (article_id) REFERENCES Ski(id_ski)
);

CREATE TABLE panier(
    id INT AUTO_INCREMENT,
    date_ajout DATETIME,
    user_id INT,
    article_id INT,
    prix_unit DECIMAL(9,2),
    quantite INT,
    PRIMARY KEY (id),
    CONSTRAINT fk_panier_user FOREIGN KEY (user_id) REFERENCES user (id),
    CONSTRAINT fk_panier_article FOREIGN KEY (article_id) REFERENCES Ski(id_ski)

)

CREATE TABLE etat(
    id INT AUTO_INCREMENT,
    libelle VARCHAR(50),
    PRIMARY KEY (id)
)
