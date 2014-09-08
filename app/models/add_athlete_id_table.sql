USE `accts_and_apps` ;

DROP TABLE IF EXISTS `accts_and_apps`.`strava_ids` ;
CREATE TABLE IF NOT EXISTS `accts_and_apps`.`strava_ids` (
  `id_athlete` INT NOT NULL,
  `city` VARCHAR(100) NOT NULL,
  `state` VARCHAR(45) NOT NULL,
  `id_strava_app` INT NOT NULL,
  `dt` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_athlete`))
ENGINE = InnoDB;
