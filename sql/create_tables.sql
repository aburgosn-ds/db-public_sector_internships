CREATE TABLE IF NOT EXISTS specific_locations (
	`id` INT AUTO_INCREMENT,
    `address` VARCHAR(200) UNIQUE,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS cities (
	`id` INT AUTO_INCREMENT,
    `name` VARCHAR(50) UNIQUE,
    PRIMARY KEY (`id`)
);


CREATE TABLE IF NOT EXISTS organizations (
	`id` INT AUTO_INCREMENT,
    `name` VARCHAR(200) UNIQUE,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS offers (
	`id` INT AUTO_INCREMENT,
    `offer_page_code` INT UNSIGNED UNIQUE,
    `offer_title` VARCHAR(200) DEFAULT NULL,
    `vacants` TINYINT UNSIGNED DEFAULT NULL,
    `type` ENUM('pre-profesional', 'profesional') DEFAULT NULL,
    `to_apply` TEXT DEFAULT NULL,
    `organization_id` INT DEFAULT NULL,
    `specific_requirements` TEXT DEFAULT NULL,
    `knowledge` TEXT DEFAULT NULL,
    `salary` DECIMAL(6,2) DEFAULT NULL,
    `responsabilities` TEXT DEFAULT NULL,
    `specific_location_id` INT DEFAULT NULL,
    `city_id` INT DEFAULT NULL, 
    `end_date` DATE DEFAULT NULL,
    `url` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`specific_location_id`) REFERENCES `specific_locations`(`id`),
    FOREIGN KEY (`city_id`) REFERENCES `cities`(`id`),
    FOREIGN KEY (`organization_id`) REFERENCES `organizations`(`id`)
);

CREATE TABLE IF NOT EXISTS careers(
    `id` INT AUTO_INCREMENT,
    `name` VARCHAR(100) UNIQUE,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS careers_per_offer (
    `offer_id` INT,
    `career_id` INT,
    FOREIGN KEY (`offer_id`) REFERENCES `offers`(`id`),
    FOREIGN KEY (`career_id`) REFERENCES `careers`(`id`)
);

