CREATE DATABASE IF NOT EXISTS CharityStoreDB;
USE CharityStoreDB;
DROP TABLE IF EXISTS `SellersInfo`;
CREATE TABLE `SellersInfo` (
    `seller_no` text,
    `charity_name` text,
    `email` text
);


LOCK TABLES `SellersInfo` WRITE;
INSERT INTO `SellersInfo` VALUES ('1', 'Water Charity', 'watercharity@columbia.edu');
INSERT INTO `SellersInfo` VALUES ('2', 'Food Charity', 'foodcharity@columbia.edu');
INSERT INTO `SellersInfo` VALUES ('3', 'School Supply Charity', 'schoolsupplycharity@columbia.edu');

UNLOCK TABLES;