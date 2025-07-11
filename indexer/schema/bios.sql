-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: bios_mainnet
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_whitelist`
--

DROP TABLE IF EXISTS `account_whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_whitelist` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `permitted` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `arrival_rewards`
--

DROP TABLE IF EXISTS `arrival_rewards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arrival_rewards` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `asteroid_id` int NOT NULL,
  `redeemed` tinyint DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `art_grabs`
--

DROP TABLE IF EXISTS `art_grabs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `art_grabs` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `asset_type` tinyint NOT NULL,
  `asset_id` int NOT NULL,
  `status` tinyint NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_bridged_from_l1`
--

DROP TABLE IF EXISTS `asteroid_bridged_from_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_bridged_from_l1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_bridged_from_l1_txns`
--

DROP TABLE IF EXISTS `asteroid_bridged_from_l1_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_bridged_from_l1_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_bridged_to_l1`
--

DROP TABLE IF EXISTS `asteroid_bridged_to_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_bridged_to_l1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_bridged_to_l1_txns`
--

DROP TABLE IF EXISTS `asteroid_bridged_to_l1_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_bridged_to_l1_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_metadata_l1`
--

DROP TABLE IF EXISTS `asteroid_metadata_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_metadata_l1` (
  `asteroid_id` int NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `radius` int NOT NULL,
  `spectral_type` tinyint NOT NULL,
  `bonuses` bigint NOT NULL,
  `scan_status` tinyint NOT NULL,
  `purchase_order` int NOT NULL,
  PRIMARY KEY (`asteroid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_transfers`
--

DROP TABLE IF EXISTS `asteroid_transfers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_transfers` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_transfers_txns`
--

DROP TABLE IF EXISTS `asteroid_transfers_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_transfers_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroid_txns_per_block`
--

DROP TABLE IF EXISTS `asteroid_txns_per_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroid_txns_per_block` (
  `block_number` int NOT NULL,
  `txns` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `asteroids`
--

DROP TABLE IF EXISTS `asteroids`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asteroids` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `asteroid_owner` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `asteroid_id` int NOT NULL,
  `random_seed` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `abundances` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `bonuses` bigint DEFAULT NULL,
  `radius` int DEFAULT NULL,
  `spectral_type` int DEFAULT NULL,
  `scan_status` tinyint(1) DEFAULT '0',
  `features` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crew_id` int DEFAULT NULL,
  `initialized` tinyint(1) DEFAULT '0',
  `surface_scan` tinyint(1) DEFAULT '0',
  `resource_scan` tinyint(1) DEFAULT '0',
  `water` int DEFAULT NULL,
  `hydrogen` int DEFAULT NULL,
  `amonia` int DEFAULT NULL,
  `nitrogen` int DEFAULT NULL,
  `sulfur_dioxide` int DEFAULT NULL,
  `carbon_dioxide` int DEFAULT NULL,
  `carbon_monoxide` int DEFAULT NULL,
  `methane` int DEFAULT NULL,
  `apatite` int DEFAULT NULL,
  `bitumen` int DEFAULT NULL,
  `calcite` int DEFAULT NULL,
  `feldspar` int DEFAULT NULL,
  `olivine` int DEFAULT NULL,
  `pyroxene` int DEFAULT NULL,
  `coffinite` int DEFAULT NULL,
  `merrillite` int DEFAULT NULL,
  `xenotime` int DEFAULT NULL,
  `rhadbdite` int DEFAULT NULL,
  `graphite` int DEFAULT NULL,
  `taenite` int DEFAULT NULL,
  `troilite` int DEFAULT NULL,
  `uranite` int DEFAULT NULL,
  `colonization_missions_tracking` tinyint DEFAULT '0',
  PRIMARY KEY (`asteroid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `buildings`
--

DROP TABLE IF EXISTS `buildings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buildings` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `building_label` tinyint NOT NULL,
  `building_id` int NOT NULL,
  `crew_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `building_type` int DEFAULT NULL,
  `lot_id` bigint DEFAULT NULL,
  `grace_period_end` int DEFAULT NULL,
  `finish_time` int DEFAULT NULL,
  `name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint DEFAULT NULL,
  PRIMARY KEY (`building_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `buy_orders`
--

DROP TABLE IF EXISTS `buy_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `buy_orders` (
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `valid_time` int NOT NULL,
  `maker_fee` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking`
--

DROP TABLE IF EXISTS `colonization_missions_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking` (
  `mission_1_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Touchdown',
  `mission_1_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_1_req_1_crew_id` int DEFAULT NULL,
  `mission_1_req_1_goal` tinyint DEFAULT '1',
  `mission_1_req_1` tinyint DEFAULT '0',
  `mission_1_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_1_req_2_crew_id` int DEFAULT NULL,
  `mission_1_req_2_goal` tinyint DEFAULT '1',
  `mission_1_req_2` tinyint DEFAULT '0',
  `mission_2_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Below the Surface',
  `mission_2_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_2_req_1_crew_id` int DEFAULT NULL,
  `mission_2_req_1_goal` tinyint DEFAULT '1',
  `mission_2_req_1` tinyint DEFAULT '0',
  `mission_2_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_2_req_2_crew_id` int DEFAULT NULL,
  `mission_2_req_2_goal` int DEFAULT '0',
  `mission_2_req_2` int DEFAULT '10000000',
  `mission_3_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Pack it Up',
  `mission_3_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_3_req_1_crew_id` int DEFAULT NULL,
  `mission_3_req_1_goal` tinyint DEFAULT '1',
  `mission_3_req_1` tinyint DEFAULT '0',
  `mission_3_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_3_req_2_crew_id` int DEFAULT NULL,
  `mission_3_req_2_goal` tinyint DEFAULT '3',
  `mission_3_req_2` tinyint DEFAULT '0',
  `mission_4_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Refined Taste',
  `mission_4_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_4_req_1_crew_id` int DEFAULT NULL,
  `mission_4_req_1_goal` int DEFAULT '1',
  `mission_4_req_1` int DEFAULT '0',
  `mission_4_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_4_req_2_crew_id` int DEFAULT NULL,
  `mission_4_req_2_goal` tinyint DEFAULT '1',
  `mission_4_req_2` tinyint DEFAULT '0',
  `mission_5_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Industrial Revolution',
  `mission_5_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_5_req_1_crew_id` int DEFAULT NULL,
  `mission_5_req_1_goal` tinyint DEFAULT '1',
  `mission_5_req_1` tinyint DEFAULT '0',
  `mission_5_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_5_req_2_crew_id` int DEFAULT NULL,
  `mission_5_req_2_goal` tinyint DEFAULT '1',
  `mission_5_req_2` tinyint DEFAULT '0',
  `mission_6_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'PoTAYto / PoTAHto',
  `mission_6_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_6_req_1_crew_id` int DEFAULT NULL,
  `mission_6_req_1_goal` tinyint DEFAULT '1',
  `mission_6_req_1` tinyint DEFAULT '0',
  `mission_6_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_6_req_2_crew_id` int DEFAULT NULL,
  `mission_6_req_2_goal` tinyint DEFAULT '1',
  `mission_6_req_2` tinyint DEFAULT '0',
  `mission_7_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Expansion and Exploration',
  `mission_7_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_7_req_1_crew_id` int DEFAULT NULL,
  `mission_7_req_1_goal` tinyint DEFAULT '1',
  `mission_7_req_1` tinyint DEFAULT '0',
  `mission_7_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_7_req_2_crew_id` int DEFAULT NULL,
  `mission_7_req_2_goal` tinyint DEFAULT '1',
  `mission_7_req_2` tinyint DEFAULT '0',
  `mission_8_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Port City',
  `mission_8_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_8_req_1_crew_id` int DEFAULT NULL,
  `mission_8_req_1_goal` tinyint DEFAULT '1',
  `mission_8_req_1` tinyint DEFAULT '0',
  `mission_8_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_8_req_2_crew_id` int DEFAULT NULL,
  `mission_8_req_2_goal` tinyint DEFAULT '1',
  `mission_8_req_2` tinyint DEFAULT '0',
  `mission_9_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Open for Business',
  `mission_9_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_9_req_1_crew_id` int DEFAULT NULL,
  `mission_9_req_1_goal` tinyint DEFAULT '1',
  `mission_9_req_1` tinyint DEFAULT '0',
  `mission_9_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_9_req_2_crew_id` int DEFAULT NULL,
  `mission_9_req_2_goal` int DEFAULT '10',
  `mission_9_req_2` int DEFAULT '0',
  `mission_10_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Homesteading',
  `mission_10_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_10_req_1_crew_id` int DEFAULT NULL,
  `mission_10_req_1_goal` tinyint DEFAULT '1',
  `mission_10_req_1` tinyint DEFAULT '0',
  `mission_10_req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_10_req_2_crew_id` int DEFAULT NULL,
  `mission_10_req_2_goal` tinyint DEFAULT '5',
  `mission_10_req_2` tinyint DEFAULT '0',
  `mission_11_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'We Built this City',
  `mission_11_req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `mission_11_req_1_crew_id` int DEFAULT NULL,
  `mission_11_req_1_goal` tinyint DEFAULT '9',
  `mission_11_req_1` tinyint DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_1`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_1` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Touchdown',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` tinyint DEFAULT '1',
  `req_2` tinyint DEFAULT '0',
  `req_2_ship_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_10`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_10`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_10` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Homesteading',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` int DEFAULT '5',
  `req_2` int DEFAULT '0',
  `req_2_habitat_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_11`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_11`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_11` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'We Built this City',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_timestamp` timestamp NULL DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '9',
  `req_1` tinyint DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_2`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_2` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Below the Surface',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` int DEFAULT '2000000',
  `req_2` int DEFAULT '0',
  `req_2_extractor_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_3`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_3`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_3` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Pack it Up',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` int DEFAULT '3',
  `req_2` int DEFAULT '0',
  `req_2_warehouse_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_4`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_4`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_4` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Refined Taste',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` int DEFAULT '1',
  `req_2` int DEFAULT '0',
  `req_2_refinery_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_5`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_5`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_5` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Industrial Revolution',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` int DEFAULT '1',
  `req_2` int DEFAULT '0',
  `req_2_factory_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_6`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_6`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_6` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'PoTAYto / PoTAHto',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` int DEFAULT '75600',
  `req_2` int DEFAULT '0',
  `req_2_bioreactor_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_7`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_7`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_7` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Expansion and Exploration',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` tinyint DEFAULT '1',
  `req_2` int DEFAULT '0',
  `req_2_shipyard_id` int DEFAULT NULL,
  `req_2_ship_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_8`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_8`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_8` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Port City',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` tinyint DEFAULT '1',
  `req_2` int DEFAULT '0',
  `req_2_spaceport_id` int DEFAULT NULL,
  `req_2_ship_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `colonization_missions_tracking_9`
--

DROP TABLE IF EXISTS `colonization_missions_tracking_9`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colonization_missions_tracking_9` (
  `asteroid_id` int DEFAULT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Open for Business',
  `req_1_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_crew_id` int DEFAULT NULL,
  `req_1_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_1_goal` tinyint DEFAULT '1',
  `req_1` tinyint DEFAULT '0',
  `req_1_building_id` int DEFAULT '0',
  `req_2_wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_crew_id` int DEFAULT NULL,
  `req_2_goal` int DEFAULT '10',
  `req_2` int DEFAULT '0',
  `req_2_exchange_id` int DEFAULT NULL,
  `req_2_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `req_2_timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `community_missions_summary`
--

DROP TABLE IF EXISTS `community_missions_summary`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `community_missions_summary` (
  `mission_id` int NOT NULL,
  `mission_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mission_description` varchar(160) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mission_required` int DEFAULT '0',
  `mission_cap` int DEFAULT '0',
  `mission_actual` int DEFAULT '0',
  `mission_crews` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `community_missions_tracking`
--

DROP TABLE IF EXISTS `community_missions_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `community_missions_tracking` (
  `wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `mission_1_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Romulus, Remus, and the Rest',
  `mission_1_required` int DEFAULT '7000',
  `mission_1_actual` int DEFAULT '0',
  `mission_1_wallet_amount` int DEFAULT '0',
  `mission_1_wallet_status` tinyint DEFAULT '0',
  `mission_1_asteroid_id` int DEFAULT '0',
  `mission_2_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Learn by Doing',
  `mission_2_required` int DEFAULT '6000',
  `mission_2_actual` int DEFAULT '0',
  `mission_2_wallet_amount` int DEFAULT '0',
  `mission_2_wallet_status` tinyint DEFAULT '0',
  `mission_3_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Four Pillars',
  `mission_3_required` int DEFAULT '3000',
  `mission_3_actual` int DEFAULT '0',
  `mission_3_wallet_amount` int DEFAULT '0',
  `mission_3_wallet_status` tinyint DEFAULT '0',
  `mission_4_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Together, We Can Rise',
  `mission_4_required` int DEFAULT '400',
  `mission_4_actual` int DEFAULT '0',
  `mission_4_wallet_amount` int DEFAULT '0',
  `mission_4_wallet_status` tinyint DEFAULT '0',
  `mission_5_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'The Fleet',
  `mission_5_required` int DEFAULT '300',
  `mission_5_actual` int DEFAULT '0',
  `mission_5_wallet_amount` int DEFAULT '0',
  `mission_5_wallet_status` tinyint DEFAULT '0',
  `mission_6_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Rock Breaker',
  `mission_6_required` int DEFAULT '12000000',
  `mission_6_actual` int DEFAULT '0',
  `mission_6_wallet_amount` int DEFAULT '0',
  `mission_6_wallet_status` tinyint DEFAULT '0',
  `mission_7_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Prospecting Pays Off',
  `mission_7_required` int DEFAULT '15000',
  `mission_7_actual` int DEFAULT '0',
  `mission_7_wallet_amount` int DEFAULT '0',
  `mission_7_wallet_status` tinyint DEFAULT '0',
  `mission_8_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Potluck',
  `mission_8_required` int DEFAULT '20000',
  `mission_8_actual` int DEFAULT '0',
  `mission_8_wallet_amount` int DEFAULT '0',
  `mission_8_wallet_status` tinyint DEFAULT '0',
  PRIMARY KEY (`crew_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `configured_exchanges`
--

DROP TABLE IF EXISTS `configured_exchanges`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `configured_exchanges` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `exchange_label` tinyint DEFAULT NULL,
  `exchange_id` bigint DEFAULT NULL,
  `exchange_type` tinyint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` bigint DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `constants`
--

DROP TABLE IF EXISTS `constants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `constants` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `construction`
--

DROP TABLE IF EXISTS `construction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `construction` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_block_number` int NOT NULL,
  `start_timestamp` timestamp NOT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `building_label` tinyint NOT NULL,
  `building_type` tinyint NOT NULL,
  `building_id` bigint NOT NULL,
  `lot_id` int DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `finish_time` int DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint NOT NULL,
  KEY `construction_multi_one` (`building_type`,`building_id`,`asteroid_id`),
  KEY `construction_multi_two` (`asteroid_id`,`status`),
  KEY `construction_building` (`building_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contract_agreements`
--

DROP TABLE IF EXISTS `contract_agreements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contract_agreements` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `permission` tinyint DEFAULT NULL,
  `permitted_label` tinyint NOT NULL,
  `permitted_id` int NOT NULL,
  `contract_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contract_policies`
--

DROP TABLE IF EXISTS `contract_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contract_policies` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `contract` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contracts`
--

DROP TABLE IF EXISTS `contracts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contracts` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `contract` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_samples`
--

DROP TABLE IF EXISTS `core_samples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_samples` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_block_number` int NOT NULL,
  `start_timestamp` timestamp NOT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `deposit_id` bigint NOT NULL,
  `lot_id` int NOT NULL,
  `packed_lot_id` bigint NOT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL,
  `finish_time` int NOT NULL,
  `improving` tinyint DEFAULT NULL,
  `initial_yield` bigint DEFAULT '0',
  `origin_label` tinyint DEFAULT NULL,
  `origin_id` int DEFAULT NULL,
  `origin_slot` int DEFAULT NULL,
  `for_sale` tinyint DEFAULT '0',
  `price` bigint DEFAULT NULL,
  `buyer_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `buyer_crew_id` int DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  PRIMARY KEY (`deposit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `core_samples_depleted`
--

DROP TABLE IF EXISTS `core_samples_depleted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_samples_depleted` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `deposit_id` bigint NOT NULL,
  `lot_id` int NOT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL,
  `finish_time` int NOT NULL,
  `current_yield` int DEFAULT '0',
  `destination_label` tinyint DEFAULT NULL,
  `destination_id` int DEFAULT NULL,
  `destination_slot` int DEFAULT NULL,
  PRIMARY KEY (`deposit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crew_actions`
--

DROP TABLE IF EXISTS `crew_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crew_actions` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crew_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `ship_id` int DEFAULT NULL,
  `action` varchar(65) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crew_composition`
--

DROP TABLE IF EXISTS `crew_composition`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crew_composition` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `crewmate_id` int DEFAULT NULL,
  `crew_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crew_transfers`
--

DROP TABLE IF EXISTS `crew_transfers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crew_transfers` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crew_transfers_txns`
--

DROP TABLE IF EXISTS `crew_transfers_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crew_transfers_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crew_txns_per_block`
--

DROP TABLE IF EXISTS `crew_txns_per_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crew_txns_per_block` (
  `block_number` int NOT NULL,
  `txns` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_actions`
--

DROP TABLE IF EXISTS `crewmate_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_actions` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crew_id` int NOT NULL,
  `crewmate_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `ship_id` int DEFAULT NULL,
  `action` varchar(65) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_bridged_from_l1`
--

DROP TABLE IF EXISTS `crewmate_bridged_from_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_bridged_from_l1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_bridged_from_l1_txns`
--

DROP TABLE IF EXISTS `crewmate_bridged_from_l1_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_bridged_from_l1_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_bridged_to_l1`
--

DROP TABLE IF EXISTS `crewmate_bridged_to_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_bridged_to_l1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_bridged_to_l1_txns`
--

DROP TABLE IF EXISTS `crewmate_bridged_to_l1_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_bridged_to_l1_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_crew_changed`
--

DROP TABLE IF EXISTS `crewmate_crew_changed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_crew_changed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_id` int NOT NULL,
  `crew_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_metadata_l1`
--

DROP TABLE IF EXISTS `crewmate_metadata_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_metadata_l1` (
  `crewmate_id` int NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `collection` int NOT NULL,
  `class` int NOT NULL,
  `title` int NOT NULL,
  PRIMARY KEY (`crewmate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_transfers`
--

DROP TABLE IF EXISTS `crewmate_transfers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_transfers` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_transfers_txns`
--

DROP TABLE IF EXISTS `crewmate_transfers_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_transfers_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmate_txns_per_block`
--

DROP TABLE IF EXISTS `crewmate_txns_per_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmate_txns_per_block` (
  `block_number` int NOT NULL,
  `txns` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crewmates`
--

DROP TABLE IF EXISTS `crewmates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crewmates` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `crewmate_owner` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crewmate_id` int NOT NULL,
  `name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `features` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `collection` tinyint(1) DEFAULT NULL,
  `class` tinyint(1) DEFAULT NULL,
  `title` int DEFAULT NULL,
  `crew_id` int DEFAULT NULL,
  `impactful_1` int DEFAULT NULL,
  `impactful_2` int DEFAULT NULL,
  `impactful_3` int DEFAULT NULL,
  `impactful_4` int DEFAULT NULL,
  `impactful_5` int DEFAULT NULL,
  `impactful_6` int DEFAULT NULL,
  `station_label` tinyint DEFAULT NULL,
  `station_id` bigint DEFAULT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  PRIMARY KEY (`crewmate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `crews`
--

DROP TABLE IF EXISTS `crews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `crews` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `crew_owner` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crew_id` int NOT NULL,
  `station_id` int DEFAULT NULL,
  `station_label` tinyint DEFAULT NULL,
  `name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `delegated_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `solo_missions_tracking` tinyint DEFAULT '0',
  `community_missions_tracking` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`crew_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deliveries`
--

DROP TABLE IF EXISTS `deliveries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveries` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `start_block_number` int DEFAULT NULL,
  `start_timestamp` timestamp NULL DEFAULT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `packaged_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `packaged_block_number` int DEFAULT NULL,
  `packaged_timestamp` timestamp NULL DEFAULT NULL,
  `cancelled_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cancelled_block_number` int DEFAULT NULL,
  `cancelled_timestamp` timestamp NULL DEFAULT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `dest_asteroid_id` int DEFAULT NULL,
  `dest_lot_id` int DEFAULT NULL,
  `delivery_id` bigint NOT NULL,
  `finish_time` int DEFAULT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL,
  `burned_inventory` tinyint DEFAULT '0',
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint NOT NULL,
  KEY `delivery_id_idx` (`delivery_id`),
  KEY `deliveries_select_multi` (`dest_asteroid_id`,`dest_label`,`dest_type`,`product_id`,`finish_txn_id`),
  KEY `deliveries_multi_two` (`dest_asteroid_id`,`dest_lot_id`,`burned_inventory`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `deliveries_pending`
--

DROP TABLE IF EXISTS `deliveries_pending`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `deliveries_pending` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `dest_asteroid_id` int DEFAULT NULL,
  `dest_lot_id` int DEFAULT NULL,
  `delivery_id` bigint NOT NULL,
  `finish_time` int DEFAULT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_added_account_to_whitelist`
--

DROP TABLE IF EXISTS `dispatcher_added_account_to_whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_added_account_to_whitelist` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `permitted` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_added_to_whitelist`
--

DROP TABLE IF EXISTS `dispatcher_added_to_whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_added_to_whitelist` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `target_label` tinyint DEFAULT NULL,
  `target_id` bigint DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_added_to_whitelist_v1`
--

DROP TABLE IF EXISTS `dispatcher_added_to_whitelist_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_added_to_whitelist_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `permitted_label` tinyint DEFAULT NULL,
  `permitted_id` bigint DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_arrival_reward_claim`
--

DROP TABLE IF EXISTS `dispatcher_arrival_reward_claim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_arrival_reward_claim` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_asteroid_initialized`
--

DROP TABLE IF EXISTS `dispatcher_asteroid_initialized`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_asteroid_initialized` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_asteroid_managed`
--

DROP TABLE IF EXISTS `dispatcher_asteroid_managed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_asteroid_managed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_asteroid_purchased`
--

DROP TABLE IF EXISTS `dispatcher_asteroid_purchased`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_asteroid_purchased` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_building_repossessed`
--

DROP TABLE IF EXISTS `dispatcher_building_repossessed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_building_repossessed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `building_label` tinyint NOT NULL,
  `building_id` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_buy_order_cancelled`
--

DROP TABLE IF EXISTS `dispatcher_buy_order_cancelled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_buy_order_cancelled` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `storage_label` tinyint NOT NULL,
  `storage_id` int NOT NULL,
  `storage_slot` tinyint NOT NULL,
  `storage_type` tinyint NOT NULL,
  `storage_asteroid_id` int DEFAULT NULL,
  `storage_lot_id` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_buy_order_created`
--

DROP TABLE IF EXISTS `dispatcher_buy_order_created`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_buy_order_created` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `storage_label` tinyint NOT NULL,
  `storage_id` int NOT NULL,
  `storage_slot` tinyint NOT NULL,
  `storage_type` tinyint NOT NULL,
  `storage_asteroid_id` int DEFAULT NULL,
  `storage_lot_id` int DEFAULT NULL,
  `valid_time` int NOT NULL,
  `maker_fee` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_buy_order_filled`
--

DROP TABLE IF EXISTS `dispatcher_buy_order_filled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_buy_order_filled` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `buyer_crew_id` int NOT NULL,
  `buyer_crew_label` tinyint NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `storage_label` tinyint NOT NULL,
  `storage_id` int NOT NULL,
  `storage_slot` tinyint NOT NULL,
  `storage_type` tinyint NOT NULL,
  `storage_asteroid_id` int DEFAULT NULL,
  `storage_lot_id` int DEFAULT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` int NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `market_order` tinyint DEFAULT NULL,
  `limit_order` tinyint DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_constant_registered`
--

DROP TABLE IF EXISTS `dispatcher_constant_registered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_constant_registered` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` varchar(156) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_construction_abandoned`
--

DROP TABLE IF EXISTS `dispatcher_construction_abandoned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_construction_abandoned` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `building_label` int NOT NULL,
  `building_id` int NOT NULL,
  `finish_time` int DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_construction_deconstructed`
--

DROP TABLE IF EXISTS `dispatcher_construction_deconstructed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_construction_deconstructed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `building_label` tinyint NOT NULL,
  `building_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_construction_finished`
--

DROP TABLE IF EXISTS `dispatcher_construction_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_construction_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `building_label` tinyint NOT NULL,
  `building_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_construction_planned`
--

DROP TABLE IF EXISTS `dispatcher_construction_planned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_construction_planned` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `building_label` int NOT NULL,
  `building_id` int NOT NULL,
  `lot_label` int NOT NULL,
  `lot_id` int NOT NULL,
  `packed_lot_id` bigint NOT NULL,
  `building_type` int NOT NULL,
  `grace_period_end` int DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_construction_started`
--

DROP TABLE IF EXISTS `dispatcher_construction_started`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_construction_started` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `building_label` int NOT NULL,
  `building_id` int NOT NULL,
  `finish_time` int DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `last_updated` timestamp NULL DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_contract_agreement_accepted`
--

DROP TABLE IF EXISTS `dispatcher_contract_agreement_accepted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_contract_agreement_accepted` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `permission` tinyint DEFAULT NULL,
  `permitted_label` tinyint NOT NULL,
  `permitted_id` int NOT NULL,
  `contract_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_contract_policy_assigned`
--

DROP TABLE IF EXISTS `dispatcher_contract_policy_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_contract_policy_assigned` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `contract` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_contract_policy_removed`
--

DROP TABLE IF EXISTS `dispatcher_contract_policy_removed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_contract_policy_removed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_contract_registered`
--

DROP TABLE IF EXISTS `dispatcher_contract_registered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_contract_registered` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `contract` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crew_delegated`
--

DROP TABLE IF EXISTS `dispatcher_crew_delegated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crew_delegated` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `delegated_to` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crew_ejected`
--

DROP TABLE IF EXISTS `dispatcher_crew_ejected`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crew_ejected` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ejected_crew_label` tinyint NOT NULL,
  `ejected_crew_id` int NOT NULL,
  `finish_time` int NOT NULL,
  `station_label` int NOT NULL,
  `station_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crew_formed`
--

DROP TABLE IF EXISTS `dispatcher_crew_formed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crew_formed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `crewmate_1` int DEFAULT NULL,
  `crewmate_2` int DEFAULT NULL,
  `crewmate_3` int DEFAULT NULL,
  `crewmate_4` int DEFAULT NULL,
  `crewmate_5` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crew_stationed`
--

DROP TABLE IF EXISTS `dispatcher_crew_stationed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crew_stationed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `station_label` tinyint NOT NULL,
  `station_id` bigint NOT NULL,
  `finish_time` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crew_stationed_v1`
--

DROP TABLE IF EXISTS `dispatcher_crew_stationed_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crew_stationed_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_station_label` tinyint NOT NULL,
  `origin_station_id` bigint NOT NULL,
  `destination_station_label` tinyint NOT NULL,
  `destination_station_id` bigint NOT NULL,
  `finish_time` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crewmate_purchased`
--

DROP TABLE IF EXISTS `dispatcher_crewmate_purchased`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crewmate_purchased` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crewmate_label` tinyint NOT NULL,
  `crewmate_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crewmate_recruited`
--

DROP TABLE IF EXISTS `dispatcher_crewmate_recruited`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crewmate_recruited` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `crewmate_label` tinyint NOT NULL,
  `crewmate_id` int NOT NULL,
  `collection` tinyint(1) NOT NULL,
  `class` tinyint(1) NOT NULL,
  `title` int DEFAULT NULL,
  `station_label` tinyint NOT NULL,
  `station_id` int NOT NULL,
  `impactful_1` int DEFAULT NULL,
  `impactful_2` int DEFAULT NULL,
  `impactful_3` int DEFAULT NULL,
  `impactful_4` int DEFAULT NULL,
  `impactful_5` int DEFAULT NULL,
  `impactful_6` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crewmate_recruited_v1`
--

DROP TABLE IF EXISTS `dispatcher_crewmate_recruited_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crewmate_recruited_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `crewmate_label` tinyint NOT NULL,
  `crewmate_id` int NOT NULL,
  `name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `collection` tinyint(1) NOT NULL,
  `class` tinyint(1) NOT NULL,
  `title` int DEFAULT NULL,
  `station_label` tinyint NOT NULL,
  `station_id` int NOT NULL,
  `impactful_1` int DEFAULT NULL,
  `impactful_2` int DEFAULT NULL,
  `impactful_3` int DEFAULT NULL,
  `impactful_4` int DEFAULT NULL,
  `impactful_5` int DEFAULT NULL,
  `impactful_6` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`crewmate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crewmates_arranged_v1`
--

DROP TABLE IF EXISTS `dispatcher_crewmates_arranged_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crewmates_arranged_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `old_crewmate_1` int DEFAULT NULL,
  `old_crewmate_2` int DEFAULT NULL,
  `old_crewmate_3` int DEFAULT NULL,
  `old_crewmate_4` int DEFAULT NULL,
  `old_crewmate_5` int DEFAULT NULL,
  `new_crewmate_1` int DEFAULT NULL,
  `new_crewmate_2` int DEFAULT NULL,
  `new_crewmate_3` int DEFAULT NULL,
  `new_crewmate_4` int DEFAULT NULL,
  `new_crewmate_5` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_crewmates_exchanged`
--

DROP TABLE IF EXISTS `dispatcher_crewmates_exchanged`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_crewmates_exchanged` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew1_label` tinyint NOT NULL,
  `crew1_id` int NOT NULL,
  `crew2_label` tinyint NOT NULL,
  `crew2_id` int NOT NULL,
  `crew1_old_crewmate_1` int DEFAULT NULL,
  `crew1_old_crewmate_2` int DEFAULT NULL,
  `crew1_old_crewmate_3` int DEFAULT NULL,
  `crew1_old_crewmate_4` int DEFAULT NULL,
  `crew1_old_crewmate_5` int DEFAULT NULL,
  `crew1_new_crewmate_1` int DEFAULT NULL,
  `crew1_new_crewmate_2` int DEFAULT NULL,
  `crew1_new_crewmate_3` int DEFAULT NULL,
  `crew1_new_crewmate_4` int DEFAULT NULL,
  `crew1_new_crewmate_5` int DEFAULT NULL,
  `crew2_old_crewmate_1` int DEFAULT NULL,
  `crew2_old_crewmate_2` int DEFAULT NULL,
  `crew2_old_crewmate_3` int DEFAULT NULL,
  `crew2_old_crewmate_4` int DEFAULT NULL,
  `crew2_old_crewmate_5` int DEFAULT NULL,
  `crew2_new_crewmate_1` int DEFAULT NULL,
  `crew2_new_crewmate_2` int DEFAULT NULL,
  `crew2_new_crewmate_3` int DEFAULT NULL,
  `crew2_new_crewmate_4` int DEFAULT NULL,
  `crew2_new_crewmate_5` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_delivery_cancelled`
--

DROP TABLE IF EXISTS `dispatcher_delivery_cancelled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_delivery_cancelled` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_delivery_finished`
--

DROP TABLE IF EXISTS `dispatcher_delivery_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_delivery_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_delivery_finished_v1`
--

DROP TABLE IF EXISTS `dispatcher_delivery_finished_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_delivery_finished_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_delivery_packaged`
--

DROP TABLE IF EXISTS `dispatcher_delivery_packaged`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_delivery_packaged` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_delivery_received`
--

DROP TABLE IF EXISTS `dispatcher_delivery_received`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_delivery_received` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_delivery_sent`
--

DROP TABLE IF EXISTS `dispatcher_delivery_sent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_delivery_sent` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `dest_asteroid_id` int DEFAULT NULL,
  `dest_lot_id` int DEFAULT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `finish_time` int DEFAULT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_delivery_started`
--

DROP TABLE IF EXISTS `dispatcher_delivery_started`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_delivery_started` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `dest_asteroid_id` int DEFAULT NULL,
  `dest_lot_id` int DEFAULT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `finish_time` int DEFAULT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_deposit_listed_for_sale`
--

DROP TABLE IF EXISTS `dispatcher_deposit_listed_for_sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_deposit_listed_for_sale` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` int NOT NULL,
  `price` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_deposit_purchased`
--

DROP TABLE IF EXISTS `dispatcher_deposit_purchased`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_deposit_purchased` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` int NOT NULL,
  `price` bigint NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_deposit_purchased_v1`
--

DROP TABLE IF EXISTS `dispatcher_deposit_purchased_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_deposit_purchased_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `seller_crew_id` int NOT NULL,
  `seller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` int NOT NULL,
  `price` bigint NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_deposit_unlisted_for_sale`
--

DROP TABLE IF EXISTS `dispatcher_deposit_unlisted_for_sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_deposit_unlisted_for_sale` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_emergency_activated`
--

DROP TABLE IF EXISTS `dispatcher_emergency_activated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_emergency_activated` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_emergency_deactivated`
--

DROP TABLE IF EXISTS `dispatcher_emergency_deactivated`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_emergency_deactivated` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_emergency_propellant_collected`
--

DROP TABLE IF EXISTS `dispatcher_emergency_propellant_collected`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_emergency_propellant_collected` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `amount` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_exchange_configured`
--

DROP TABLE IF EXISTS `dispatcher_exchange_configured`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_exchange_configured` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `exchange_label` tinyint DEFAULT NULL,
  `exchange_id` bigint DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_food_supplied`
--

DROP TABLE IF EXISTS `dispatcher_food_supplied`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_food_supplied` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `food` int NOT NULL,
  `last_fed` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_food_supplied_v1`
--

DROP TABLE IF EXISTS `dispatcher_food_supplied_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_food_supplied_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `food` int NOT NULL,
  `last_fed` int NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_lot_reclaimed`
--

DROP TABLE IF EXISTS `dispatcher_lot_reclaimed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_lot_reclaimed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `lot_label` tinyint NOT NULL,
  `lot_id` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_material_processing_finished`
--

DROP TABLE IF EXISTS `dispatcher_material_processing_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_material_processing_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `processor_label` tinyint NOT NULL,
  `processor_id` bigint NOT NULL,
  `processor_slot` tinyint NOT NULL,
  `processor_type` tinyint NOT NULL,
  `processor_asteroid_id` int DEFAULT NULL,
  `processor_lot_id` bigint DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `processor_multi` (`processor_asteroid_id`,`processor_type`,`block_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_material_processing_started_inputs`
--

DROP TABLE IF EXISTS `dispatcher_material_processing_started_inputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_material_processing_started_inputs` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `process_id` int NOT NULL,
  `process_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_id` int NOT NULL,
  `resource_amount` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_material_processing_started_outputs`
--

DROP TABLE IF EXISTS `dispatcher_material_processing_started_outputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_material_processing_started_outputs` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `process_id` int NOT NULL,
  `process_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_id` int NOT NULL,
  `resource_amount` bigint NOT NULL,
  KEY `txn_idx` (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_material_processing_started_v1`
--

DROP TABLE IF EXISTS `dispatcher_material_processing_started_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_material_processing_started_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `processor_label` tinyint NOT NULL,
  `processor_id` bigint NOT NULL,
  `processor_slot` tinyint NOT NULL,
  `processor_type` tinyint NOT NULL,
  `processor_asteroid_id` int DEFAULT NULL,
  `processor_lot_id` bigint DEFAULT NULL,
  `process_id` int NOT NULL,
  `process_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` bigint DEFAULT NULL,
  `destination_type` tinyint NOT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` bigint DEFAULT NULL,
  `destination_label` tinyint NOT NULL,
  `destination_id` bigint NOT NULL,
  `destination_slot` tinyint NOT NULL,
  `finish_time` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_name_changed`
--

DROP TABLE IF EXISTS `dispatcher_name_changed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_name_changed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_prepaid_agreement_accepted`
--

DROP TABLE IF EXISTS `dispatcher_prepaid_agreement_accepted`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_prepaid_agreement_accepted` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` bigint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `permission` tinyint DEFAULT NULL,
  `permitted_label` tinyint NOT NULL,
  `permitted_id` int NOT NULL,
  `rate` bigint DEFAULT NULL,
  `term` int DEFAULT NULL,
  `initial_term` int DEFAULT NULL,
  `notice_period` int DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_prepaid_agreement_cancelled`
--

DROP TABLE IF EXISTS `dispatcher_prepaid_agreement_cancelled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_prepaid_agreement_cancelled` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `permission` tinyint DEFAULT NULL,
  `permitted_label` tinyint NOT NULL,
  `permitted_id` int NOT NULL,
  `eviction_time` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_prepaid_agreement_extended`
--

DROP TABLE IF EXISTS `dispatcher_prepaid_agreement_extended`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_prepaid_agreement_extended` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` bigint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `permission` tinyint DEFAULT NULL,
  `permitted_label` tinyint NOT NULL,
  `permitted_id` int NOT NULL,
  `rate` bigint DEFAULT NULL,
  `term` int DEFAULT NULL,
  `initial_term` int DEFAULT NULL,
  `notice_period` int DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_prepaid_merkle_policy_removed`
--

DROP TABLE IF EXISTS `dispatcher_prepaid_merkle_policy_removed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_prepaid_merkle_policy_removed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_prepaid_policy_assigned`
--

DROP TABLE IF EXISTS `dispatcher_prepaid_policy_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_prepaid_policy_assigned` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `rate` bigint DEFAULT NULL,
  `initial_term` int DEFAULT NULL,
  `notice_period` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_prepaid_policy_removed`
--

DROP TABLE IF EXISTS `dispatcher_prepaid_policy_removed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_prepaid_policy_removed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_prepare_for_launch_reward_claim`
--

DROP TABLE IF EXISTS `dispatcher_prepare_for_launch_reward_claim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_prepare_for_launch_reward_claim` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_public_policy_assigned`
--

DROP TABLE IF EXISTS `dispatcher_public_policy_assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_public_policy_assigned` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `permission` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_public_policy_removed`
--

DROP TABLE IF EXISTS `dispatcher_public_policy_removed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_public_policy_removed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_random_event_resolved`
--

DROP TABLE IF EXISTS `dispatcher_random_event_resolved`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_random_event_resolved` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `random_event` int NOT NULL,
  `choice` int NOT NULL,
  `action_type` int DEFAULT NULL,
  `action_target_label` tinyint DEFAULT NULL,
  `action_target_id` bigint DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_removed_from_whitelist`
--

DROP TABLE IF EXISTS `dispatcher_removed_from_whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_removed_from_whitelist` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `target_label` tinyint DEFAULT NULL,
  `target_id` bigint DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_removed_from_whitelist_v1`
--

DROP TABLE IF EXISTS `dispatcher_removed_from_whitelist_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_removed_from_whitelist_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `permitted_label` tinyint DEFAULT NULL,
  `permitted_id` bigint DEFAULT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_resource_extraction_finished`
--

DROP TABLE IF EXISTS `dispatcher_resource_extraction_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_resource_extraction_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `extractor_label` tinyint(1) NOT NULL,
  `extractor_id` int NOT NULL,
  `extractor_slot` tinyint NOT NULL,
  `extractor_type` tinyint NOT NULL,
  `extractor_asteroid_id` int DEFAULT NULL,
  `extractor_lot_id` int DEFAULT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_yield` bigint NOT NULL,
  `destination_label` tinyint(1) NOT NULL,
  `destination_id` int NOT NULL,
  `destination_slot` int NOT NULL,
  `destination_type` tinyint NOT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_resource_extraction_started`
--

DROP TABLE IF EXISTS `dispatcher_resource_extraction_started`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_resource_extraction_started` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` bigint NOT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_yield` bigint NOT NULL,
  `extractor_label` tinyint(1) NOT NULL,
  `extractor_id` int NOT NULL,
  `extractor_slot` tinyint NOT NULL,
  `extractor_type` tinyint NOT NULL,
  `extractor_asteroid_id` int DEFAULT NULL,
  `extractor_lot_id` int DEFAULT NULL,
  `destination_label` int NOT NULL,
  `destination_id` int NOT NULL,
  `destination_slot` tinyint NOT NULL,
  `destination_type` tinyint NOT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` int DEFAULT NULL,
  `finish_time` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_resource_scan_finished`
--

DROP TABLE IF EXISTS `dispatcher_resource_scan_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_resource_scan_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `water` int DEFAULT NULL,
  `hydrogen` int DEFAULT NULL,
  `amonia` int DEFAULT NULL,
  `nitrogen` int DEFAULT NULL,
  `sulfur_dioxide` int DEFAULT NULL,
  `carbon_dioxide` int DEFAULT NULL,
  `carbon_monoxide` int DEFAULT NULL,
  `methane` int DEFAULT NULL,
  `apatite` int DEFAULT NULL,
  `bitumen` int DEFAULT NULL,
  `calcite` int DEFAULT NULL,
  `feldspar` int DEFAULT NULL,
  `olivine` int DEFAULT NULL,
  `pyroxene` int DEFAULT NULL,
  `coffinite` int DEFAULT NULL,
  `merrillite` int DEFAULT NULL,
  `xenotime` int DEFAULT NULL,
  `rhadbdite` int DEFAULT NULL,
  `graphite` int DEFAULT NULL,
  `taenite` int DEFAULT NULL,
  `troilite` int DEFAULT NULL,
  `uranite` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`asteroid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_resource_scan_started`
--

DROP TABLE IF EXISTS `dispatcher_resource_scan_started`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_resource_scan_started` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` int NOT NULL,
  `finish_time` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_sampling_deposit_finished`
--

DROP TABLE IF EXISTS `dispatcher_sampling_deposit_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_sampling_deposit_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` bigint NOT NULL,
  `initial_yield` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_sampling_deposit_started`
--

DROP TABLE IF EXISTS `dispatcher_sampling_deposit_started`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_sampling_deposit_started` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` bigint NOT NULL,
  `lot_label` tinyint(1) NOT NULL,
  `lot_id` int NOT NULL,
  `packed_lot_id` bigint NOT NULL,
  `asteroid_id` int NOT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `finish_time` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_sampling_deposit_started_v1`
--

DROP TABLE IF EXISTS `dispatcher_sampling_deposit_started_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_sampling_deposit_started_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `deposit_label` tinyint NOT NULL,
  `deposit_id` bigint NOT NULL,
  `lot_label` tinyint(1) NOT NULL,
  `lot_id` int NOT NULL,
  `packed_lot_id` bigint NOT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `improving` int NOT NULL,
  `finish_time` int NOT NULL,
  `origin_label` int NOT NULL,
  `origin_id` int NOT NULL,
  `origin_slot` int NOT NULL,
  `asteroid_id` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_sell_order_cancelled`
--

DROP TABLE IF EXISTS `dispatcher_sell_order_cancelled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_sell_order_cancelled` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` bigint NOT NULL,
  `amount` bigint NOT NULL,
  `storage_label` tinyint NOT NULL,
  `storage_id` int NOT NULL,
  `storage_slot` tinyint NOT NULL,
  `storage_type` tinyint NOT NULL,
  `storage_asteroid_id` int DEFAULT NULL,
  `storage_lot_id` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_sell_order_created`
--

DROP TABLE IF EXISTS `dispatcher_sell_order_created`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_sell_order_created` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `storage_label` tinyint NOT NULL,
  `storage_id` int NOT NULL,
  `storage_slot` tinyint NOT NULL,
  `storage_type` tinyint NOT NULL,
  `storage_asteroid_id` int DEFAULT NULL,
  `storage_lot_id` int DEFAULT NULL,
  `valid_time` int NOT NULL,
  `maker_fee` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_sell_order_filled`
--

DROP TABLE IF EXISTS `dispatcher_sell_order_filled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_sell_order_filled` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `seller_crew_id` int NOT NULL,
  `seller_crew_label` tinyint NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `storage_label` tinyint NOT NULL,
  `storage_id` int NOT NULL,
  `storage_slot` tinyint NOT NULL,
  `storage_type` tinyint NOT NULL,
  `storage_asteroid_id` int DEFAULT NULL,
  `storage_lot_id` int DEFAULT NULL,
  `destination_label` tinyint NOT NULL,
  `destination_id` int NOT NULL,
  `destination_slot` tinyint NOT NULL,
  `destination_type` tinyint NOT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` int DEFAULT NULL,
  `market_order` tinyint DEFAULT NULL,
  `limit_order` tinyint DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `sell_multi_one` (`exchange_asteroid_id`,`block_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_ship_assembly_finished`
--

DROP TABLE IF EXISTS `dispatcher_ship_assembly_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_ship_assembly_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` bigint NOT NULL,
  `dry_dock_label` tinyint NOT NULL,
  `dry_dock_id` bigint NOT NULL,
  `dry_dock_slot` tinyint NOT NULL,
  `destination_label` tinyint NOT NULL,
  `destination_id` bigint NOT NULL,
  `finish_time` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_ship_assembly_started_v1`
--

DROP TABLE IF EXISTS `dispatcher_ship_assembly_started_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_ship_assembly_started_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` bigint NOT NULL,
  `ship_type` tinyint NOT NULL,
  `ship_type_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `dry_dock_label` tinyint NOT NULL,
  `dry_dock_id` bigint NOT NULL,
  `dry_dock_slot` tinyint NOT NULL,
  `dry_dock_type` tinyint NOT NULL,
  `dry_dock_asteroid_id` int NOT NULL,
  `dry_dock_lot_id` int NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_asteroid_id` int NOT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `finish_time` int NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_ship_commandeered`
--

DROP TABLE IF EXISTS `dispatcher_ship_commandeered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_ship_commandeered` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_ship_docked`
--

DROP TABLE IF EXISTS `dispatcher_ship_docked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_ship_docked` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` bigint NOT NULL,
  `dock_label` tinyint NOT NULL,
  `dock_id` bigint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_ship_undocked`
--

DROP TABLE IF EXISTS `dispatcher_ship_undocked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_ship_undocked` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` bigint NOT NULL,
  `dock_label` tinyint NOT NULL,
  `dock_id` bigint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_surface_scan_finished`
--

DROP TABLE IF EXISTS `dispatcher_surface_scan_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_surface_scan_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` bigint NOT NULL,
  `bonuses` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_surface_scan_started`
--

DROP TABLE IF EXISTS `dispatcher_surface_scan_started`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_surface_scan_started` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_label` tinyint NOT NULL,
  `asteroid_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `caller_crew_id` bigint NOT NULL,
  `finish_time` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_system_registered`
--

DROP TABLE IF EXISTS `dispatcher_system_registered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_system_registered` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `class_hash` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_transit_finished`
--

DROP TABLE IF EXISTS `dispatcher_transit_finished`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_transit_finished` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `destination_label` tinyint NOT NULL,
  `destination_id` bigint NOT NULL,
  `departure` bigint NOT NULL,
  `arrival` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_transit_started`
--

DROP TABLE IF EXISTS `dispatcher_transit_started`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_transit_started` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `ship_type` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `destination_label` tinyint NOT NULL,
  `destination_id` bigint NOT NULL,
  `departure` bigint NOT NULL,
  `arrival` bigint NOT NULL,
  `finish_time` int DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `dispatcher_txns_per_block`
--

DROP TABLE IF EXISTS `dispatcher_txns_per_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispatcher_txns_per_block` (
  `block_number` int NOT NULL,
  `txns` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `extractions`
--

DROP TABLE IF EXISTS `extractions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `extractions` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_block_number` int NOT NULL,
  `start_timestamp` timestamp NOT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `deposit_id` bigint NOT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_yield` bigint NOT NULL,
  `extractor_id` int NOT NULL,
  `extractor_slot` tinyint NOT NULL,
  `extractor_type` tinyint NOT NULL,
  `extractor_asteroid_id` int DEFAULT NULL,
  `extractor_lot_id` int DEFAULT NULL,
  `destination_label` tinyint NOT NULL,
  `destination_id` int NOT NULL,
  `destination_slot` tinyint NOT NULL,
  `destination_type` tinyint NOT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` int DEFAULT NULL,
  `finish_time` int NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint NOT NULL,
  KEY `extractions_multi_one` (`extractor_id`,`resource_id`,`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `food_burned`
--

DROP TABLE IF EXISTS `food_burned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_burned` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `food` int NOT NULL,
  `station_label` tinyint DEFAULT NULL,
  `station_id` bigint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` bigint DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `food_produced`
--

DROP TABLE IF EXISTS `food_produced`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_produced` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `destination_type` tinyint DEFAULT NULL,
  `destination_label` tinyint DEFAULT NULL,
  `destination_id` bigint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `amount` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `food_supplied_actions`
--

DROP TABLE IF EXISTS `food_supplied_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `food_supplied_actions` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `food` int NOT NULL,
  `last_fed` int NOT NULL,
  `origin_label` tinyint DEFAULT NULL,
  `origin_id` bigint DEFAULT NULL,
  `origin_slot` tinyint DEFAULT NULL,
  `origin_type` tinyint DEFAULT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` bigint DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `influence_txns`
--

DROP TABLE IF EXISTS `influence_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `influence_txns` (
  `block_number` int NOT NULL,
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `fee` bigint NOT NULL DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  `contract` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int DEFAULT NULL,
  `wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`txn_id`,`fee`,`contract`),
  KEY `timestamp_index` (`timestamp`),
  KEY `contract_index` (`contract`,`timestamp`),
  KEY `txn_index` (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `inventories`
--

DROP TABLE IF EXISTS `inventories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventories` (
  `inventory_label` int DEFAULT NULL,
  `inventory_type` tinyint NOT NULL,
  `inventory_id` int NOT NULL,
  `inventory_slot` tinyint NOT NULL,
  `resource_id` int NOT NULL,
  `inventory_amount` bigint NOT NULL,
  KEY `inventories_multi_one` (`inventory_label`,`inventory_id`,`inventory_slot`,`inventory_type`,`resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `packaged_deliveries`
--

DROP TABLE IF EXISTS `packaged_deliveries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `packaged_deliveries` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_slot` tinyint NOT NULL,
  `dest_label` tinyint NOT NULL,
  `dest_id` bigint NOT NULL,
  `dest_type` tinyint NOT NULL,
  `dest_slot` tinyint NOT NULL,
  `delivery_label` tinyint NOT NULL,
  `delivery_id` bigint NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `product_id` int NOT NULL,
  `product_amount` bigint NOT NULL,
  `last_updated` timestamp NULL DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prepaid_agreements`
--

DROP TABLE IF EXISTS `prepaid_agreements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prepaid_agreements` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `cancelled_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cancelled_block_number` int DEFAULT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` bigint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `permission` tinyint DEFAULT NULL,
  `permitted_label` tinyint NOT NULL,
  `permitted_id` int NOT NULL,
  `rate` bigint DEFAULT NULL,
  `term` int DEFAULT NULL,
  `initial_term` int DEFAULT NULL,
  `notice_period` int DEFAULT NULL,
  `eviction_time` int DEFAULT NULL,
  `status` tinyint DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prepaid_merkle_policies`
--

DROP TABLE IF EXISTS `prepaid_merkle_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prepaid_merkle_policies` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_crew_id` int NOT NULL,
  `caller_crew_label` tinyint NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `contract` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prepaid_policies`
--

DROP TABLE IF EXISTS `prepaid_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prepaid_policies` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `permission` int DEFAULT NULL,
  `rate` bigint DEFAULT NULL,
  `initial_term` int DEFAULT NULL,
  `notice_period` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `prepare_for_launch_rewards`
--

DROP TABLE IF EXISTS `prepare_for_launch_rewards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prepare_for_launch_rewards` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `asteroid_id` int NOT NULL,
  `redeemed` tinyint DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `processing_actions`
--

DROP TABLE IF EXISTS `processing_actions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processing_actions` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_block_number` int NOT NULL,
  `start_timestamp` timestamp NOT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `process_id` int NOT NULL,
  `process_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `finish_time` int NOT NULL,
  `processor_id` bigint NOT NULL,
  `processor_type` tinyint NOT NULL,
  `processor_asteroid_id` int DEFAULT NULL,
  `processor_lot_id` bigint DEFAULT NULL,
  `processor_slot` tinyint NOT NULL,
  `processor_label` tinyint NOT NULL,
  `origin_id` bigint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` bigint DEFAULT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `destination_id` bigint NOT NULL,
  `destination_type` tinyint NOT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` bigint DEFAULT NULL,
  `destination_slot` tinyint NOT NULL,
  `destination_label` tinyint NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint NOT NULL,
  KEY `processor_status_multi` (`processor_id`,`status`),
  KEY `processor_status_multi_two` (`processor_asteroid_id`,`processor_type`,`process_id`,`finish_txn_id`,`finish_block_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_consumed`
--

DROP TABLE IF EXISTS `products_consumed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_consumed` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `origin_type` tinyint DEFAULT NULL,
  `origin_label` tinyint DEFAULT NULL,
  `origin_id` bigint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_amount` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_produced`
--

DROP TABLE IF EXISTS `products_produced`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_produced` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `destination_type` tinyint DEFAULT NULL,
  `destination_label` tinyint DEFAULT NULL,
  `destination_id` bigint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_amount` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`),
  KEY `products_multi_one` (`txn_id`,`resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `products_sold`
--

DROP TABLE IF EXISTS `products_sold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products_sold` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `buyer_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `buyer_crew_id` int NOT NULL,
  `seller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `seller_crew_id` int NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `storage_label` tinyint NOT NULL,
  `storage_id` int NOT NULL,
  `storage_slot` tinyint NOT NULL,
  `storage_type` tinyint NOT NULL,
  `storage_asteroid_id` int DEFAULT NULL,
  `storage_lot_id` int DEFAULT NULL,
  `destination_label` tinyint DEFAULT NULL,
  `destination_id` int DEFAULT NULL,
  `destination_slot` tinyint DEFAULT NULL,
  `destination_type` tinyint DEFAULT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` int DEFAULT NULL,
  `origin_label` tinyint DEFAULT NULL,
  `origin_id` int DEFAULT NULL,
  `origin_slot` tinyint DEFAULT NULL,
  `origin_type` tinyint DEFAULT NULL,
  `origin_asteroid_id` int DEFAULT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `maker_fee` bigint DEFAULT '0',
  `order_type` varchar(4) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `market_order` tinyint DEFAULT NULL,
  `limit_order` tinyint DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `propellant_burned`
--

DROP TABLE IF EXISTS `propellant_burned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propellant_burned` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `ship_label` int NOT NULL,
  `ship_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `fuel_burned` bigint DEFAULT '0',
  `previous_fuel` bigint DEFAULT '0',
  `new_fuel` bigint DEFAULT '0',
  `burn_type` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `propellant_produced`
--

DROP TABLE IF EXISTS `propellant_produced`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propellant_produced` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `destination_type` tinyint DEFAULT NULL,
  `destination_label` tinyint DEFAULT NULL,
  `destination_id` bigint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `amount` bigint DEFAULT '0',
  `method` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `public_policies`
--

DROP TABLE IF EXISTS `public_policies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `public_policies` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `entity_type` tinyint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `permission` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sell_orders`
--

DROP TABLE IF EXISTS `sell_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sell_orders` (
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `valid_time` int NOT NULL,
  `maker_fee` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `settings`
--

DROP TABLE IF EXISTS `settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `settings` (
  `name` varchar(45) DEFAULT NULL,
  `setting` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_assembly`
--

DROP TABLE IF EXISTS `ship_assembly`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_assembly` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_block_number` int NOT NULL,
  `start_timestamp` timestamp NOT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `ship_id` bigint NOT NULL,
  `ship_type` tinyint NOT NULL,
  `ship_type_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `dry_dock_label` tinyint NOT NULL,
  `dry_dock_id` bigint NOT NULL,
  `dry_dock_slot` tinyint NOT NULL,
  `dry_dock_type` tinyint NOT NULL,
  `dry_dock_asteroid_id` int NOT NULL,
  `dry_dock_lot_id` int NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` bigint DEFAULT NULL,
  `origin_slot` tinyint NOT NULL,
  `origin_type` tinyint NOT NULL,
  `origin_asteroid_id` int NOT NULL,
  `origin_lot_id` int DEFAULT NULL,
  `destination_label` tinyint DEFAULT NULL,
  `destination_id` bigint DEFAULT NULL,
  `destination_type` tinyint DEFAULT NULL,
  `destination_asteroid_id` int DEFAULT NULL,
  `destination_lot_id` int DEFAULT NULL,
  `finish_time` int NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_bridged_from_l1`
--

DROP TABLE IF EXISTS `ship_bridged_from_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_bridged_from_l1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_bridged_from_l1_txns`
--

DROP TABLE IF EXISTS `ship_bridged_from_l1_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_bridged_from_l1_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_bridged_to_l1`
--

DROP TABLE IF EXISTS `ship_bridged_to_l1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_bridged_to_l1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_bridged_to_l1_txns`
--

DROP TABLE IF EXISTS `ship_bridged_to_l1_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_bridged_to_l1_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_emergency`
--

DROP TABLE IF EXISTS `ship_emergency`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_emergency` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_block_number` int NOT NULL,
  `start_timestamp` timestamp NOT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `ship_id` int NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_type` tinyint(1) DEFAULT NULL,
  `amount` int DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_sell_order_filled`
--

DROP TABLE IF EXISTS `ship_sell_order_filled`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_sell_order_filled` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `price` bigint NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_sell_order_set`
--

DROP TABLE IF EXISTS `ship_sell_order_set`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_sell_order_set` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `price` bigint NOT NULL,
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_transfers`
--

DROP TABLE IF EXISTS `ship_transfers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_transfers` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_transfers_txns`
--

DROP TABLE IF EXISTS `ship_transfers_txns`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_transfers_txns` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `fee` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ship_txns_per_block`
--

DROP TABLE IF EXISTS `ship_txns_per_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ship_txns_per_block` (
  `block_number` int NOT NULL,
  `txns` int NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ships`
--

DROP TABLE IF EXISTS `ships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ships` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_owner` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_id` int NOT NULL,
  `name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `features` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_type` tinyint(1) DEFAULT NULL,
  `ship_type_name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crew_id` int DEFAULT NULL,
  `emergency` tinyint DEFAULT '0',
  PRIMARY KEY (`ship_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ships_docked`
--

DROP TABLE IF EXISTS `ships_docked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ships_docked` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crew_id` int DEFAULT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `dock_label` tinyint NOT NULL,
  `dock_id` bigint DEFAULT NULL,
  `dock_type` tinyint NOT NULL,
  `dock_asteroid_id` int DEFAULT NULL,
  `dock_lot_id` int DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint DEFAULT '0',
  PRIMARY KEY (`ship_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ships_for_sale`
--

DROP TABLE IF EXISTS `ships_for_sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ships_for_sale` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `seller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `ship_type` tinyint NOT NULL,
  `price` bigint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ships_sold`
--

DROP TABLE IF EXISTS `ships_sold`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ships_sold` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `seller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `buyer_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_id` int NOT NULL,
  `ship_type` tinyint NOT NULL,
  `price` bigint NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ships_state`
--

DROP TABLE IF EXISTS `ships_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ships_state` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `crew_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `ship_type` int DEFAULT NULL,
  `lot_id` bigint DEFAULT NULL,
  `status` tinyint DEFAULT NULL,
  PRIMARY KEY (`ship_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `solo_missions_tracking`
--

DROP TABLE IF EXISTS `solo_missions_tracking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solo_missions_tracking` (
  `wallet` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `mission_1_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Team Assemble',
  `mission_1_req_1_goal` tinyint DEFAULT '5',
  `mission_1_req_1` tinyint DEFAULT '0',
  `mission_1_req_2_goal` tinyint DEFAULT '2',
  `mission_1_req_2` tinyint DEFAULT '0',
  `mission_2_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Buried Treasure',
  `mission_2_req_1_goal` tinyint DEFAULT '5',
  `mission_2_req_1` tinyint DEFAULT '0',
  `mission_2_req_2_goal` tinyint DEFAULT '5',
  `mission_2_req_2` tinyint DEFAULT '0',
  `mission_3_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Market Maker',
  `mission_3_req_1_goal` tinyint DEFAULT '6',
  `mission_3_req_1` tinyint DEFAULT '0',
  `mission_3_req_2_goal` tinyint DEFAULT '6',
  `mission_3_req_2` tinyint DEFAULT '0',
  `mission_4_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Breaking Ground',
  `mission_4_req_1_goal` int DEFAULT '10000',
  `mission_4_req_1` int DEFAULT '0',
  `mission_4_req_2_goal` tinyint DEFAULT '4',
  `mission_4_req_2` tinyint DEFAULT '0',
  `mission_5_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'City Builder',
  `mission_5_req_1_goal` tinyint DEFAULT '5',
  `mission_5_req_1` tinyint DEFAULT '0',
  `mission_6_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Explore the Stars',
  `mission_6_req_1_goal` tinyint DEFAULT '1',
  `mission_6_req_1` tinyint DEFAULT '0',
  `mission_6_req_2_goal` tinyint DEFAULT '1',
  `mission_6_req_2` tinyint DEFAULT '0',
  `mission_7_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Expand the Colony',
  `mission_7_req_1_goal` tinyint DEFAULT '1',
  `mission_7_req_1` tinyint DEFAULT '0',
  `mission_8_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Special Delivery',
  `mission_8_req_1_goal` int DEFAULT '1000',
  `mission_8_req_1` int DEFAULT '0',
  `mission_9_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'Dinner is Served',
  `mission_9_req_1_goal` int DEFAULT '10',
  `mission_9_req_1` int DEFAULT '0',
  PRIMARY KEY (`crew_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `starknet_txns_per_block`
--

DROP TABLE IF EXISTS `starknet_txns_per_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `starknet_txns_per_block` (
  `block_number` int NOT NULL,
  `txns` int DEFAULT NULL,
  `dispatcher_txns` int DEFAULT NULL,
  `asteroid_txns` int DEFAULT NULL,
  `crewmate_txns` int DEFAULT NULL,
  `crew_txns` int DEFAULT NULL,
  `ship_txns` int DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stations`
--

DROP TABLE IF EXISTS `stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stations` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `station_id` int NOT NULL,
  `station_label` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sway_holders`
--

DROP TABLE IF EXISTS `sway_holders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sway_holders` (
  `wallet_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `value` bigint NOT NULL,
  PRIMARY KEY (`wallet_address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `sway_transfers`
--

DROP TABLE IF EXISTS `sway_transfers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sway_transfers` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `to_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `value` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `systems_registered`
--

DROP TABLE IF EXISTS `systems_registered`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `systems_registered` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `class_hash` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_inventories`
--

DROP TABLE IF EXISTS `temp_inventories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_inventories` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `inventory_label` int DEFAULT NULL,
  `inventory_type` tinyint NOT NULL,
  `inventory_slot` tinyint NOT NULL,
  `resource_id` int NOT NULL,
  `inventory_amount` bigint NOT NULL,
  PRIMARY KEY (`txn_id`,`resource_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_products_produced`
--

DROP TABLE IF EXISTS `temp_products_produced`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_products_produced` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `destination_type` tinyint DEFAULT NULL,
  `destination_label` tinyint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `resource_id` int NOT NULL,
  `resource_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `resource_amount` bigint DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT NULL,
  KEY `timestamp_idx` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_propellant_produced`
--

DROP TABLE IF EXISTS `temp_propellant_produced`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_propellant_produced` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `destination_type` tinyint DEFAULT NULL,
  `destination_label` tinyint DEFAULT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `amount` bigint DEFAULT '0',
  `method` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_ships`
--

DROP TABLE IF EXISTS `temp_ships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_ships` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_owner` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `features` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ship_type` tinyint(1) DEFAULT NULL,
  `ship_type_name` varchar(48) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `crew_id` int DEFAULT NULL,
  `emergency` tinyint DEFAULT '0',
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `temp_stations`
--

DROP TABLE IF EXISTS `temp_stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `temp_stations` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `asteroid_id` int DEFAULT NULL,
  `lot_id` int DEFAULT NULL,
  `station_label` tinyint NOT NULL,
  PRIMARY KEY (`txn_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `transit`
--

DROP TABLE IF EXISTS `transit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transit` (
  `start_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_block_number` int NOT NULL,
  `start_timestamp` timestamp NOT NULL,
  `finish_txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `finish_block_number` int DEFAULT NULL,
  `finish_timestamp` timestamp NULL DEFAULT NULL,
  `from_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `ship_label` tinyint NOT NULL,
  `ship_id` int NOT NULL,
  `ship_type` tinyint NOT NULL,
  `origin_label` tinyint NOT NULL,
  `origin_id` int NOT NULL,
  `destination_label` tinyint NOT NULL,
  `destination_id` int NOT NULL,
  `departure` bigint NOT NULL,
  `arrival` bigint NOT NULL,
  `finish_time` int DEFAULT NULL,
  `cargo` int DEFAULT NULL,
  `c_cargo` int DEFAULT NULL,
  `m_cargo` int DEFAULT NULL,
  `s_cargo` int DEFAULT NULL,
  `i_cargo` int DEFAULT NULL,
  `fuel` int DEFAULT NULL,
  `discobot` tinyint DEFAULT '1',
  `dashboard` tinyint DEFAULT '1',
  `status` tinyint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `txns_per_block`
--

DROP TABLE IF EXISTS `txns_per_block`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `txns_per_block` (
  `block_number` int NOT NULL,
  `txns` int NOT NULL,
  `ship_txns` int DEFAULT '0',
  `ship_status` tinyint DEFAULT NULL,
  `crewmate_txns` int DEFAULT '0',
  `crewmate_status` tinyint DEFAULT NULL,
  `crew_txns` int DEFAULT '0',
  `crew_status` tinyint DEFAULT NULL,
  `asteroid_txns` int DEFAULT '0',
  `asteroid_status` tinyint DEFAULT NULL,
  `dispatcher_txns` int DEFAULT '0',
  `dispatcher_status` tinyint DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL,
  `status` tinyint DEFAULT '1',
  KEY `timestamp_idx` (`timestamp`),
  KEY `txn_block` (`block_number`),
  KEY `block_number_idx` (`block_number`),
  KEY `ship_status_idx` (`ship_status`),
  KEY `asteroid_multi` (`asteroid_status`,`block_number`),
  KEY `crew_multi` (`crew_status`,`block_number`),
  KEY `crewmate_multi` (`crewmate_status`,`block_number`),
  KEY `dispatcher_multi` (`dispatcher_status`,`block_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wallet_buy_orders`
--

DROP TABLE IF EXISTS `wallet_buy_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallet_buy_orders` (
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `valid_time` int NOT NULL,
  `maker_fee` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `wallet_sell_orders`
--

DROP TABLE IF EXISTS `wallet_sell_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `wallet_sell_orders` (
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `exchange_label` tinyint NOT NULL,
  `exchange_id` int NOT NULL,
  `exchange_type` tinyint NOT NULL,
  `exchange_asteroid_id` int DEFAULT NULL,
  `exchange_lot_id` int DEFAULT NULL,
  `product_id` int NOT NULL,
  `product_name` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `amount` bigint NOT NULL,
  `price` bigint NOT NULL,
  `valid_time` int NOT NULL,
  `maker_fee` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `whitelist`
--

DROP TABLE IF EXISTS `whitelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `whitelist` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `entity_label` tinyint NOT NULL,
  `entity_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `target_label` tinyint DEFAULT NULL,
  `target_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `whitelist_v1`
--

DROP TABLE IF EXISTS `whitelist_v1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `whitelist_v1` (
  `txn_id` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `block_number` int NOT NULL,
  `caller_address` varchar(68) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `crew_id` int NOT NULL,
  `target_label` tinyint NOT NULL,
  `target_id` int NOT NULL,
  `permission` int DEFAULT NULL,
  `permitted_label` tinyint DEFAULT NULL,
  `permitted_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-12 18:52:44
