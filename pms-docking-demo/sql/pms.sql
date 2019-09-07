-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
-- 首先创建PMS数据库，然后执行sql脚本导入数据：
-- CREATE DATABASE `PMS` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- use PMS;
-- source pms.sql;
-- 导入完整PMS菜单资源、对接应用(APP_ID=2)的测试数据(应用资源、菜单资源)
-- 用户：admin/admin test/test
-- Host: localhost    Database: PMS
-- ------------------------------------------------------
-- Server version	5.7.25

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
-- Table structure for table `application`
--

DROP TABLE IF EXISTS `application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(80) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_name` (`app_name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `application`
--

LOCK TABLES `application` WRITE;
/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (1,'PMS','权限统一管理系统'),(2,'DEMO','测试');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group`
--

DROP TABLE IF EXISTS `group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_name` varchar(80) DEFAULT NULL,
  `remark` varchar(80) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  `perm_menu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_id` (`app_id`),
  KEY `perm_menu_id` (`perm_menu_id`),
  CONSTRAINT `group_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `application` (`id`) ON DELETE CASCADE,
  CONSTRAINT `group_ibfk_2` FOREIGN KEY (`perm_menu_id`) REFERENCES `perm_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group`
--

LOCK TABLES `group` WRITE;
/*!40000 ALTER TABLE `group` DISABLE KEYS */;
INSERT INTO `group` VALUES (1,'tester','测试',2,1),(2,'tester','访客',1,2);
/*!40000 ALTER TABLE `group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `group_permission`
--

DROP TABLE IF EXISTS `group_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `group_permission` (
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`,`permission_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `group_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`),
  CONSTRAINT `group_permission_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `group_permission`
--

LOCK TABLES `group_permission` WRITE;
/*!40000 ALTER TABLE `group_permission` DISABLE KEYS */;
INSERT INTO `group_permission` VALUES (1,1),(1,2);
/*!40000 ALTER TABLE `group_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `perm_menu`
--

DROP TABLE IF EXISTS `perm_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `perm_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `p_menu_name` varchar(80) DEFAULT NULL,
  `checked_keys` json DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  `res_menu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_customer_uc_2` (`app_id`,`p_menu_name`),
  KEY `res_menu_id` (`res_menu_id`),
  CONSTRAINT `perm_menu_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `application` (`id`),
  CONSTRAINT `perm_menu_ibfk_2` FOREIGN KEY (`res_menu_id`) REFERENCES `res_menu` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `perm_menu`
--

LOCK TABLES `perm_menu` WRITE;
/*!40000 ALTER TABLE `perm_menu` DISABLE KEYS */;
INSERT INTO `perm_menu` VALUES (1,'DEMO','[1567703702693, 1567703962546]','测试',2,2),(2,'访客菜单','[1567780912116]','PMS访客菜单',1,1);
/*!40000 ALTER TABLE `perm_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_name` varchar(80) DEFAULT NULL,
  `action` int(11) DEFAULT NULL,
  `remark` varchar(80) DEFAULT NULL,
  `app_id` int(11) DEFAULT NULL,
  `resource_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_id` (`app_id`),
  KEY `resource_id` (`resource_id`),
  CONSTRAINT `permission_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `application` (`id`),
  CONSTRAINT `permission_ibfk_2` FOREIGN KEY (`resource_id`) REFERENCES `resource` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,'按钮-0b0',0,'DEMO-按钮-element-DISABLE',2,2),(2,'test-0b11',3,'DEMO-test-url-GET-POST',2,1);
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `res_menu`
--

DROP TABLE IF EXISTS `res_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `res_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `r_menu_data` json DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_id` (`app_id`),
  CONSTRAINT `res_menu_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `application` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `res_menu`
--

LOCK TABLES `res_menu` WRITE;
/*!40000 ALTER TABLE `res_menu` DISABLE KEYS */;
INSERT INTO `res_menu` VALUES (1,1,'[{\"id\": 1567591557542, \"meta\": {\"icon\": \"table\", \"name\": \"PMS\", \"path\": \"/pms\", \"title\": \"PMS\", \"hidden\": \"\", \"redirect\": \"/pms/resource/application\", \"component\": \"Layout\"}, \"label\": \"PMS\", \"isEdit\": false}, {\"id\": 1567591774754, \"pid\": 1567591557542, \"meta\": {\"icon\": \"table\", \"name\": \"Resource\", \"path\": \"resource\", \"title\": \"资源管理\", \"hidden\": \"\", \"redirect\": \"/pms/resource/application\", \"component\": \"/pms/resource/index.vue\"}, \"label\": \"资源管理\", \"isEdit\": false}, {\"id\": 1567780608379, \"pid\": 1567591557542, \"meta\": {\"icon\": \"table\", \"name\": \"Permission\", \"path\": \"permission\", \"title\": \"权限管理\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/pms/permission/index.vue\"}, \"label\": \"权限管理\", \"isEdit\": false}, {\"id\": 1567780912116, \"pid\": 1567591557542, \"meta\": {\"icon\": \"table\", \"name\": \"Group\", \"path\": \"group\", \"title\": \"组织管理\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/pms/organization/index.vue\"}, \"label\": \"组织管理\", \"isEdit\": false}, {\"id\": 1567591833989, \"pid\": 1567591774754, \"meta\": {\"icon\": \"table\", \"name\": \"Application\", \"path\": \"application\", \"title\": \"应用系统\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/pms/resource/application/index.vue\"}, \"label\": \"应用系统\", \"isEdit\": false}, {\"id\": 1567592849807, \"pid\": 1567591774754, \"meta\": {\"icon\": \"table\", \"name\": \"AppResource\", \"path\": \"app_resource\", \"title\": \"应用资源\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/pms/resource/appResource/index.vue\"}, \"label\": \"应用资源\", \"isEdit\": false}, {\"id\": 1567593004361, \"pid\": 1567591774754, \"meta\": {\"icon\": \"table\", \"name\": \"Menu\", \"path\": \"menu\", \"title\": \"应用菜单\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/pms/resource/menu/index.vue\"}, \"label\": \"应用菜单\", \"isEdit\": false}, {\"id\": 1567780723652, \"pid\": 1567780608379, \"meta\": {\"icon\": \"table\", \"name\": \"ResourcePermission\", \"path\": \"resource\", \"title\": \"资源权限\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/pms/permission/resource/index.vue\"}, \"label\": \"资源权限\", \"isEdit\": false}, {\"id\": 1567780836760, \"pid\": 1567780608379, \"meta\": {\"icon\": \"table\", \"name\": \"MenuPermission\", \"path\": \"menu\", \"title\": \"菜单权限\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/pms/permission/menu/index.vue\"}, \"label\": \"菜单权限\", \"isEdit\": false}]','pms菜单'),(2,2,'[{\"id\": 1567703702693, \"meta\": {\"icon\": \"table\", \"name\": \"TEST\", \"path\": \"/test\", \"title\": \"测试\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"Layout\"}, \"label\": \"测试\", \"isEdit\": false}, {\"id\": 1567703962546, \"pid\": 1567703702693, \"meta\": {\"icon\": \"table\", \"name\": \"PAGE\", \"path\": \"page\", \"title\": \"页面\", \"hidden\": \"\", \"redirect\": \"\", \"component\": \"/test/index.vue\"}, \"label\": \"test\", \"isEdit\": false}]','测试菜单');
/*!40000 ALTER TABLE `res_menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resource`
--

DROP TABLE IF EXISTS `resource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `resource_name` varchar(80) DEFAULT NULL,
  `resource_type` enum('url','element','data') DEFAULT NULL,
  `resource_code` json DEFAULT NULL,
  `remark` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_customer_uc_1` (`app_id`,`resource_name`),
  CONSTRAINT `resource_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `application` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resource`
--

LOCK TABLES `resource` WRITE;
/*!40000 ALTER TABLE `resource` DISABLE KEYS */;
INSERT INTO `resource` VALUES (1,2,'test','url','{\"url\": \"/v1/test/\"}','测试url资源'),(2,2,'按钮','element','{\"element\": \"btn\"}','测试页面元素');
/*!40000 ALTER TABLE `resource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'admin','2019-09-07 09:57:44'),(2,'test','2019-09-07 10:04:32');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_group`
--

DROP TABLE IF EXISTS `user_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_group` (
  `group_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`,`user_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_group_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `group` (`id`),
  CONSTRAINT `user_group_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_group`
--

LOCK TABLES `user_group` WRITE;
/*!40000 ALTER TABLE `user_group` DISABLE KEYS */;
INSERT INTO `user_group` VALUES (1,2),(2,2);
/*!40000 ALTER TABLE `user_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `code` varchar(80) DEFAULT NULL,
  `username` varchar(80) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'0001','admin','$6$rounds=656000$mcRTm4CcnznUN4G3$ffKSLNPY9MNJLFG7uZk47mcVaZazKnzAHLBGUOj71oRcXgC0E6BAhOQ.LBTIG4u8qt1yPrgWxC0oVQvGw9jbE1',1,'2019-09-07 09:57:44'),(2,'0002','test','$6$rounds=656000$yeUqZQi/VSy9r3lj$cSm793ukC0rDTM4fCSVnMEvA6VK.8Sc/BSPTqlM7aTYsbCeAM8MmeZe8wP5r7gekM004qDysMd8zPLdwKZqMl.',2,'2019-09-07 10:04:32');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'PMS'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-09-07 10:30:50
