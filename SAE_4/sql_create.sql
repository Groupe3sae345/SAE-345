INSERT INTO fabricant VALUES
(1,'Rossignol'),
(2,'Head'),
(3,'Fischer'),
(4,'Salomon'),
(5,'Dynastar'),
(6,'Rabbit');

INSERT INTO fournisseur VALUES
(1,'Europages'),
(2,'Glisshop'),
(3,'Kompass'),
(4,'Montaz'),
(5,'Precisionski'),
(6,'Destokplus');

INSERT INTO etat VALUES
(1, 'en attente'),
(2, 'expédié');

INSERT INTO type_ski VALUES
(1,'Mini ski'),
(2,'Ski polyvalent'),
(3,'Ski freeride'),
(4,'Ski freestyle'),
(5,'Ski de randonnée'),
(6,'Ski de piste'),
(7,'Ski alpin'),
(8,'Ski de fond'),
(9,'Snowboard');

INSERT INTO type_adresse VALUES
(1,'Expédition'),
(2,'Livraison');

INSERT INTO user VALUES
(1,'admin','sha256$pBGlZy6UukyHBFDH$2f089c1d26f2741b68c9218a68bfe2e25dbb069c27868a027dad03bcb3d7f69a','ROLE_admin',1,'admin@admin.fr',1),
(2,'client','sha256$Q1HFT4TKRqnMhlTj$cf3c84ea646430c98d4877769c7c5d2cce1edd10c7eccd2c1f9d6114b74b81c4','ROLE_client',1,'client@client.fr',2),
(3,'client2','sha256$ayiON3nJITfetaS8$0e039802d6fac2222e264f5a1e2b94b347501d040d71cfa4264cad6067cf5cf3','ROLE_client',1,'client2@client2.fr',2);

INSERT INTO region VALUES
(1,'Auvergne-Rhône-Alpes'),
(2,'Bourgogne Franche-Comté'),
(3,'Bretagne'),
(4,'Centre-Val-de-Loire'),
(5,'Corse'),
(6,'Grand-Est'),
(7,'Hauts-de-France'),
(8,'Île-de-France'),
(9,'Normandie'),
(10,'Nouvelle-Aquitaine'),
(11,'Occitanie'),
(12,'Pays-de-la-Loire'),
(13,'Provence-Alpes-Côte-D-Azur');

INSERT INTO adresse VALUES
(1,'4 avenue Jean Jaures 90000 Belfort',1,2,1),
(2,'13 Rue Saint-Bernard 31000 Toulouse',2,11,2),
(3,'63 Rue Thénard 68200 Mulhouse',2,6,3);

INSERT INTO ski VALUES
(1,7,169,229.99,4,'ski_alpin.jpg',5,1),
(2,5,181,199.99,5,'ski_randone.jpg',3,2),
(3,8,200,256.99,2,'ski_fond.jpg',3,3),
(4,6,167,231.99,4,'ski_piste.jpg',4,1),
(5,4,179,249.99,3,'ski_freestyle.jpg',4,2),
(6,7,172,219.99,6,'ski_alpin.jpg',5,3),
(7,4,171,214.99,1,'ski_freestyle.jpg',2,4),
(8,8,196,222.99,4,'ski_fond.jpg',3,1),
(9,9,142,256.99,7,'snowboard.jpg',4,4),
(10,2,191,168.99,8,'ski_polyvalent.jpg',3,4),
(11,1,100,149.99,5,'mini_ski.jpg',2,2),
(12,2,186,247.99,3,'ski_polyvalent.jpg',2,2),
(13,7,165,178.99,2,'ski_alpin.jpg',2,1),
(14,6,150,279.99,6,'ski_piste.jpg',5,2),
(15,2,183,224.99,2,'ski_polyvalent.jpg',1,3),
(16,3,168,234.99,2,'ski_freeride.jpg',5,4),
(17,6,158,189.99,4,'ski_piste.jpg',1,1),
(18,7,178,224.99,8,'ski_alpin.jpg',1,1),
(19,8,204,238.99,9,'ski_fond.jpg',3,4),
(20,9,140,248.99,6,'snowboard.jpg',4,4),
(21,6,161,234.99,1,'ski_piste.jpg',4,3),
(22,3,178,214.99,4,'ski_freeride.jpg',1,3),
(23,3,185,209.99,2,'ski_freeride.jpg',1,3);

INSERT INTO avis VALUES
(1,'Je recommande pour de la compétition', 4.5, 2, 1),
(2,'Parfait pour une personne qui débute', 4.0, 3, 4);
