
DROP DATABASE IF EXISTS `notes_db`;
CREATE DATABASE IF NOT EXISTS `notes_db` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `notes_db`;




DROP TABLE IF EXISTS `careers`;
CREATE TABLE IF NOT EXISTS `careers` (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(60) NOT NULL UNIQUE COMMENT 'name',
  `description` varchar(200) DEFAULT NULL COMMENT 'username',
  `users` varchar(60) DEFAULT NULL COMMENT 'users',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='';


DROP TABLE IF EXISTS `roles`;
CREATE TABLE IF NOT EXISTS `roles` (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(60) NOT NULL UNIQUE COMMENT 'name',
  `description` varchar(200) DEFAULT NULL COMMENT 'username',
  `users` varchar(60) DEFAULT NULL COMMENT 'users',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='';

DROP TABLE IF EXISTS `notes`;
CREATE TABLE IF NOT EXISTS `notes` (
  `id` bigint(50) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `title` varchar(80) NOT NULL COMMENT 'name',
  `user_id` bigint(50) DEFAULT NULL COMMENT 'user_id',
  `body` longtext DEFAULT NULL COMMENT 'users',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='';



DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `email` varchar(60) NOT NULL UNIQUE COMMENT 'email',
  `username` varchar(60) DEFAULT NULL UNIQUE COMMENT 'username',
  `first_name` varchar(60) DEFAULT NULL COMMENT 'first_name',
  `last_name` varchar(60) DEFAULT NULL COMMENT 'last_name',
  `password_hash` varchar(128) DEFAULT NULL COMMENT 'password_hash',
  `subject_id` bigint(50) DEFAULT NULL COMMENT 'subject_id',
  `role_id` bigint(255) DEFAULT NULL COMMENT 'role_id',
  `is_admin` boolean DEFAULT FALSE,
  `notes` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `idx_email`(`email`),
  INDEX `idx_username`(`username`),
  INDEX `idx_first_name`(`first_name`),
  INDEX `idx_last_name`(`last_name`),
  CONSTRAINT subject_id_FK FOREIGN KEY(subject_id) REFERENCES careers(id),
  CONSTRAINT role_id_FK FOREIGN KEY(role_id) REFERENCES roles(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='';
