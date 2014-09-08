CREATE DATABASE  IF NOT EXISTS `accts_and_apps` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `accts_and_apps`;
-- MySQL dump 10.13  Distrib 5.6.17, for osx10.6 (i386)
--
-- Host: localhost    Database: accts_and_apps
-- ------------------------------------------------------
-- Server version	5.6.20

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `strava_accts`
--

DROP TABLE IF EXISTS `strava_accts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `strava_accts` (
  `id_strava_acct` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(45) NOT NULL,
  `last_name` varchar(45) NOT NULL,
  `user_email` varchar(45) NOT NULL,
  `user_pw` varchar(45) NOT NULL,
  PRIMARY KEY (`id_strava_acct`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strava_accts`
--

LOCK TABLES `strava_accts` WRITE;
/*!40000 ALTER TABLE `strava_accts` DISABLE KEYS */;
INSERT INTO `strava_accts` VALUES (1,'tim','green','ustas06+1@hotmail.com','timgreen1'),(2,'tim','green','ustas06+2@hotmail.com','timgreen2'),(3,'tim','green','ustas06+3@hotmail.com','timgreen3'),(4,'tim','green','ustas06+4@hotmail.com','timgreen4'),(5,'tim','green','ustas06+5@hotmail.com','timgreen5'),(6,'tim','green','ustas06+6@hotmail.com','timgreen6'),(7,'tim','green','ustas06+7@hotmail.com','timgreen7'),(8,'tim','green','ustas06+8@hotmail.com','timgreen8'),(9,'tim','green','ustas06+9@hotmail.com','timgreen9'),(10,'tim','green','ustas06+10@hotmail.com','timgreen10'),(11,'tim','green','ustas06+11@hotmail.com','timgreen11'),(12,'tim','green','ustas06+12@hotmail.com','timgreen12'),(13,'tim','green','ustas06+13@hotmail.com','timgreen13'),(14,'tim','green','ustas06+14@hotmail.com','timgreen14'),(15,'tim','green','ustas06+15@hotmail.com','timgreen15'),(16,'tim','green','ustas06+16@hotmail.com','timgreen16'),(17,'tim','green','ustas06+17@hotmail.com','timgreen17'),(18,'tim','green','ustas06+18@hotmail.com','timgreen18'),(19,'tim','green','ustas06+19@hotmail.com','timgreen19'),(20,'tim','green','ustas06+20@hotmail.com','timgreen20'),(21,'tim','green','ustas06+21@hotmail.com','timgreen21'),(22,'tim','green','ustas06+22@hotmail.com','timgreen22'),(23,'tim','green','ustas06+23@hotmail.com','timgreen23'),(24,'tim','green','ustas06+24@hotmail.com','timgreen24'),(25,'tim','green','ustas06+25@hotmail.com','timgreen25'),(26,'tim','green','ustas06+26@hotmail.com','timgreen26'),(27,'tim','green','ustas06+27@hotmail.com','timgreen27'),(28,'tim','green','ustas06+28@hotmail.com','timgreen28'),(29,'tim','green','ustas06+29@hotmail.com','timgreen29'),(30,'tim','green','ustas06+30@hotmail.com','timgreen30'),(31,'tim','green','ustas06+31@hotmail.com','timgreen31'),(32,'tim','green','ustas06+32@hotmail.com','timgreen32'),(33,'tim','green','ustas06+33@hotmail.com','timgreen33'),(34,'tim','green','ustas06+34@hotmail.com','timgreen34'),(35,'tim','green','ustas06+35@hotmail.com','timgreen35'),(36,'tim','green','ustas06+36@hotmail.com','timgreen36'),(37,'tim','green','ustas06+37@hotmail.com','timgreen37'),(38,'tim','green','ustas06+38@hotmail.com','timgreen38'),(39,'tim','green','ustas06+39@hotmail.com','timgreen39'),(40,'tim','green','ustas06+40@hotmail.com','timgreen40'),(41,'tim','green','ustas06+41@hotmail.com','timgreen41'),(42,'tim','green','ustas06+42@hotmail.com','timgreen42'),(43,'tim','green','ustas06+43@hotmail.com','timgreen43'),(44,'tim','green','ustas06+44@hotmail.com','timgreen44'),(45,'tim','green','ustas06+45@hotmail.com','timgreen45'),(46,'tim','green','ustas06+46@hotmail.com','timgreen46'),(47,'tim','green','ustas06+47@hotmail.com','timgreen47'),(48,'tim','green','ustas06+48@hotmail.com','timgreen48'),(49,'tim','green','ustas06+49@hotmail.com','timgreen49'),(50,'tim','green','ustas06+50@hotmail.com','timgreen50'),(51,'tim','green','ustas06+51@hotmail.com','timgreen51'),(52,'tim','green','ustas06+52@hotmail.com','timgreen52'),(53,'tim','green','ustas06+53@hotmail.com','timgreen53'),(54,'tim','green','ustas06+54@hotmail.com','timgreen54'),(55,'tim','green','ustas06+55@hotmail.com','timgreen55'),(56,'tim','green','ustas06+56@hotmail.com','timgreen56'),(57,'tim','green','ustas06+57@hotmail.com','timgreen57'),(58,'tim','green','ustas06+58@hotmail.com','timgreen58'),(59,'tim','green','ustas06+59@hotmail.com','timgreen59'),(60,'tim','green','ustas06+60@hotmail.com','timgreen60'),(61,'tim','green','ustas06+61@hotmail.com','timgreen61'),(62,'tim','green','ustas06+62@hotmail.com','timgreen62'),(63,'tim','green','ustas06+63@hotmail.com','timgreen63'),(64,'tim','green','ustas06+64@hotmail.com','timgreen64'),(65,'tim','green','ustas06+65@hotmail.com','timgreen65'),(66,'tim','green','ustas06+66@hotmail.com','timgreen66'),(67,'tim','green','ustas06+67@hotmail.com','timgreen67'),(68,'tim','green','ustas06+68@hotmail.com','timgreen68'),(69,'tim','green','ustas06+69@hotmail.com','timgreen69'),(70,'tim','green','ustas06+70@hotmail.com','timgreen70'),(71,'tim','green','ustas06+71@hotmail.com','timgreen71'),(72,'tim','green','ustas06+72@hotmail.com','timgreen72'),(73,'tim','green','ustas06+73@hotmail.com','timgreen73'),(74,'tim','green','ustas06+74@hotmail.com','timgreen74'),(75,'tim','green','ustas06+75@hotmail.com','timgreen75'),(76,'tim','green','ustas06+76@hotmail.com','timgreen76'),(77,'tim','green','ustas06+77@hotmail.com','timgreen77'),(78,'tim','green','ustas06+78@hotmail.com','timgreen78'),(79,'tim','green','ustas06+79@hotmail.com','timgreen79'),(80,'tim','green','ustas06+80@hotmail.com','timgreen80'),(81,'tim','green','ustas06+81@hotmail.com','timgreen81'),(82,'tim','green','ustas06+82@hotmail.com','timgreen82'),(83,'tim','green','ustas06+83@hotmail.com','timgreen83'),(84,'tim','green','ustas06+84@hotmail.com','timgreen84'),(85,'tim','green','ustas06+85@hotmail.com','timgreen85'),(86,'tim','green','ustas06+86@hotmail.com','timgreen86'),(87,'tim','green','ustas06+87@hotmail.com','timgreen87'),(88,'tim','green','ustas06+88@hotmail.com','timgreen88'),(89,'tim','green','ustas06+89@hotmail.com','timgreen89'),(90,'tim','green','ustas06+90@hotmail.com','timgreen90'),(91,'tim','green','ustas06+91@hotmail.com','timgreen91'),(92,'tim','green','ustas06+92@hotmail.com','timgreen92'),(93,'tim','green','ustas06+93@hotmail.com','timgreen93'),(94,'tim','green','ustas06+94@hotmail.com','timgreen94'),(95,'tim','green','ustas06+95@hotmail.com','timgreen95'),(96,'tim','green','ustas06+96@hotmail.com','timgreen96'),(97,'tim','green','ustas06+97@hotmail.com','timgreen97'),(98,'tim','green','ustas06+98@hotmail.com','timgreen98'),(99,'tim','green','ustas06+99@hotmail.com','timgreen99'),(100,'tim','green','ustas06+100@hotmail.com','timgreen100');
/*!40000 ALTER TABLE `strava_accts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-09-07 21:02:05
