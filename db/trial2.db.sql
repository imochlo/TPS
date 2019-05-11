BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `transactions` (
	`transNo`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`custNo`	INTEGER,
	`invoiceNo`	INTEGER
);
INSERT INTO `transactions` VALUES (1,1,1);
INSERT INTO `transactions` VALUES (2,2,2);
INSERT INTO `transactions` VALUES (3,3,3);
INSERT INTO `transactions` VALUES (4,4,4);
INSERT INTO `transactions` VALUES (5,5,5);
INSERT INTO `transactions` VALUES (6,6,6);
INSERT INTO `transactions` VALUES (7,7,7);
INSERT INTO `transactions` VALUES (8,8,8);
INSERT INTO `transactions` VALUES (9,9,9);
INSERT INTO `transactions` VALUES (10,10,10);
CREATE TABLE IF NOT EXISTS `menu` (
	`menuNo`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT,
	`category`	TEXT,
	`price`	REAL
);
INSERT INTO `menu` VALUES (1,'Beer Battered Onion Rings','Appetizers',175.0);
INSERT INTO `menu` VALUES (2,'Croquets','Appetizers',195.0);
INSERT INTO `menu` VALUES (3,'Chicken Parmigiano Poppers','Appetizers',185.0);
INSERT INTO `menu` VALUES (4,'Poutine','Appetizers',190.0);
INSERT INTO `menu` VALUES (5,'Fried Chicken Wings','Appetizers',195.0);
INSERT INTO `menu` VALUES (6,'Fish and Chips','Appetizers',195.0);
INSERT INTO `menu` VALUES (7,'Poached Mussels','Appetizers',200.0);
INSERT INTO `menu` VALUES (8,'Bacon and Cheese Fries','Appetizers',175.0);
INSERT INTO `menu` VALUES (9,'Spinach-Banana Blossom','Appetizers',175.0);
INSERT INTO `menu` VALUES (10,'Cioppino','Soup',135.0);
INSERT INTO `menu` VALUES (11,'Truffled Mushroom','Soup',145.0);
INSERT INTO `menu` VALUES (12,'Roasted Pumpkin','Soup',135.0);
INSERT INTO `menu` VALUES (13,'Seafood Chowder','Soup',145.0);
INSERT INTO `menu` VALUES (14,'House Salad','Salad',195.0);
INSERT INTO `menu` VALUES (15,'Caesar Salad','Salad',190.0);
INSERT INTO `menu` VALUES (16,'Greek Salad','Salad',210.0);
INSERT INTO `menu` VALUES (17,'Asian Salad','Salad',190.0);
INSERT INTO `menu` VALUES (18,'Signature Burger','Sandwiches',275.0);
INSERT INTO `menu` VALUES (19,'Four Cheese Burger =','Sandwiches',270.0);
INSERT INTO `menu` VALUES (20,'Fried Chicken Sandwich','Sandwiches',275.0);
INSERT INTO `menu` VALUES (21,'Chives Chicken Sandwich','Sandwiches',275.0);
INSERT INTO `menu` VALUES (22,'Truffled Mushroom Burger','Sandwiches',285.0);
INSERT INTO `menu` VALUES (23,'Truffled Egg Sandwhich','Sandwiches',220.0);
INSERT INTO `menu` VALUES (24,'Grilled Chicken Pesto','Pasta',245.0);
INSERT INTO `menu` VALUES (25,'Truffled Mushroom','Pasta',250.0);
INSERT INTO `menu` VALUES (26,'Frutti di Mare','Pasta',250.0);
INSERT INTO `menu` VALUES (27,'Vongole','Pasta',245.0);
INSERT INTO `menu` VALUES (28,'Tuffled Mac & Cheese','Pasta',250.0);
INSERT INTO `menu` VALUES (29,'Salted Egg Carbonara','Pasta',245.0);
INSERT INTO `menu` VALUES (30,'Farmet''s Pasta','Pasta',240.0);
INSERT INTO `menu` VALUES (31,'Spinach & Blue Cheese Pasta','Pasta',245.0);
INSERT INTO `menu` VALUES (32,'Thrice Cooked Spicy Chicken Adobo','Entree',295.0);
INSERT INTO `menu` VALUES (33,'Pork Belly Crisp','Entree',290.0);
INSERT INTO `menu` VALUES (34,'Beef Salpicao','Entree',280.0);
INSERT INTO `menu` VALUES (35,'Chives Signature Ribs','Entree',350.0);
INSERT INTO `menu` VALUES (36,'Grilled Peri-Pero Chicken','Entree',185.0);
INSERT INTO `menu` VALUES (37,'Grilled Salmon with Puttanesca','Entree',325.0);
INSERT INTO `menu` VALUES (38,'Shrimp and Chorizo Gambas','Entree',350.0);
INSERT INTO `menu` VALUES (39,'Baked Pork Schnitzel','Entree',295.0);
INSERT INTO `menu` VALUES (40,'Beef Stroganoff','Entree',295.0);
INSERT INTO `menu` VALUES (41,'Tuffled Salisbury Steak','Entree',270.0);
INSERT INTO `menu` VALUES (42,'Grilled Korean Porkchop','Entree',295.0);
INSERT INTO `menu` VALUES (43,'Salted Egg Pork Belly','Entree',300.0);
INSERT INTO `menu` VALUES (44,'Roasted Salmon Head Teriyaki','Entree',310.0);
INSERT INTO `menu` VALUES (45,'Sisig Fritters','Entree',295.0);
INSERT INTO `menu` VALUES (46,'Pan Seared Mahi-Mahi with Lemon Basil Sauce','Entree',290.0);
INSERT INTO `menu` VALUES (47,'Chicken Picatta','Entree',275.0);
INSERT INTO `menu` VALUES (48,'Roasted Lemon Pepper Chicken','Entree',290.0);
INSERT INTO `menu` VALUES (49,'Grilled Salmon with Mango Calamansi Salsa','Entree',320.0);
INSERT INTO `menu` VALUES (50,'Sprite','Soda in Can',50.0);
INSERT INTO `menu` VALUES (51,'Coke','Soda in Can',50.0);
INSERT INTO `menu` VALUES (52,'Coke Light','Soda in Can',50.0);
INSERT INTO `menu` VALUES (53,'Coke Zero','Soda in Can',50.0);
INSERT INTO `menu` VALUES (54,'Royal','Soda in Can',50.0);
INSERT INTO `menu` VALUES (55,'Coke Vanilla','Soda in Can',70.0);
INSERT INTO `menu` VALUES (56,'Barqs','Soda in Can',70.0);
INSERT INTO `menu` VALUES (57,'Stellina''s Lemonade','Coolers',85.0);
INSERT INTO `menu` VALUES (58,'Stellina''s Cranberry Lemonade','Coolers',85.0);
INSERT INTO `menu` VALUES (59,'Watermelon Cooler (Glass)','Coolers',120.0);
INSERT INTO `menu` VALUES (60,'Watermelon Cooler (Pitcher)','Coolers',240.0);
INSERT INTO `menu` VALUES (61,'Lemongrass Iced Tea (Glass)','Coolers',120.0);
INSERT INTO `menu` VALUES (62,'Lemongrass Iced Tea (Pitcher)','Coolers',180.0);
INSERT INTO `menu` VALUES (63,'Rasberry Iced Tea (Glass)','Coolers',70.0);
INSERT INTO `menu` VALUES (64,'Rasberry Iced Tea (Pitcher)','Coolers',120.0);
INSERT INTO `menu` VALUES (65,'2A','Platter',650.0);
INSERT INTO `menu` VALUES (66,'2B','Platter',725.0);
INSERT INTO `menu` VALUES (67,'4A','Platter',1099.0);
INSERT INTO `menu` VALUES (68,'4B','Platter',1199.0);
INSERT INTO `menu` VALUES (69,'6A','Platter',1599.0);
INSERT INTO `menu` VALUES (70,'6B','Platter',1699.0);
CREATE TABLE IF NOT EXISTS `invoice` (
	`invoiceNo`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`date`	DATE,
	`discAmt`	INTEGER,
	`totAmt`	REAL,
	`rcvAmt`	REAL
);
INSERT INTO `invoice` VALUES (1,'2019-04-20 10:13',20,3952.0,5000.0);
INSERT INTO `invoice` VALUES (2,'2019-10-25 17:39:19',0,7275.0,8000.0);
INSERT INTO `invoice` VALUES (3,'2019-11-22 11:19:51',0,2535.0,2535.0);
INSERT INTO `invoice` VALUES (4,'2020-04-19 12:50:10',10,3712.5,4000.0);
INSERT INTO `invoice` VALUES (5,'2019-12-28 10:27:17',20,4864.0,4864.0);
CREATE TABLE IF NOT EXISTS `foodOrders` (
	`orderNo`	INTEGER,
	`menuNo`	INTEGER,
	`qty`	INTEGER
);
INSERT INTO `foodOrders` VALUES (1,9,1);
INSERT INTO `foodOrders` VALUES (1,14,4);
INSERT INTO `foodOrders` VALUES (1,15,1);
INSERT INTO `foodOrders` VALUES (1,16,1);
INSERT INTO `foodOrders` VALUES (1,22,3);
INSERT INTO `foodOrders` VALUES (1,23,3);
INSERT INTO `foodOrders` VALUES (1,28,4);
INSERT INTO `foodOrders` VALUES (1,30,1);
INSERT INTO `foodOrders` VALUES (1,47,1);
INSERT INTO `foodOrders` VALUES (1,50,4);
INSERT INTO `foodOrders` VALUES (1,51,1);
INSERT INTO `foodOrders` VALUES (1,53,1);
INSERT INTO `foodOrders` VALUES (1,58,3);
INSERT INTO `foodOrders` VALUES (2,4,4);
INSERT INTO `foodOrders` VALUES (2,5,2);
INSERT INTO `foodOrders` VALUES (2,7,3);
INSERT INTO `foodOrders` VALUES (2,10,4);
INSERT INTO `foodOrders` VALUES (2,11,4);
INSERT INTO `foodOrders` VALUES (2,15,4);
INSERT INTO `foodOrders` VALUES (2,22,4);
INSERT INTO `foodOrders` VALUES (2,30,3);
INSERT INTO `foodOrders` VALUES (2,31,2);
INSERT INTO `foodOrders` VALUES (2,48,4);
INSERT INTO `foodOrders` VALUES (2,63,1);
INSERT INTO `foodOrders` VALUES (3,18,3);
INSERT INTO `foodOrders` VALUES (3,23,3);
INSERT INTO `foodOrders` VALUES (3,35,4);
INSERT INTO `foodOrders` VALUES (3,52,4);
INSERT INTO `foodOrders` VALUES (4,5,3);
INSERT INTO `foodOrders` VALUES (4,8,2);
INSERT INTO `foodOrders` VALUES (4,17,1);
INSERT INTO `foodOrders` VALUES (4,29,1);
INSERT INTO `foodOrders` VALUES (4,39,1);
INSERT INTO `foodOrders` VALUES (4,50,1);
INSERT INTO `foodOrders` VALUES (4,55,3);
INSERT INTO `foodOrders` VALUES (4,60,3);
INSERT INTO `foodOrders` VALUES (4,61,4);
INSERT INTO `foodOrders` VALUES (4,64,3);
INSERT INTO `foodOrders` VALUES (5,8,4);
INSERT INTO `foodOrders` VALUES (5,8,3);
INSERT INTO `foodOrders` VALUES (5,10,4);
INSERT INTO `foodOrders` VALUES (5,11,2);
INSERT INTO `foodOrders` VALUES (5,28,1);
INSERT INTO `foodOrders` VALUES (5,33,3);
INSERT INTO `foodOrders` VALUES (5,35,2);
INSERT INTO `foodOrders` VALUES (5,44,3);
INSERT INTO `foodOrders` VALUES (5,45,4);
INSERT INTO `foodOrders` VALUES (5,46,3);
INSERT INTO `foodOrders` VALUES (5,47,2);
INSERT INTO `foodOrders` VALUES (5,53,1);
INSERT INTO `foodOrders` VALUES (5,56,1);
INSERT INTO `foodOrders` VALUES (5,62,3);
INSERT INTO `foodOrders` VALUES (5,63,1);
INSERT INTO `foodOrders` VALUES (6,18,2);
INSERT INTO `foodOrders` VALUES (6,25,4);
INSERT INTO `foodOrders` VALUES (6,26,2);
INSERT INTO `foodOrders` VALUES (6,33,2);
INSERT INTO `foodOrders` VALUES (6,35,3);
INSERT INTO `foodOrders` VALUES (6,43,4);
INSERT INTO `foodOrders` VALUES (6,56,1);
INSERT INTO `foodOrders` VALUES (6,57,1);
INSERT INTO `foodOrders` VALUES (7,10,4);
INSERT INTO `foodOrders` VALUES (7,11,3);
INSERT INTO `foodOrders` VALUES (7,15,4);
INSERT INTO `foodOrders` VALUES (7,17,3);
INSERT INTO `foodOrders` VALUES (7,19,4);
INSERT INTO `foodOrders` VALUES (7,42,1);
INSERT INTO `foodOrders` VALUES (7,47,1);
INSERT INTO `foodOrders` VALUES (7,53,4);
INSERT INTO `foodOrders` VALUES (8,6,2);
INSERT INTO `foodOrders` VALUES (8,12,3);
INSERT INTO `foodOrders` VALUES (8,25,2);
INSERT INTO `foodOrders` VALUES (8,26,3);
INSERT INTO `foodOrders` VALUES (8,27,4);
INSERT INTO `foodOrders` VALUES (8,34,4);
INSERT INTO `foodOrders` VALUES (8,35,2);
INSERT INTO `foodOrders` VALUES (8,40,2);
INSERT INTO `foodOrders` VALUES (8,42,3);
INSERT INTO `foodOrders` VALUES (8,61,4);
INSERT INTO `foodOrders` VALUES (8,63,1);
INSERT INTO `foodOrders` VALUES (9,4,3);
INSERT INTO `foodOrders` VALUES (9,12,1);
INSERT INTO `foodOrders` VALUES (9,19,2);
INSERT INTO `foodOrders` VALUES (9,29,3);
INSERT INTO `foodOrders` VALUES (9,31,1);
INSERT INTO `foodOrders` VALUES (9,35,4);
INSERT INTO `foodOrders` VALUES (9,51,4);
INSERT INTO `foodOrders` VALUES (9,57,1);
INSERT INTO `foodOrders` VALUES (9,61,1);
INSERT INTO `foodOrders` VALUES (9,63,1);
INSERT INTO `foodOrders` VALUES (9,66,4);
INSERT INTO `foodOrders` VALUES (9,68,4);
INSERT INTO `foodOrders` VALUES (10,1,3);
INSERT INTO `foodOrders` VALUES (10,3,4);
INSERT INTO `foodOrders` VALUES (10,6,3);
INSERT INTO `foodOrders` VALUES (10,43,3);
INSERT INTO `foodOrders` VALUES (10,49,3);
INSERT INTO `foodOrders` VALUES (10,52,1);
INSERT INTO `foodOrders` VALUES (10,58,2);
INSERT INTO `foodOrders` VALUES (10,66,2);
CREATE TABLE IF NOT EXISTS `customer` (
	`custNo.`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`arrTime`	DATETIME,
	`deptTime`	DATETIME,
	`partySize`	INTEGER,
	`checkotPref`	TEXT,
	`tableNo`	INTEGER
);
INSERT INTO `customer` VALUES (1,'2019-04-20 5:51','2019-04-20 10:13',4,'Dine-In',1);
INSERT INTO `customer` VALUES (2,'2019-10-25 8:35:10','2019-10-25 17:39:19',8,'Take-Out',2);
INSERT INTO `customer` VALUES (3,'2019-11-22 0:06:34','2019-11-22 11:19:51',12,'Delivery',3);
INSERT INTO `customer` VALUES (4,'2019-04-19 12:30:10','2020-04-19 12:50:10',8,'Dine-In',4);
INSERT INTO `customer` VALUES (5,'2019-12-28 8:21:00','2019-12-28 10:27:17',2,'Delivery',5);
INSERT INTO `customer` VALUES (6,'2020-08-04 10:14','2020-08-04 12:43:22',3,'Dine-In',6);
INSERT INTO `customer` VALUES (7,'2020-10-20 12:59:11','2020-10-20 16:32:27',5,'Take-Out',7);
INSERT INTO `customer` VALUES (8,'2021-03-21 11:41:42','2021-03-21 14:33:38',3,'Delivery',8);
INSERT INTO `customer` VALUES (9,'2021-06-30 17:43:47','2021-06-30 18:30:50',6,'Dine-In',9);
INSERT INTO `customer` VALUES (10,'2022-02-13 18:52:11','2022-02-13 18:52:11',7,'Delivery',10);
COMMIT;
