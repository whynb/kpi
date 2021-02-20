/*
 Navicat Premium Data Transfer

 Source Server         : MySQL - dev - localhost
 Source Server Type    : MySQL
 Source Server Version : 50717
 Source Host           : localhost:3306
 Source Schema         : kpi

 Target Server Type    : MySQL
 Target Server Version : 50717
 File Encoding         : 65001

 Date: 18/02/2021 20:27:10
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add user', 4, 'add_user');
INSERT INTO `auth_permission` VALUES (14, 'Can change user', 4, 'change_user');
INSERT INTO `auth_permission` VALUES (15, 'Can delete user', 4, 'delete_user');
INSERT INTO `auth_permission` VALUES (16, 'Can view user', 4, 'view_user');
INSERT INTO `auth_permission` VALUES (17, 'Can add content type', 5, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (18, 'Can change content type', 5, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (19, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (20, 'Can view content type', 5, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (21, 'Can add session', 6, 'add_session');
INSERT INTO `auth_permission` VALUES (22, 'Can change session', 6, 'change_session');
INSERT INTO `auth_permission` VALUES (23, 'Can delete session', 6, 'delete_session');
INSERT INTO `auth_permission` VALUES (24, 'Can view session', 6, 'view_session');
INSERT INTO `auth_permission` VALUES (25, 'Can add tgt', 7, 'add_tgt');
INSERT INTO `auth_permission` VALUES (26, 'Can change tgt', 7, 'change_tgt');
INSERT INTO `auth_permission` VALUES (27, 'Can delete tgt', 7, 'delete_tgt');
INSERT INTO `auth_permission` VALUES (28, 'Can view tgt', 7, 'view_tgt');
INSERT INTO `auth_permission` VALUES (29, 'Can add pgt iou', 8, 'add_pgtiou');
INSERT INTO `auth_permission` VALUES (30, 'Can change pgt iou', 8, 'change_pgtiou');
INSERT INTO `auth_permission` VALUES (31, 'Can delete pgt iou', 8, 'delete_pgtiou');
INSERT INTO `auth_permission` VALUES (32, 'Can view pgt iou', 8, 'view_pgtiou');
INSERT INTO `auth_permission` VALUES (33, 'Can add sys user', 9, 'add_sysuser');
INSERT INTO `auth_permission` VALUES (34, 'Can change sys user', 9, 'change_sysuser');
INSERT INTO `auth_permission` VALUES (35, 'Can delete sys user', 9, 'delete_sysuser');
INSERT INTO `auth_permission` VALUES (36, 'Can view sys user', 9, 'view_sysuser');
INSERT INTO `auth_permission` VALUES (37, 'Can add role', 10, 'add_role');
INSERT INTO `auth_permission` VALUES (38, 'Can change role', 10, 'change_role');
INSERT INTO `auth_permission` VALUES (39, 'Can delete role', 10, 'delete_role');
INSERT INTO `auth_permission` VALUES (40, 'Can view role', 10, 'view_role');
INSERT INTO `auth_permission` VALUES (41, 'Can add usertype', 11, 'add_usertype');
INSERT INTO `auth_permission` VALUES (42, 'Can change usertype', 11, 'change_usertype');
INSERT INTO `auth_permission` VALUES (43, 'Can delete usertype', 11, 'delete_usertype');
INSERT INTO `auth_permission` VALUES (44, 'Can view usertype', 11, 'view_usertype');
INSERT INTO `auth_permission` VALUES (45, 'Can add menu', 12, 'add_menu');
INSERT INTO `auth_permission` VALUES (46, 'Can change menu', 12, 'change_menu');
INSERT INTO `auth_permission` VALUES (47, 'Can delete menu', 12, 'delete_menu');
INSERT INTO `auth_permission` VALUES (48, 'Can view menu', 12, 'view_menu');
COMMIT;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user
-- ----------------------------
BEGIN;
INSERT INTO `auth_user` VALUES (1, '!PAQG48PfQPPVIqJS3gM6O1RbcKaTEkpNHhKSZZnB', '2021-02-08 08:59:12.073433', 0, 'why', '', '', '', 0, 1, '2021-02-06 21:48:07.200536');
COMMIT;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_jzgjcsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_jzgjcsjxx`;
CREATE TABLE `dc_jzgjcsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JZGH` varchar(16) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `YWXM` varchar(16) DEFAULT NULL,
  `XMPY` varchar(16) DEFAULT NULL,
  `CYM` varchar(16) DEFAULT NULL,
  `XBM` varchar(16) DEFAULT NULL,
  `CSRQ` datetime DEFAULT NULL,
  `CSDM` varchar(16) DEFAULT NULL,
  `BZLBM` varchar(16) DEFAULT NULL,
  `JZGLBM` varchar(16) DEFAULT NULL,
  `DQZTM` varchar(16) DEFAULT NULL,
  `note` varchar(1024) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `JZGH` (`JZGH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_jzgjcsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_xmjfxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_xmjfxx`;
CREATE TABLE `dc_xmjfxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JHJFZE` float DEFAULT NULL,
  `XMJFLYM` varchar(16) DEFAULT NULL,
  `BRRQ` datetime DEFAULT NULL,
  `BKS` float DEFAULT NULL,
  `ZCRQ` datetime DEFAULT NULL,
  `BFXZDWJF` float DEFAULT NULL,
  `XMPZBH` varchar(64) DEFAULT NULL,
  `JBRXM` varchar(32) DEFAULT NULL,
  `XMBH` varchar(64) DEFAULT NULL,
  `ZZKS` float DEFAULT NULL,
  `JZGH` varchar(16) DEFAULT NULL,
  `note` varchar(1024) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `JHJFZE` (`JHJFZE`),
  UNIQUE KEY `XMBH` (`XMBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_xmjfxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_zzjgjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_zzjgjbsjxx`;
CREATE TABLE `dc_zzjgjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DWH` varchar(128) DEFAULT NULL,
  `DWMC` varchar(128) DEFAULT NULL,
  `DWYWMC` varchar(128) DEFAULT NULL,
  `DWJC` varchar(128) DEFAULT NULL,
  `DWYWJC` varchar(128) DEFAULT NULL,
  `DWJP` varchar(128) DEFAULT NULL,
  `DWDZ` varchar(128) DEFAULT NULL,
  `SZXQ` varchar(128) DEFAULT NULL,
  `LSDWH` varchar(128) DEFAULT NULL,
  `DWLBM` varchar(128) DEFAULT NULL,
  `DWBBM` varchar(128) DEFAULT NULL,
  `DWYXBS` varchar(128) DEFAULT NULL,
  `SXRQ` datetime DEFAULT NULL,
  `SFST` varchar(128) DEFAULT NULL,
  `JLNY` datetime DEFAULT NULL,
  `DWFZRH` varchar(128) DEFAULT NULL,
  `note` varchar(1024) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `DWH` (`DWH`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_zzjgjbsjxx
-- ----------------------------
BEGIN;
INSERT INTO `dc_zzjgjbsjxx` VALUES (1, '00000B', '', '', '', '', '', '', '', '', '', '', '', '2021-02-08 21:48:08', '', '2020-01-01 00:00:00', '', '', '2021-02-18 20:16:11.461727');
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (8, 'cas', 'pgtiou');
INSERT INTO `django_content_type` VALUES (7, 'cas', 'tgt');
INSERT INTO `django_content_type` VALUES (5, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (12, 'jx', 'menu');
INSERT INTO `django_content_type` VALUES (10, 'jx', 'role');
INSERT INTO `django_content_type` VALUES (9, 'jx', 'sysuser');
INSERT INTO `django_content_type` VALUES (11, 'jx', 'usertype');
INSERT INTO `django_content_type` VALUES (6, 'sessions', 'session');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2021-02-06 21:17:55.354021');
INSERT INTO `django_migrations` VALUES (2, 'auth', '0001_initial', '2021-02-06 21:17:55.531317');
INSERT INTO `django_migrations` VALUES (3, 'admin', '0001_initial', '2021-02-06 21:17:55.825775');
INSERT INTO `django_migrations` VALUES (4, 'admin', '0002_logentry_remove_auto_add', '2021-02-06 21:17:55.887854');
INSERT INTO `django_migrations` VALUES (5, 'admin', '0003_logentry_add_action_flag_choices', '2021-02-06 21:17:55.919536');
INSERT INTO `django_migrations` VALUES (6, 'contenttypes', '0002_remove_content_type_name', '2021-02-06 21:17:56.011789');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2021-02-06 21:17:56.094470');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2021-02-06 21:17:56.132299');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2021-02-06 21:17:56.160419');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2021-02-06 21:17:56.213143');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2021-02-06 21:17:56.216450');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2021-02-06 21:17:56.252004');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2021-02-06 21:17:56.310754');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2021-02-06 21:17:56.360693');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0010_alter_group_name_max_length', '2021-02-06 21:17:56.405934');
INSERT INTO `django_migrations` VALUES (16, 'auth', '0011_update_proxy_permissions', '2021-02-06 21:17:56.421721');
INSERT INTO `django_migrations` VALUES (17, 'auth', '0012_alter_user_first_name_max_length', '2021-02-06 21:17:56.465593');
INSERT INTO `django_migrations` VALUES (18, 'sessions', '0001_initial', '2021-02-06 21:17:56.491293');
INSERT INTO `django_migrations` VALUES (20, 'jx', '0001_initial', '2021-02-06 23:31:35.686678');
INSERT INTO `django_migrations` VALUES (21, 'jx', '0002_auto_20210208_1139', '2021-02-08 11:40:00.274172');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_jzgjcsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_jzgjcsjxx`;
CREATE TABLE `dr_jzgjcsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JZGH` varchar(16) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `YWXM` varchar(16) DEFAULT NULL,
  `XMPY` varchar(16) DEFAULT NULL,
  `CYM` varchar(16) DEFAULT NULL,
  `XBM` varchar(16) DEFAULT NULL,
  `CSRQ` datetime DEFAULT NULL,
  `CSDM` varchar(16) DEFAULT NULL,
  `BZLBM` varchar(16) DEFAULT NULL,
  `JZGLBM` varchar(16) DEFAULT NULL,
  `DQZTM` varchar(16) DEFAULT NULL,
  `note` varchar(1024) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `JZGH` (`JZGH`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_jzgjcsjxx
-- ----------------------------
BEGIN;
INSERT INTO `dr_jzgjcsjxx` VALUES (1, 'admin', '00000A', '超级管理员', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2021-02-18 20:14:46.670939');
INSERT INTO `dr_jzgjcsjxx` VALUES (3, '0001a', '00000C', '张三', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '985', '2021-02-18 20:14:46.670939');
INSERT INTO `dr_jzgjcsjxx` VALUES (4, '00001B', '00000C', '李四', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '名校', '2021-02-18 20:14:46.670939');
INSERT INTO `dr_jzgjcsjxx` VALUES (5, '000001C', '00000B', '王武', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', '2021-02-18 20:14:46.670939');
INSERT INTO `dr_jzgjcsjxx` VALUES (6, '000001D', '00000B', '赵六', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '', '2021-02-18 20:14:46.670939');
COMMIT;

-- ----------------------------
-- Table structure for dr_xmjfxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_xmjfxx`;
CREATE TABLE `dr_xmjfxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JHJFZE` float DEFAULT NULL,
  `XMJFLYM` varchar(16) DEFAULT NULL,
  `BRRQ` datetime DEFAULT NULL,
  `BKS` float DEFAULT NULL,
  `ZCRQ` datetime DEFAULT NULL,
  `BFXZDWJF` float DEFAULT NULL,
  `XMPZBH` varchar(64) DEFAULT NULL,
  `JBRXM` varchar(32) DEFAULT NULL,
  `XMBH` varchar(64) DEFAULT NULL,
  `ZZKS` float DEFAULT NULL,
  `JZGH` varchar(16) DEFAULT NULL,
  `note` varchar(1024) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `XMBH` (`XMBH`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_xmjfxx
-- ----------------------------
BEGIN;
INSERT INTO `dr_xmjfxx` VALUES (1, 18000, '12', '2020-02-01 00:00:00', 20000, '1970-01-01 00:00:00', 0, 'XS12345', '李四', 'BH8888', 9000, '00001B', NULL, '2021-02-18 20:12:21.436629');
INSERT INTO `dr_xmjfxx` VALUES (2, 78000, '12', '2020-02-01 00:00:00', 110000, '1970-01-01 00:00:00', 0, 'XS12345', '李四', 'BH8887', 9000, '00001B', NULL, '2021-02-18 20:12:21.436629');
INSERT INTO `dr_xmjfxx` VALUES (3, 6000, '12', '2020-02-01 00:00:00', 10000, '1970-01-01 00:00:00', 0, 'XS12345', '李四', 'BH8886', 14000, '00001B', NULL, '2021-02-18 20:12:21.436629');
COMMIT;

-- ----------------------------
-- Table structure for dr_zzjgjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_zzjgjbsjxx`;
CREATE TABLE `dr_zzjgjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DWH` varchar(128) DEFAULT NULL,
  `DWMC` varchar(128) DEFAULT NULL,
  `DWYWMC` varchar(128) DEFAULT NULL,
  `DWJC` varchar(128) DEFAULT NULL,
  `DWYWJC` varchar(128) DEFAULT NULL,
  `DWJP` varchar(128) DEFAULT NULL,
  `DWDZ` varchar(128) DEFAULT NULL,
  `SZXQ` varchar(128) DEFAULT NULL,
  `LSDWH` varchar(128) DEFAULT NULL,
  `DWLBM` varchar(128) DEFAULT NULL,
  `DWBBM` varchar(128) DEFAULT NULL,
  `DWYXBS` varchar(128) DEFAULT NULL,
  `SXRQ` datetime DEFAULT NULL,
  `SFST` varchar(128) DEFAULT NULL,
  `JLNY` datetime DEFAULT NULL,
  `DWFZRH` varchar(128) DEFAULT NULL,
  `note` varchar(1024) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `DWH` (`DWH`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_zzjgjbsjxx
-- ----------------------------
BEGIN;
INSERT INTO `dr_zzjgjbsjxx` VALUES (1, '', '', '', '', '', '', '', '', '00000B', '', '', '', '2021-00-01 00:00:00', '', '2021-00-01 00:00:00', '', '', '2021-02-18 20:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (3, '122', '', '', '', '', '', '', '', '00000B', '', '', '', '2021-00-01 00:00:00', '', '2021-00-01 00:00:00', '', '', '2021-02-18 20:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (4, '1223', '', '', '', '', '', '', '', '00000B', '', '', '', '2021-00-01 00:00:00', '', '2020-00-01 00:00:00', '', '', '2021-02-18 20:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (13, '00000D', '金属研究所', 'ITC', '', '', '', '', '', '00000C', '', '', '', '2099-12-31 00:00:00', '', '1954-01-01 00:00:00', '', '', '2021-02-18 20:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (14, '1234', '', '', '', '', '', '', '', '00000B', '', '', '', '2021-00-01 00:00:00', '', '1920-00-01 00:00:00', '', '', '2021-02-18 20:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (28, '00000A', '东北大学', 'NEU', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2099-12-31 00:00:00', NULL, '1909-01-01 00:00:00', NULL, '985', '2021-02-18 20:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (29, '00000B', '信息工程学院', 'ITC', '信息', '', '', '', '', '00000A', '', '', NULL, '2099-01-01 00:00:00', '', '1909-00-01 00:00:00', '', '名校', '2021-02-18 20:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (30, '00000C', '冶金工程学院', 'ITC', '冶金', NULL, NULL, NULL, NULL, '00000A', NULL, NULL, NULL, '2099-12-31 00:00:00', NULL, '1935-01-01 00:00:00', NULL, '', '2021-02-18 20:14:40.767352');
COMMIT;

-- ----------------------------
-- Table structure for jx_menu
-- ----------------------------
DROP TABLE IF EXISTS `jx_menu`;
CREATE TABLE `jx_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(128) NOT NULL,
  `menu_classify` varchar(128) NOT NULL,
  `menu_addr` varchar(128) NOT NULL,
  `menu_icon` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jx_menu
-- ----------------------------
BEGIN;
INSERT INTO `jx_menu` VALUES (1, '角色管理', '系统管理', '/jx/role_manage/', NULL);
INSERT INTO `jx_menu` VALUES (2, '权限分配', '系统管理', '/jx/role_assign/', NULL);
INSERT INTO `jx_menu` VALUES (3, '组织机构基本数据信息', '公共管理', '/jx/base/zzjgjbsjxx/', NULL);
INSERT INTO `jx_menu` VALUES (4, '教职工基础数据信息', '公共管理', '/jx/base/jzgjcsjxx/', NULL);
INSERT INTO `jx_menu` VALUES (5, '项目经费信息', '科研管理', '/jx/base/xmjfxx/', NULL);
INSERT INTO `jx_menu` VALUES (6, '绩效考核规则', '考核管理', '/jx/jxkhgz/', NULL);
INSERT INTO `jx_menu` VALUES (7, '绩效考核结果', '考核管理', '/jx/khjgmx/', NULL);
COMMIT;

-- ----------------------------
-- Table structure for jx_role
-- ----------------------------
DROP TABLE IF EXISTS `jx_role`;
CREATE TABLE `jx_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jx_role
-- ----------------------------
BEGIN;
INSERT INTO `jx_role` VALUES (1, '超级管理员');
INSERT INTO `jx_role` VALUES (2, '系统管理员');
INSERT INTO `jx_role` VALUES (3, '部门管理员');
INSERT INTO `jx_role` VALUES (4, '教职工');
COMMIT;

-- ----------------------------
-- Table structure for jx_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `jx_role_menu`;
CREATE TABLE `jx_role_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `permission` varchar(1024) DEFAULT 'n,n,n,n,n,n',
  PRIMARY KEY (`id`),
  UNIQUE KEY `jx_role_menu_role_id_menu_id_db4f98e9_uniq` (`role_id`,`menu_id`),
  KEY `jx_role_menu_menu_id_8a8f7bb1_fk_jx_menu_id` (`menu_id`),
  CONSTRAINT `jx_role_menu_menu_id_8a8f7bb1_fk_jx_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `jx_menu` (`id`),
  CONSTRAINT `jx_role_menu_role_id_3cfa6a3a_fk_jx_role_id` FOREIGN KEY (`role_id`) REFERENCES `jx_role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jx_role_menu
-- ----------------------------
BEGIN;
INSERT INTO `jx_role_menu` VALUES (1, 1, 1, 'n,n,n,n,y,n');
INSERT INTO `jx_role_menu` VALUES (3, 1, 2, 'y,y,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (8, 1, 3, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (9, 1, 4, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (10, 1, 5, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (11, 1, 6, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (12, 1, 7, 'y,n,n,y,y,y');
COMMIT;

-- ----------------------------
-- Table structure for jx_sysuser
-- ----------------------------
DROP TABLE IF EXISTS `jx_sysuser`;
CREATE TABLE `jx_sysuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `payroll` varchar(32) NOT NULL,
  `password` varchar(256) NOT NULL,
  `time_pwd` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `role_id` int(11) NOT NULL,
  `usertype_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `jx_sysuser_role_id_2e0db55f_fk_jx_role_id` (`role_id`),
  KEY `jx_sysuser_usertype_id_8b22427b_fk_jx_usertype_id` (`usertype_id`),
  CONSTRAINT `jx_sysuser_role_id_2e0db55f_fk_jx_role_id` FOREIGN KEY (`role_id`) REFERENCES `jx_role` (`id`),
  CONSTRAINT `jx_sysuser_usertype_id_8b22427b_fk_jx_usertype_id` FOREIGN KEY (`usertype_id`) REFERENCES `jx_usertype` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jx_sysuser
-- ----------------------------
BEGIN;
INSERT INTO `jx_sysuser` VALUES (1, '00XW1306', '111111', '2021-02-06 23:51:43.981236', 1, 1);
INSERT INTO `jx_sysuser` VALUES (2, 'admin', '111111', '2021-02-06 23:52:03.097344', 1, 1);
INSERT INTO `jx_sysuser` VALUES (3, 'dev', '111111', '2021-02-06 23:52:14.803931', 4, 1);
INSERT INTO `jx_sysuser` VALUES (4, 'why', '111111', '2021-02-08 08:30:49.536812', 4, 4);
INSERT INTO `jx_sysuser` VALUES (5, '000001C', '111111', '2021-02-09 19:57:47.163106', 4, 4);
COMMIT;

-- ----------------------------
-- Table structure for jx_usertype
-- ----------------------------
DROP TABLE IF EXISTS `jx_usertype`;
CREATE TABLE `jx_usertype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `usertype_name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jx_usertype
-- ----------------------------
BEGIN;
INSERT INTO `jx_usertype` VALUES (1, '超级管理员');
INSERT INTO `jx_usertype` VALUES (2, '系统管理员');
INSERT INTO `jx_usertype` VALUES (3, '部门管理员');
INSERT INTO `jx_usertype` VALUES (4, '教职工');
COMMIT;

-- ----------------------------
-- Table structure for kh_jxkhgz
-- ----------------------------
DROP TABLE IF EXISTS `kh_jxkhgz`;
CREATE TABLE `kh_jxkhgz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `GZH` varchar(128) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `KHLX` varchar(32) DEFAULT NULL,
  `KHZL` varchar(32) DEFAULT NULL,
  `XXKLZL` varchar(32) DEFAULT NULL,
  `KHMC` varchar(256) DEFAULT NULL,
  `KHSJDX` varchar(64) DEFAULT NULL,
  `GZTJ` varchar(2056) DEFAULT NULL,
  `JXFSJS` varchar(2056) DEFAULT NULL,
  `KHMXMB` text,
  `KHJGDX` varchar(64) DEFAULT NULL,
  `note` varchar(2056) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `GZH` (`GZH`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_jxkhgz
-- ----------------------------
BEGIN;
INSERT INTO `kh_jxkhgz` VALUES (1, 'A1', '00000C', 'A', 'A-1', 'A-1-1', '项目经费信息额度1', 'XMJFXX', 'JHJFZE > 10000', '1.5', '', 'KHJGMX', '测试');
INSERT INTO `kh_jxkhgz` VALUES (2, 'A2', '00000C', 'A', 'A-1', 'A-1-2', '项目经费信息额度', 'XMJFXX', 'JHJFZE > 10000', '21.5', '%(XMBH)s', 'KHJGMX', '测试');
COMMIT;

-- ----------------------------
-- Table structure for kh_khjgmx
-- ----------------------------
DROP TABLE IF EXISTS `kh_khjgmx`;
CREATE TABLE `kh_khjgmx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JZGH` varchar(16) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `GZH` varchar(128) DEFAULT NULL,
  `KHNF` datetime DEFAULT NULL,
  `KHJD` float DEFAULT NULL,
  `KHMX` text,
  `note` varchar(2056) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_khjgmx
-- ----------------------------
BEGIN;
INSERT INTO `kh_khjgmx` VALUES (5, '00001B', '00000C', 'A1', '2021-02-10 13:35:27', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (6, '00001B', '00000C', 'A1', '2021-02-10 13:35:27', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (7, '00001B', '00000C', 'A2', '2021-02-10 13:35:27', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (8, '00001B', '00000C', 'A2', '2021-02-10 13:35:27', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (9, '00001B', '00000C', 'A1', '2021-02-10 13:37:53', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (10, '00001B', '00000C', 'A1', '2021-02-10 13:37:53', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (11, '00001B', '00000C', 'A2', '2021-02-10 13:37:53', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (12, '00001B', '00000C', 'A2', '2021-02-10 13:37:53', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (13, '00001B', '00000C', 'A1', '2021-02-10 13:38:12', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (14, '00001B', '00000C', 'A1', '2021-02-10 13:38:12', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (15, '00001B', '00000C', 'A2', '2021-02-10 13:38:12', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (16, '00001B', '00000C', 'A2', '2021-02-10 13:38:12', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (17, '00001B', '00000C', 'A1', '2021-02-10 13:38:27', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (18, '00001B', '00000C', 'A1', '2021-02-10 13:38:27', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (19, '00001B', '00000C', 'A2', '2021-02-10 13:38:27', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (20, '00001B', '00000C', 'A2', '2021-02-10 13:38:27', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (21, '00001B', '00000C', 'A1', '2021-02-10 13:51:19', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (22, '00001B', '00000C', 'A1', '2021-02-10 13:51:19', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (23, '00001B', '00000C', 'A2', '2021-02-10 13:51:19', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (24, '00001B', '00000C', 'A2', '2021-02-10 13:51:19', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (25, '00001B', '00000C', 'A1', '2021-02-10 13:51:19', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (26, '00001B', '00000C', 'A1', '2021-02-10 13:51:19', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (27, '00001B', '00000C', 'A2', '2021-02-10 13:51:19', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (28, '00001B', '00000C', 'A2', '2021-02-10 13:51:19', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (29, '00001B', '00000C', 'A1', '2021-02-10 13:51:19', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (30, '00001B', '00000C', 'A1', '2021-02-10 13:51:19', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (31, '00001B', '00000C', 'A2', '2021-02-10 13:51:19', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (32, '00001B', '00000C', 'A2', '2021-02-10 13:51:19', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (33, '00001B', '00000C', 'A1', '2021-02-18 11:03:45', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (34, '00001B', '00000C', 'A1', '2021-02-18 11:03:45', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (35, '00001B', '00000C', 'A2', '2021-02-18 11:03:45', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (36, '00001B', '00000C', 'A2', '2021-02-18 11:03:45', 21.5, 'BH8888', '');
INSERT INTO `kh_khjgmx` VALUES (37, '00001B', '00000C', 'A1', '2021-02-18 12:32:09', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (38, '00001B', '00000C', 'A1', '2021-02-18 12:32:09', 1.5, '', '');
INSERT INTO `kh_khjgmx` VALUES (39, '00001B', '00000C', 'A2', '2021-02-18 12:32:09', 21.5, 'BH8887', '');
INSERT INTO `kh_khjgmx` VALUES (40, '00001B', '00000C', 'A2', '2021-02-18 12:32:09', 21.5, 'BH8888', '');
COMMIT;

-- ----------------------------
-- View structure for view_jxkhgz
-- ----------------------------
DROP VIEW IF EXISTS `view_jxkhgz`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_jxkhgz` AS select `kh`.`id` AS `id`,`kh`.`GZH` AS `GZH`,`kh`.`DWH` AS `DWH`,`kh`.`KHLX` AS `KHLX`,`kh`.`KHZL` AS `KHZL`,`kh`.`XXKLZL` AS `XXKLZL`,`kh`.`KHMC` AS `KHMC`,`kh`.`KHSJDX` AS `KHSJDX`,`kh`.`GZTJ` AS `GZTJ`,`kh`.`JXFSJS` AS `JXFSJS`,`kh`.`KHMXMB` AS `KHMXMB`,`kh`.`KHJGDX` AS `KHJGDX`,`kh`.`note` AS `note` from `kh_jxkhgz` `kh` where (1 = 1);

-- ----------------------------
-- View structure for view_jzgjcsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_jzgjcsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_jzgjcsjxx` AS select `dr`.`id` AS `id`,`dr`.`JZGH` AS `JZGH`,`dr`.`DWH` AS `DWH`,`dr`.`XM` AS `XM`,`dr`.`YWXM` AS `YWXM`,`dr`.`XMPY` AS `XMPY`,`dr`.`CYM` AS `CYM`,`dr`.`XBM` AS `XBM`,`dr`.`CSRQ` AS `CSRQ`,`dr`.`CSDM` AS `CSDM`,`dr`.`BZLBM` AS `BZLBM`,`dr`.`JZGLBM` AS `JZGLBM`,`dr`.`DQZTM` AS `DQZTM`,`dr`.`stamp` AS `stamp`,`dr`.`note` AS `note` from (`dr_jzgjcsjxx` `dr` left join `dc_jzgjcsjxx` `dc` on((`dc`.`JZGH` = `dr`.`JZGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_khjgmx
-- ----------------------------
DROP VIEW IF EXISTS `view_khjgmx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_khjgmx` AS select `kh`.`id` AS `id`,`kh`.`JZGH` AS `JZGH`,`kh`.`DWH` AS `DWH`,`kh`.`GZH` AS `GZH`,`kh`.`KHNF` AS `KHNF`,`kh`.`KHJD` AS `KHJD`,`kh`.`KHMX` AS `KHMX`,`kh`.`note` AS `note` from `kh_khjgmx` `kh` where (1 = 1);

-- ----------------------------
-- View structure for view_sysuser
-- ----------------------------
DROP VIEW IF EXISTS `view_sysuser`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_sysuser` AS select `su`.`id` AS `id`,`su`.`payroll` AS `payroll`,`su`.`password` AS `password`,`su`.`time_pwd` AS `time_pwd`,`su`.`role_id` AS `role_id`,`su`.`usertype_id` AS `usertype_id`,`ro`.`role_name` AS `role_name`,`jg`.`JZGH` AS `JZGH`,`jg`.`XM` AS `XM`,`jg`.`DWH` AS `DWH`,`zz`.`DWMC` AS `DWMC` from (((`jx_sysuser` `su` left join `jx_role` `ro` on((`ro`.`id` = `su`.`role_id`))) left join `view_jzgjcsjxx` `jg` on((`jg`.`JZGH` = `su`.`payroll`))) left join `view_zzjgjbsjxx` `zz` on((`zz`.`DWH` = `jg`.`DWH`)));

-- ----------------------------
-- View structure for view_xmjfxx
-- ----------------------------
DROP VIEW IF EXISTS `view_xmjfxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_xmjfxx` AS select `dr`.`id` AS `id`,`dr`.`JHJFZE` AS `JHJFZE`,`dr`.`XMJFLYM` AS `XMJFLYM`,`dr`.`BRRQ` AS `BRRQ`,`dr`.`BKS` AS `BKS`,`dr`.`ZCRQ` AS `ZCRQ`,`dr`.`BFXZDWJF` AS `BFXZDWJF`,`dr`.`XMPZBH` AS `XMPZBH`,`dr`.`JBRXM` AS `JBRXM`,`dr`.`XMBH` AS `XMBH`,`dr`.`ZZKS` AS `ZZKS`,`jz`.`JZGH` AS `JZGH`,`jz`.`DWH` AS `DWH`,`dr`.`BRRQ` AS `stamp`,`dr`.`note` AS `note` from ((`dr_xmjfxx` `dr` left join `dc_xmjfxx` `dc` on((`dc`.`XMBH` = `dr`.`XMBH`))) left join `dr_jzgjcsjxx` `jz` on((`jz`.`JZGH` = `dr`.`JZGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_zzjgjbsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_zzjgjbsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_zzjgjbsjxx` AS select `dr`.`id` AS `id`,`dr`.`DWH` AS `DWH`,`dr`.`DWMC` AS `DWMC`,`dr`.`DWYWMC` AS `DWYWMC`,`dr`.`DWJC` AS `DWJC`,`dr`.`DWYWJC` AS `DWYWJC`,`dr`.`DWJP` AS `DWJP`,`dr`.`DWDZ` AS `DWDZ`,`dr`.`SZXQ` AS `SZXQ`,`dr`.`LSDWH` AS `LSDWH`,`dr`.`DWLBM` AS `DWLBM`,`dr`.`DWBBM` AS `DWBBM`,`dr`.`DWYXBS` AS `DWYXBS`,`dr`.`SXRQ` AS `SXRQ`,`dr`.`SFST` AS `SFST`,`dr`.`JLNY` AS `JLNY`,`dr`.`DWFZRH` AS `DWFZRH`,`dr`.`stamp` AS `stamp`,`dr`.`note` AS `note` from (`dr_zzjgjbsjxx` `dr` left join `dc_zzjgjbsjxx` `dc` on((`dc`.`DWH` = `dr`.`DWH`))) where (1 = 1);

SET FOREIGN_KEY_CHECKS = 1;
