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

--
-- Table structure for table `strava_apps`
--

DROP TABLE IF EXISTS `strava_apps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `strava_apps` (
  `id_strava_app` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `client_secret` varchar(50) NOT NULL,
  `access_token` varchar(50) NOT NULL,
  PRIMARY KEY (`id_strava_app`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strava_apps`
--

LOCK TABLES `strava_apps` WRITE;
/*!40000 ALTER TABLE `strava_apps` DISABLE KEYS */;
INSERT INTO `strava_apps` VALUES (1,2827,'f9f794ac535ddae2ea40357d3a493686e900d79b','74f38ae909e94eb4805d13f5c424c4f49132be9f'),(2,2828,'52e2caa141afa98e8f76e9b1732d0e030a337511','62b66543be7a7524c47c6f33e87f0aa40e029e2c'),(3,2829,'ec255756bb13f8b48945bcc86eeb1a9175507879','0d8aec8e09b2fb55e2262d974f1be7e504e123d0'),(4,2830,'b7822e2efd64064c36067a3f41d330a602c90a26','ac659bdb30a11dac4d51c20f231a20c9313f7283'),(5,2831,'5f7590217bb6f37b4e7f6f51696fd7057f946bdb','14e35e9c9613db73705af633477364a3d36d397b'),(6,2832,'41b782c5db9c586068fbb0ce165114f68f0e6f30','8a83e703df44b15b501e372a596dc19aa793d077'),(7,2833,'3291ee17946232b55b38f85a7879d88788ca5d1a','18d6038f0f4d6364582ee871e5c1e69879c75239'),(8,2834,'9abeae1168bc34beab8034b49d97579a05d7c6a2','4d52b59e36da10cd7c9b703d9334f70eecaa1aac'),(9,2835,'4ff281eda2791ea54a889806225c3d36977ee127','f52707a9ab9a75e31a9aa0aa415e085e830671a1'),(10,2836,'78531aa4d0a9da1b47902cb2649569d901bafd46','f61b4333d9a1e2e087424b1e6087463dd488b99f'),(11,2837,'bb488455f47b7f9546ab7c2920f6272b96ce0976','079d6ec0cda0087aa5825c4bebafe3b2d978fc6d'),(12,2838,'d5ed0b53c7291cc35ea661bd26b5674957853a59','770d688e67e77778c2166ac5694395bab80ab918'),(13,2839,'9f718e8b29ae017232b16dcb9c0133ce9c65d37e','d6bbbe569b9e6e323d26176d000f9244483ac85c'),(14,2840,'46f4fd3866ad8567e953e3c789ab12052f3e9745','778aab3ac5bc8b88832ed0447061768e88fce6bf'),(15,2841,'ebe7d93997630622ac92f672d701dc05f97d90d1','a3d2995a19b92df72573a43c4448208b89a75ff8'),(16,2842,'6adde803f89d267e05c1a5a02edf6728026d4408','2c968c5a9254b5c294ce1ab401b9dbf0a9e02386'),(17,2843,'37297e8559ffe27d2b92b092d3364a933cd1a3df','1d9d5b124c2cbfdea00f8258c347482004fb5860'),(18,2844,'88f87f011a0075867b6908577f04feef49bf4756','c3bca8396be6d7211742b84d3baef0084256e8df'),(19,2845,'f2a605c58dbcf804b73af0131751bbb3fc2e9fc5','1b0174b7f70d49436bb732e10fc4922661ed49a3'),(20,2846,'6475e8638ffde10b3e61b968c55b5940ddc9f7e6','3cf7eeb6dfbe54b5fa26eb04be355212493f1482'),(21,2847,'170e27faa4029892668792b1b8df73c3234d38cd','d0ae6d090008aa0c2ac862f318bb2f6d9771042d'),(22,2848,'7733350facde357fc0392c64c91f22275bfb5d40','52fa98de6d2a15af97882a0d2fed1e7d8b9d2c55'),(23,2849,'f96c73969e44ac945f76c1fbb63850fe15270f77','f418536afc136dddc663d7bce5dfd1fcb89cfd58'),(24,2850,'b7027c4b3c785afd8b74be62b8a870fc9e7d19f3','91ea61b861cdb41d47ffc99dd2a610671c2f8724'),(25,2851,'39be149993efe91252f579f9cff0ac3d6d2f1546','240ff9b6004802693309319568d4063aa3ad676a'),(26,2852,'b2a037280cfa7d39cc5f0a737d04cc74ea6323e5','b0769b399bab564c7705f59b0a956beb4d9a04dc'),(27,2853,'8bc1a1d49af6c647381f4ed82581ed836f5c56d3','630e57d920cd648dab6f6b745a2e3f2bf77e6a7e'),(28,2854,'1852b454e31234680522ea4437b84fed3f325884','510012820ee1008e1c934cee39d69bcd4f4a678a'),(29,2855,'7c7a83019a758448c45961783dfb39071e489655','9824ae3f005c97892b66d658541236bf2abc29b3'),(30,2856,'e88f958286516d313c8267809418b58916ec9ae2','20ec8ca3f1789697c1a7dc2e40cd3257d0213e65'),(31,2857,'0df7451e36d692df1b4b22abf7f4073863f249d6','1da10230c9459d688a4922020c52c22645e027d3'),(32,2858,'8a7d213f7367e7765c975957348a5b4f93d2deda','5d2e70e845953319cc95398abc3d1030113cfae5'),(33,2860,'07d68dcabf00ffef9f15f7992385b7c58b0acd51','1f126b22fe863a66020f7d3d2c1b7deee7444764'),(34,2861,'1fafac4eddcad7118343d5fdf47a3995514fc2ea','cdfffdf04ef6504123f37fe57e705e894d1d7312'),(35,2862,'d8334aae77f4dd787355b78b586fd488a3e1cf64','cdff49a71dee84745f753dc8f0357503d26b99e9'),(36,2863,'9721329ec9965218f511ae7bd7de47fb1626517a','aa2e12a1959f131cc28a7d2ce5f089cd14632496'),(37,2864,'6fbeab94b4d385c0c497be745e0dfc3be5a6cc84','f9aaec8c9630bdf160e48eb1641fb4a1c2775d68'),(38,2865,'2da805e787d33ec056aa8f5eec68e87dc274b53e','45152d3ae02442a935c831665db89fda4bebfc7a'),(39,2866,'06f7ba02169b5f378d7ab0ce1d398d558a2741f4','c1e2d11e45e9efbd119385f0f7226575c5199d8a'),(40,2867,'a9376bd3b67cd93e0f2269ce53025c07bf8da9fe','a688ef622fd711ce966488e98d69ccc3f51bac48'),(41,2868,'b642889f154bee61a4e94be95016709d9be09f95','31f55e69c608481268333583eec3eee3929eb477'),(42,2869,'55ac804d4674770816376e666ff0379d3809bb08','c8c85835b24e85b51d6d7cf7c6b6951770903584'),(43,2870,'245206c1f076ce37078b78dc52acb72ae2dd5ba0','cfcf94410fac390b99ffbc460122993c128c76c9'),(44,2871,'4b510d27f7f74924f86d8f7c44cc9a38376633ee','529524067459431b5481e09dc8b3c0bda4947b5f'),(45,2872,'fca53182b3e7dd9858818464e23cb561ab5a5b4c','8a379a456d02bbb3623654b1a35db141a37cb313'),(46,2873,'a1555cac4723b73d35f0cffa40f92885434596c5','cbfa0b1001d2f16984adbb6b394409ac2a6d1f5f'),(47,2874,'b55233ec3303beba1a42df9cec1fc2aa9670f9e8','0dce9ba755ef3105a0cd223ba6b07db2bb2282c7'),(48,2875,'c3bb7bb612630e2f86778358aed2e466b90db5ef','3477e4a3c97c0548aa1f67485215168ff1857020'),(49,2876,'7f357aa01602a1799ee7b94494cb6d08e01dd666','bff64cb0ddc67b32f1c0c6935d152b389a70ed23'),(50,2877,'339c1c7f51dba2df296fc5e61d8d95386479b6a9','227577b3f88721bbec91d6f3d028ccaf5009dfd2'),(51,2878,'cc7779e0d904d93f9af32f675e86f7b53551a932','0c00c21be2bd5c74c65edd3e6b6ab6e95c1edf65'),(52,2879,'26dd9e2064266778f576718bed42972dc75ad9e9','dcc98202234c07415cd471bdff49912d35446029'),(53,2880,'048e2b088a8cc83974ebf452e54557f466f1a8c9','a314d1e9078487035219bb6119f2e69a078217c2'),(54,2881,'9b2b48683b6e2bf38c4db64b52485fffb75c0367','8679cc2581dc83edb229cba14cf5d6877ae16d6b'),(55,2882,'96ef52b94b1a1f30523fb4261fa7638254100ca6','94deba0311ef9639695ed2bb95a7ed8484f66c05'),(56,2883,'f4b608f2ebf164219ac00413a5c03f64910babc2','c026a27d950e848b9e11e2d682dc3a28d4dc10d8'),(57,2884,'95be129063e807278aa142004c98f1bd05a3fb5a','22892ea1d723b0a2806c8ce6366913f91ca78fb8'),(58,2887,'2b8faadb15882e8ac13070a8400c98a90f3032b2','8c24d3e79ed4defb9e4f47d5089ef51fa641e741'),(59,2885,'aa213350fb380b9c80c1a04226f23e5b27f70e38','456bf26b64d89dd9e3e35b297501257b27d5d861'),(60,2886,'a2802b7a922346999f2038afa271953dca33a558','69616222b5174b7fa58ee466318244c66fa36a86'),(61,2888,'6679af9ec458122782e6cb28bd0ab3ea4d400a3f','a80d11d00af9826e3c83198341fbaeb18f179c1a'),(62,2889,'77f6aa77a0a53a1b91212fcf81cf78897a1c94df','d755c61c8fd2628bebaa4088ea6af9c782dbb6c6'),(63,2890,'f7449380e2217b3983b66b54df17d4c17d168cf8','2be3d56a53f07fdae06279f2aee7ebb289435d4d'),(64,2891,'53a818f67a996933bf5a5de5c43a3255d9c3dec9','bebebd061645a06ab4ca8f1b7378b87b5ccd7c5f'),(65,2892,'fa9d0a47aa314adc9cb530cc12b5b6a81ccb0f27','a5597ebb08ec5a9876dfe3a603ac239d870e1b10'),(66,2893,'9d24c5cb1d0b9afbe5f1be6a3d9c1a2b7d8227d8','aa3e27026ebe9daa0a60128f6d25c72fb6fe5a9e'),(67,2894,'476bb89060abb8e4cdccc7d0ef86353a92f765e5','b2e731c958386719fa4f90bf58bdaa5472d09306'),(68,2895,'aa0d1b8f584d4cbd96b242668b674b010b180456','c881d1bbad494261cb05e28d149748c94db444db'),(69,2896,'e273e1cf548feb1a7ee09c080e6e63d7ebb78b59','8902e17f220b2c4ba44e119a1db1e74c43f4869c'),(70,2897,'98d3eacea15f21feff0540dd9bd74a75e0f51051','4839acd2cd4fadb6e31e510698c444e822714dbd'),(71,2898,'53bb47f480d78e833a1286414edb09e35a1c38d8','fe314b09f205289a7635e11073491f45cdb15919'),(72,2899,'89f71d018f496a24f68d5e6c6e10aa603a87d2aa','19fb9f22c46b23375e40d19e9f00f2010983ee22'),(73,2900,'f206681fea0d1abbaf35ba51b26fa385c49a369d','24e3852f46c5b5906547897f9d3f5c042b1bb7b6'),(74,2901,'c21c2abd315521ed7fb3c843033ba823106b3d55','76a04d9630725655f372818603b9d7faaa104920'),(75,2902,'a7da28ecbb22f592c4ea7c7dcc2d9c866b071c9e','9f9d96c999c1b1d9c83ac1a590673bdab4781636'),(76,2903,'fc25950cc5120976cf9468437854ece037220e32','7a646527198e35b7419ea688d3948cea752b117d'),(77,2904,'d67d55296d8ad4bd6e928f78b52df313ab003ab8','908782eead6592999849f10460f8e811695ab13d'),(78,2905,'31ce818c68a6ae0017e3b0163cf0f004e565c417','15287b6dd480673399d3af54b07f2b1f1cfa4b7c'),(79,2906,'2e2059b08bebf757a19629e68d3cf634be355fa8','a67ab73fb2524490a448b7ada9e518e25fda664a'),(80,2907,'cad06f218bdd7c67320b7e2bbeaf063be369c27e','032e72870921f4a9db89374260ef61d8c958f2a7'),(81,2908,'fb3d06b7260d93b5b1953e0261ef456245b93a9d','916cdac39895f1d1c8bf850b41ec8824f78d029b'),(82,2909,'7c55a5ba35be390c48ef64ca7568371dffeb86c6','39f07c112d0fbee168f41beaaa5199781fe95ac0'),(83,2910,'72953c21ba49aa0a2d107c8314edafd1e8f1f521','9bcebc18908d1a41affb252fe41835ebf13839fc'),(84,2911,'7e05ccbb46ed777742773bbc506e9ae157f3b7ff','ff27c0df340911af4aea44021b942c7c9e8045d6'),(85,2912,'f29631cdfc8967b5761525c4164ee232b1b07c32','4edc76b796e3e6ec6769f70e4f8e404c1c4b6b61'),(86,2913,'77993be8d61adb7bd090fd7691c9e3d71db8401f','b16b8864eaa917e4f793a4c60f15b31af64afea1'),(87,2914,'1c7364ec4a1e083a2646c22dc6a19321413c3a88','b02214a781d5d730d34d2e1a619f9f99eed21dc6'),(88,2915,'17e8280b1f50e98900e525cd8433b924f0c7d46f','1693cb72315458bab431ad6681e4393621b898ec'),(89,2916,'bc114d3732480d1b01fd0ebe246fbeaaf884f6f4','8d7484bd2e992e08e72a5bb8458a98ece5f5721a'),(90,2917,'1a0c55fcfa8cc87beeb968c5bc1e468cf1c7f0e0','8badffb959d6c498049ca3e61d564b9ae0c229fa'),(91,2918,'006da3f6f73fe2903542cc33ea0e35a8fb491a40','28f064c757271a577a45bca11f661a55294a7ccd'),(92,2919,'7c338c5a8c29582a5196ec9fb10aa1a3895f1a23','64872e7a96bf2e1d798078b55479eebc59a63cf4'),(93,2920,'ebf128fb22a352719605245edd4871a1d3287785','320b417a47e298a4955ab05d06f997378a4d4dc4'),(94,2921,'c2a20f1fea6510eac1552f0a3ccd30f0b3189689','24004134b3e7403dd91bfaf50e8c0f8de35b82d4'),(95,2922,'4907abab5000b4a6b705d14651675ae9cbe12501','d316bf8e3c7d3a9c4ce0aa97db4f372ab1feb778'),(96,2923,'724d123091dc11f8ab077568efc2894ec5148d13','3ee9e27a0492da5bff4ef4c3c5e47fed7d1ba97e'),(97,2924,'cebb31ae6752e9465121a39a26b9b999350e6609','bbe5e975009e3dd12de720d439cc6749f482bbf7'),(98,2925,'a370f66ab399bb6b198ee321cb22455037ecb896','54965a06343c7848cdfcb7e4b5a5aed49ae0222a'),(99,2926,'bed01d717ce4089486c280535f681e387840ed16','d20f8791736f6973e4c298d1906e743075f09fe3'),(100,2927,'3828565e97b89cbd9ef3a6e3327803b9543be005','52a1ba21fe715110783eb33e96df4d1fc7cbf029'),(101,2826,'0ce1197ef390982ea0d10d3d6b234ce994313031','1ea68b72721de1795005a392ed78b7aaa161c230'),(102,2780,'e66454a8d753d6ef126e4f37499588011ff25a11','e21378aea6e4971836150bab87dcfe3edc09291f');
/*!40000 ALTER TABLE `strava_apps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `strava_ids`
--

DROP TABLE IF EXISTS `strava_ids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `strava_ids` (
  `id_athlete` int(11) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(45) NOT NULL,
  `id_strava_app` int(11) NOT NULL,
  `dt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_athlete`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `strava_ids`
--

LOCK TABLES `strava_ids` WRITE;
/*!40000 ALTER TABLE `strava_ids` DISABLE KEYS */;
INSERT INTO `strava_ids` VALUES (1,'NA','NA',101,'2014-09-08 05:18:30'),(2,'NA','NA',101,'2014-09-08 05:22:30'),(3,'NA','NA',101,'2014-09-08 05:22:34'),(4,'NA','NA',101,'2014-09-08 05:22:37'),(5,'NA','NA',101,'2014-09-08 05:22:38'),(6,'NA','NA',101,'2014-09-08 05:22:42'),(7,'Norwich','Vermont',101,'2014-09-08 05:22:46'),(8,'San Francisco','CA',101,'2014-09-08 05:22:47'),(9,'Helsingborg','',101,'2014-09-08 05:22:50'),(10,'Portola Valley','CA',101,'2014-09-08 05:22:53'),(11,'NA','NA',101,'2014-09-08 05:22:56'),(12,'South Lake Tahoe','California',102,'2014-09-08 05:22:32'),(13,'NA','NA',102,'2014-09-08 05:22:35'),(14,'NA','NA',102,'2014-09-08 05:22:37'),(15,'NA','NA',102,'2014-09-08 05:22:38'),(16,'None','None',102,'2014-09-08 05:22:42'),(17,'San Francisco','CA',102,'2014-09-08 05:22:45'),(18,'Lebanon','NH',102,'2014-09-08 05:22:46'),(19,'San Francisco','CA',102,'2014-09-08 05:22:48'),(20,'Palo Alto','CA',102,'2014-09-08 05:22:51');
/*!40000 ALTER TABLE `strava_ids` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-09-07 22:39:37
