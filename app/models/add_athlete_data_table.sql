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
  `rides_count` INT NOT NULL,
  `rides_dist_per_week` DECIMAL(2) NOT NULL,
  `rides_time_per_week` DECIMAL(2) NOT NULL,
  `runs_count` INT NOT NULL,
  `runs_dist_per_week` DECIMAL(2) NOT NULL,
  `runs_time_per_week` DECIMAL(2) NOT NULL,
  `mon_freq` DECIMAL(2) NOT NULL,
  `tues_freq` DECIMAL(2) NOT NULL,
  `wed_freq` DECIMAL(2) NOT NULL,
  `thurs_freq` DECIMAL(2) NOT NULL,
  `fri_freq` DECIMAL(2) NOT NULL,
  `sat_freq` DECIMAL(2) NOT NULL,
  `sun_freq` DECIMAL(2) NOT NULL,
  `variability` DECIMAL(3) NOT NULL,
  PRIMARY KEY (`athlete_id`))
ENGINE = InnoDB;
