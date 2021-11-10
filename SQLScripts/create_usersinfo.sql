DROP DATABASE IF EXISTS usersInfo;
CREATE DATABASE usersInfo;
USE usersInfo;
DROP TABLE IF EXISTS `usersInfo`;
CREATE TABLE `usersInfo` (
    `user_no` text,
    `first_name` text,
    `last_name` text,
    `email` text
);


LOCK TABLES `usersInfo` WRITE;
INSERT INTO `usersInfo` VALUES ('1', 'Phu', 'Pham', 'pdp2121@columbia.edu');
INSERT INTO `usersInfo` VALUES ('2', 'Aditya', 'Kulkarni', 'ak4725@columbia.edu');
INSERT INTO `usersInfo` VALUES ('3', 'Isha', 'Shah', 'is2404@columbia.edu');
INSERT INTO `usersInfo` VALUES ('4', 'Di', 'Chen', 'dc3260@columbia.edu');
UNLOCK TABLES;