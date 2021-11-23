DROP DATABASE IF EXISTS UsersInfo;
CREATE DATABASE UsersInfo;
USE UsersInfo;
DROP TABLE IF EXISTS `UsersInfo`;
CREATE TABLE `UsersInfo` (
    `user_no` text,
    `first_name` text,
    `last_name` text,
    `email` text
);


LOCK TABLES `UsersInfo` WRITE;
INSERT INTO `UsersInfo` VALUES ('1', 'Phu', 'Pham', 'pdp2121@columbia.edu');
INSERT INTO `UsersInfo` VALUES ('2', 'Aditya', 'Kulkarni', 'ak4725@columbia.edu');
INSERT INTO `UsersInfo` VALUES ('3', 'Isha', 'Shah', 'is2404@columbia.edu');
INSERT INTO `UsersInfo` VALUES ('4', 'Di', 'Chen', 'dc3260@columbia.edu');
UNLOCK TABLES;