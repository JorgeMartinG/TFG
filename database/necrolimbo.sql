DROP DATABASE IF EXISTS `necrolimbo`;
CREATE DATABASE IF NOT EXISTS `necrolimbo`;
USE `necrolimbo`;
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`(
	`id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(30) NOT NULL,
    `mail` varchar(120) NOT NULL,
    `passwd` char(60) NOT NULL,
    `tel` char(9),
    `reg_date` datetime NOT NULL,
    PRIMARY KEY (id)
)ENGINE = InnoDB;
DROP TABLE IF EXISTS `item`;
CREATE TABLE `item`(
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(60) NOT NULL,
    `descr` text NOT NULL,
    `image` varchar(512) NOT NULL,
	PRIMARY KEY (id)
)ENGINE = InnoDB;
DROP TABLE IF EXISTS `trade`;
CREATE TABLE `trade`(
	`id` int NOT NULL AUTO_INCREMENT,
    `date` datetime NOT NULL,
    `id_user` int NOT NULL,
    `id_item` int NOT NULL,
    FOREIGN KEY (id_user) 
    REFERENCES user(id),
    FOREIGN KEY (id_item) 
    REFERENCES item(id),
	PRIMARY KEY (id) 
)ENGINE = InnoDB;
DROP TABLE IF EXISTS `stash`;
CREATE TABLE `stash`(
	`id_item` int NOT NULL,
    `id_user` int NOT NULL,
    FOREIGN KEY (id_item) 
    REFERENCES item (id),
    FOREIGN KEY (id_user) 
    REFERENCES user (id),
    PRIMARY KEY (id_user, id_item)
)ENGINE = InnoDB;
