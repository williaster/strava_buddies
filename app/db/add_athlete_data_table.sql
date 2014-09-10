USE `accts_and_apps` ;

-- -----------------------------------------------------
-- Table `accts_and_apps`.`athletes_data`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `accts_and_apps`.`athletes_data` ;

CREATE TABLE IF NOT EXISTS `accts_and_apps`.`athletes_data` (
  `athlete_id` INT NOT NULL,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `state` VARCHAR(45) NOT NULL,
  `ride_count` INT NOT NULL,
  `run_count` INT NOT NULL,
  `mon_freq` float NOT NULL,
  `tues_freq` float NOT NULL,
  `wed_freq` float NOT NULL,
  `thurs_freq` float NOT NULL,
  `fri_freq` float NOT NULL,
  `sat_freq` float NOT NULL,
  `sun_freq` float NOT NULL,
  `annual_dist_median` float NOT NULL,
  `annual_dist_std` float NOT NULL,
  `avatar_url` VARCHAR(150) NOT NULL,
  PRIMARY KEY (`athlete_id`))
ENGINE = InnoDB;
