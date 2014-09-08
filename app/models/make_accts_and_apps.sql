-- MySQL Script generated by MySQL Workbench
-- Sat Sep  6 19:28:00 2014
-- Model: New Model    Version: 1.0
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema accts_and_apps
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `accts_and_apps` ;
CREATE SCHEMA IF NOT EXISTS `accts_and_apps` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `accts_and_apps` ;

-- -----------------------------------------------------
-- Table `accts_and_apps`.`strava_accts`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `accts_and_apps`.`strava_accts` ;

CREATE TABLE IF NOT EXISTS `accts_and_apps`.`strava_accts` (
  `id_strava_acct` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `user_pw` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_strava_acct`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `accts_and_apps`.`strava_apps`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `accts_and_apps`.`strava_apps` ;

CREATE TABLE IF NOT EXISTS `accts_and_apps`.`strava_apps` (
  `id_strava_app` INT NOT NULL AUTO_INCREMENT,
  `client_id` INT NOT NULL,
  `client_secret` VARCHAR(50) NOT NULL,
  `access_token` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_strava_app`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
