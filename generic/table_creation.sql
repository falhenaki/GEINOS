-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: bitforcedev.se.rit.edu    Database: se_project
-- ------------------------------------------------------
-- Server version	5.5.60-0ubuntu0.14.04.1-log

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
-- Table structure for table `Device_Groups`
--

DROP TABLE IF EXISTS `Device_Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Device_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `last_modified` datetime NOT NULL,
  `template_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`device_group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Device_Groups`
--

LOCK TABLES `Device_Groups` WRITE;
/*!40000 ALTER TABLE `Device_Groups` DISABLE KEYS */;
INSERT INTO `Device_Groups` VALUES ('Doug_Test_Group','2018-04-25 12:59:29','a_new_hope.xml');
/*!40000 ALTER TABLE `Device_Groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Devices`
--

DROP TABLE IF EXISTS `Devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Devices` (
  `vendor_id` varchar(20) NOT NULL DEFAULT '',
  `serial_number` varchar(20) NOT NULL DEFAULT '',
  `model_number` varchar(50) NOT NULL DEFAULT '',
  `device_status` enum('UNAUTHORIZED','AUTHORIZED','PROVISIONED') NOT NULL DEFAULT 'UNAUTHORIZED',
  `last_modified` datetime NOT NULL,
  `IP` varchar(39) NOT NULL DEFAULT '',
  `config_file` varchar(50) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`vendor_id`,`serial_number`,`model_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Devices`
--

LOCK TABLES `Devices` WRITE;
/*!40000 ALTER TABLE `Devices` DISABLE KEYS */;
INSERT INTO `Devices` VALUES ('Doug_Test','123123','MDS Orbit ECR','UNAUTHORIZED','2018-04-25 12:58:59','1.1.1.1',NULL,NULL,NULL);
/*!40000 ALTER TABLE `Devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Devices_in_Groups`
--

DROP TABLE IF EXISTS `Devices_in_Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Devices_in_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `vendor_id` varchar(20) NOT NULL DEFAULT '',
  `serial_number` varchar(20) NOT NULL DEFAULT '',
  `model_number` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`device_group_name`,`vendor_id`,`serial_number`,`model_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Devices_in_Groups`
--

LOCK TABLES `Devices_in_Groups` WRITE;
/*!40000 ALTER TABLE `Devices_in_Groups` DISABLE KEYS */;
INSERT INTO `Devices_in_Groups` VALUES ('csdfsdfasd','Test','12345','MDS Orbit ECR'),('Demo_Group','Test','12345','MDS Orbit ECR'),('Doug_Test_Group','Doug_Test','123123','MDS Orbit ECR'),('Doug_Test_Group','Test','12345','MDS Orbit ECR'),('grp2','123','4311','4321'),('grp2','22','456','777'),('grp2','49','50','51'),('grp2','50','50','44'),('MondayDemoGroup','MondayDemoDevice','123456','MDS Orbit MCR'),('whaever','0','12345','0');
/*!40000 ALTER TABLE `Devices_in_Groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ListParameters`
--

DROP TABLE IF EXISTS `ListParameters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ListParameters` (
  `param_name` varchar(50) NOT NULL,
  `param_value` varchar(50) NOT NULL,
  PRIMARY KEY (`param_name`,`param_value`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ListParameters`
--

LOCK TABLES `ListParameters` WRITE;
/*!40000 ALTER TABLE `ListParameters` DISABLE KEYS */;
/*!40000 ALTER TABLE `ListParameters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Logs`
--

DROP TABLE IF EXISTS `Logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Logs` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type` tinyint(4) DEFAULT NULL,
  `log_message` varchar(100) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `role` enum('ADMIN','OPERATOR') DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Logs`
--

LOCK TABLES `Logs` WRITE;
/*!40000 ALTER TABLE `Logs` DISABLE KEYS */;
INSERT INTO `Logs` VALUES (1,1,'whatever dude','User1','OPERATOR','0000-00-00 00:00:00'),(2,1,'User added','test','ADMIN','2018-04-23 12:10:15'),(3,1,'User added','test','ADMIN','2018-04-23 17:10:01'),(4,1,'User added','test','ADMIN','2018-04-23 17:11:19');
/*!40000 ALTER TABLE `Logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Parameters`
--

DROP TABLE IF EXISTS `Parameters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Parameters` (
  `param_name` varchar(50) NOT NULL,
  `start_value` varchar(50) DEFAULT NULL,
  `end_value` varchar(50) DEFAULT NULL,
  `param_type` enum('RANGE','SCALAR','LIST') DEFAULT 'SCALAR',
  `date_created` datetime DEFAULT NULL,
  `current_offset` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`param_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Parameters`
--

LOCK TABLES `Parameters` WRITE;
/*!40000 ALTER TABLE `Parameters` DISABLE KEYS */;
INSERT INTO `Parameters` VALUES ('Some_Random_Thing','1.2.3.4','','SCALAR',NULL,'1.2.3.4');
/*!40000 ALTER TABLE `Parameters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Templates`
--

DROP TABLE IF EXISTS `Templates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Templates` (
  `name` varchar(100) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `template_file` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Templates`
--

LOCK TABLES `Templates` WRITE;
/*!40000 ALTER TABLE `Templates` DISABLE KEYS */;
INSERT INTO `Templates` VALUES ('a_new_hope.xml','2018-04-25 13:01:21','/Users/Alaina/PycharmProjects/Genios_Demo/GEINOS/g'),('some_template.xml','2018-04-25 13:16:34','/Users/Alaina/PycharmProjects/Genios_Demo/GEINOS/g');
/*!40000 ALTER TABLE `Templates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User_Groups`
--

DROP TABLE IF EXISTS `User_Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User_Groups` (
  `role_type` enum('ADMIN','OPERATOR') NOT NULL DEFAULT 'OPERATOR',
  `group_name` varchar(50) NOT NULL,
  PRIMARY KEY (`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User_Groups`
--

LOCK TABLES `User_Groups` WRITE;
/*!40000 ALTER TABLE `User_Groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `User_Groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `passwordhash` varchar(128) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `role_type` enum('ADMIN','OPERATOR') NOT NULL DEFAULT 'OPERATOR',
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (20,'fawaz','pbkdf2:sha256:50000$RSCHY9x8$1280f9da4961bf6a5ba923bfd1b17b2f6961504c988976ff4f12dc95d92af08c','2018-03-17 23:10:15','ADMIN',NULL),(27,'fawaz','pbkdf2:sha256:50000$XHVrxcOi$d1004a79410f9a31e9d5549ab55721f61c29e2e8ef84a1c98ae7159742483117',NULL,'ADMIN',NULL),(36,'puttest','pbkdf2:sha256:50000$vq8OKcy3$1da72f92feac6d5dabd416a9607a75bbe6918049cafd596f5ee13c6c4755e691',NULL,'OPERATOR',NULL),(37,'test','pbkdf2:sha256:50000$RYygkMH7$54e38ec22dfaa9fac5bb9a4985bb017796e6da81041ffb85759c51c118050b20','2018-04-25 12:37:29','ADMIN',NULL),(39,'Admin','pbkdf2:sha256:50000$NEtNHIF0$09666884db42b06e7862e36a0405a32593dd73d0c94bd595d3233ab6a498348b',NULL,'ADMIN',NULL),(43,'Qasim','pbkdf2:sha256:50000$5vauTVFJ$41fe3f6c7e57265d06d3334c61d8f9c745533ec38988787c8c3e72a471416314',NULL,'ADMIN',NULL),(44,'sample','pbkdf2:sha256:50000$fxerBkZA$b267344af4b985798f514e32c1d54b244acc028902ee5f69fe032ebdbefa7c31',NULL,'ADMIN',NULL),(46,'abcd','pbkdf2:sha256:50000$Jwj949ze$46fce4ace1c91a7fa81a071651eca83b10aad84b91cb27be4d431e25fad4f199',NULL,'ADMIN',NULL);
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users_in_Groups`
--

DROP TABLE IF EXISTS `Users_in_Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users_in_Groups` (
  `group_name` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users_in_Groups`
--

LOCK TABLES `Users_in_Groups` WRITE;
/*!40000 ALTER TABLE `Users_in_Groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `Users_in_Groups` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-25 13:18:45
