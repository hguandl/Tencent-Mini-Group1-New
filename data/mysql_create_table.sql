CREATE TABLE `Authors` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`name` varchar,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Functions` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`signature` VARCHAR(255) NOT NULL UNIQUE,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Lines` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`commit_id` INT NOT NULL,
	`author_id` INT NOT NULL,
	`function_id` INT NOT NULL,
	`file_id` INT NOT NULL,
	`line_no` INT NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Commits` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`hash` varchar NOT NULL UNIQUE,
	`time` DATETIME NOT NULL,
	PRIMARY KEY (`id`)
);

CREATE TABLE `Files` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`file_path` varchar NOT NULL,
	PRIMARY KEY (`id`)
);

ALTER TABLE `Lines` ADD CONSTRAINT `Lines_fk0` FOREIGN KEY (`commit_id`) REFERENCES `Commits`(`id`);

ALTER TABLE `Lines` ADD CONSTRAINT `Lines_fk1` FOREIGN KEY (`author_id`) REFERENCES `Authors`(`id`);

ALTER TABLE `Lines` ADD CONSTRAINT `Lines_fk2` FOREIGN KEY (`function_id`) REFERENCES `Functions`(`id`);

ALTER TABLE `Lines` ADD CONSTRAINT `Lines_fk3` FOREIGN KEY (`file_id`) REFERENCES `Files`(`id`);

