USE `accts_and_apps` ;

DROP TABLE IF EXISTS `accts_and_apps`.`athletes_raw` ;
CREATE TABLE IF NOT EXISTS `accts_and_apps`.`athletes_raw` (
  `athlete_id` INT NOT NULL,
  `page` MEDIUMBLOB NOT NULL,
  `dt` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`athlete_id`))
ENGINE = InnoDB;
