DROP DATABASE IF EXISTS enterprise_info;
CREATE DATABASE enterprise_info DEFAULT CHARACTER SET utf8;
USE enterprise_info;
CREATE TABLE info(id BIGINT AUTO_INCREMENT PRIMARY KEY,
                en_name VARCHAR(150) UNIQUE,
                boss_name VARCHAR(150),
                address VARCHAR(150),
                property VARCHAR(150),
                type VARCHAR(150))ENGINE=InnoDB DEFAULT CHARSET=utf8;
                