DROP DATABASE IF EXISTS ProductInfo;
CREATE DATABASE ProductInfo;
USE ProductInfo;
DROP TABLE IF EXISTS `ProductInfo`;
CREATE TABLE `ProductInfo` (
    `product_no` text,
    `product_name` text,
    `price` text,
    `inventory` text
);


LOCK TABLES `ProductInfo` WRITE;
INSERT INTO `ProductInfo` VALUES ('1', 'Water Charity', '100', '5');
INSERT INTO `ProductInfo` VALUES ('2', 'Food Charity', '500', '3');
INSERT INTO `ProductInfo` VALUES ('3', 'School Supply Charity', '50', '20');
UNLOCK TABLES;