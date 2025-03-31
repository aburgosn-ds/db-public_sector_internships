##### Database #####
CREATE DATABASE IF NOT EXISTS `public_sector_internships`;
USE `public_sector_internships`;

##### Tables #####
CREATE TABLE IF NOT EXISTS cities (
	`id` INT AUTO_INCREMENT,
    `name` VARCHAR(50) UNIQUE DEFAULT NULL,
    `current_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS organizations (
	`id` INT AUTO_INCREMENT,
    `name` VARCHAR(200) UNIQUE DEFAULT NULL,
    `current_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS offers (
	`id` INT AUTO_INCREMENT,
    `offer_page_code` INT UNSIGNED UNIQUE,
    `offer_title` VARCHAR(200) DEFAULT NULL,
    `vacants` TINYINT UNSIGNED DEFAULT NULL,
    `type` ENUM('PRE-PROFESIONAL', 'PROFESIONAL') DEFAULT NULL,
    `to_apply` TEXT DEFAULT NULL,
    `organization_id` INT DEFAULT NULL,
    `specific_requirements` TEXT DEFAULT NULL,
    `knowledge` TEXT DEFAULT NULL,
    `salary` DECIMAL(6,2) DEFAULT NULL,
    `responsabilities` TEXT DEFAULT NULL,
    `specific_location` VARCHAR(200),
    `city_id` INT DEFAULT NULL, 
    `end_date` DATE DEFAULT NULL,
    `url` VARCHAR(200) NOT NULL,
    `current_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `active` BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`city_id`) REFERENCES `cities`(`id`),
    FOREIGN KEY (`organization_id`) REFERENCES `organizations`(`id`)
);

CREATE TABLE IF NOT EXISTS careers(
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(100) UNIQUE,
    `current_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS careers_per_offer (
    `offer_id` INT,
    `career_id` INT,
    `current_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`offer_id`) REFERENCES `offers`(`id`),
    FOREIGN KEY (`career_id`) REFERENCES `careers`(`id`)
);



##### Stored Procedure #####
DELIMITER //

CREATE PROCEDURE update_active_status_proc()
BEGIN
	UPDATE `offers`
    SET `active` = CASE
		WHEN end_date >= CURDATE() THEN 1
        ELSE 0
	END;
END //

DELIMITER ;

CREATE EVENT update_active_status_event
ON SCHEDULE EVERY 1 DAY
DO CALL update_active_status_proc();


##### Views #####
CREATE VIEW active_offers AS 
SELECT 
id, offer_page_code, offer_title, vacants, `type`, to_apply, organization_id, specific_requirements, knowledge, salary, responsabilities, specific_location, city_id, end_date, url, `current_date`
FROM offers 
WHERE `active` = 1;

CREATE VIEW inactive_offers AS 
SELECT 
id, offer_page_code, offer_title, vacants, `type`, to_apply, organization_id, specific_requirements, knowledge, salary, responsabilities, specific_location, city_id, end_date, url, `current_date`
FROM offers 
WHERE `active` = 0;


##### Users #####
CREATE USER 'user' IDENTIFIED BY '';
GRANT SELECT ON `public_sector_internships`.* to 'user';