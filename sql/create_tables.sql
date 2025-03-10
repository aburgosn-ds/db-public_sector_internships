CREATE TABLE IF NOT EXISTS locations (
	`id` INT AUTO_INCREMENT,
    `city` VARCHAR(40),
    `specific_location` VARCHAR(200),
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
    `organization_id` INT DEFAULT NULL,
    `to_apply` TEXT DEFAULT NULL,
    `specific_requirements` TEXT DEFAULT NULL,
    `knowledge` TEXT DEFAULT NULL,
    `salary` DECIMAL(6,2) DEFAULT NULL,
    `responsabilities` TEXT DEFAULT NULL,
    `location_id` INT DEFAULT NULL,
    `end_date` DATE DEFAULT NULL,
    `url` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`organization_id`) REFERENCES `organizations`(`id`),
    FOREIGN KEY (`location_id`) REFERENCES `locations`(`id`)
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

