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

 Date: 14/05/2021 15:18:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for KH_KHJGHZ
-- ----------------------------
DROP TABLE IF EXISTS `kh_khjghz`;
CREATE TABLE `kh_khjghz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `KHNF` datetime DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `LSDWH` varchar(16) DEFAULT NULL,
  `JZGH` varchar(16) DEFAULT NULL,
  `GZH` varchar(128) DEFAULT NULL,
  `KHJDHJ` float DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(2056) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_kh_khjghz_dwh_khnf_gzh_jzgh_uc` (`DWH`,`KHNF`,`GZH`,`JZGH`)
) ENGINE=InnoDB AUTO_INCREMENT=325 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_khjghz
-- ----------------------------
BEGIN;
INSERT INTO `kh_khjghz` VALUES (312, '2021-01-01 00:00:00', '00000C', '00000A', '00001B', '', 72025, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (313, '2021-01-01 00:00:00', '00000C', '00000A', '', 'ZJ-1', 20, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (314, '2021-01-01 00:00:00', '00000A', '', '', 'ZJ-1', 20, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (315, '2021-01-01 00:00:00', '00000C', '00000A', '', '', 72025, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (316, '2021-01-01 00:00:00', '00000A', '', '', '', 72045, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (317, '2021-01-01 00:00:00', '00000C', '00000A', '', 'A1', 3, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (318, '2021-01-01 00:00:00', '00000A', '', '', 'A1', 3, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (319, '2021-01-01 00:00:00', '00000C', '00000A', '', 'A2', 72002, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (320, '2021-01-01 00:00:00', '00000A', '', '', 'A2', 72002, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (321, '2021-01-01 00:00:00', '00000B', '00000A', '00001B', '', 20, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (322, '2021-01-01 00:00:00', '00000B', '00000A', '', 'XX-002', 20, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (323, '2021-01-01 00:00:00', '00000A', '', '', 'XX-002', 20, '2021-05-14 06:08:05.000000', '');
INSERT INTO `kh_khjghz` VALUES (324, '2021-01-01 00:00:00', '00000B', '00000A', '', '', 20, '2021-05-14 06:08:05.000000', '');
COMMIT;

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
INSERT INTO `auth_user` VALUES (1, 'pbkdf2_sha256$260000$wh6XRnJQ0nauYs8cOLnB0h$mzfCMjHKR6kpAL7cUVOxunRqQO8niLFXvQMz3Zr1Rgk=', '2021-04-07 21:52:05.015143', 0, 'why', '', '', '', 0, 1, '2021-02-06 21:48:07.200536');
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
-- Table structure for dc_bjsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_bjsjxx`;
CREATE TABLE `dc_bjsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `BH` varchar(16) DEFAULT NULL,
  `BJ` varchar(16) DEFAULT NULL,
  `JBNY` datetime DEFAULT NULL,
  `RXNF` datetime DEFAULT NULL,
  `FDYH` varchar(16) DEFAULT NULL,
  `BDS` varchar(16) DEFAULT NULL,
  `SSXY` varchar(16) DEFAULT NULL,
  `SSZY` varchar(16) DEFAULT NULL,
  `XSLB` varchar(16) DEFAULT NULL,
  `QYBZ` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_bjsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_bks_jpkc
-- ----------------------------
DROP TABLE IF EXISTS `dc_bks_jpkc`;
CREATE TABLE `dc_bks_jpkc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `KCH` varchar(16) DEFAULT NULL,
  `KCMC` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `FZRGH` varchar(16) DEFAULT NULL,
  `FZRXM` varchar(16) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `KCH` (`KCH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_bks_jpkc
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_hjcgjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_hjcgjbsjxx`;
CREATE TABLE `dc_hjcgjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `HJCGBH` varchar(16) DEFAULT NULL,
  `HJCGMC` varchar(16) DEFAULT NULL,
  `XMLYM` varchar(16) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `HJRQ` datetime DEFAULT NULL,
  `CGHJLBM` varchar(16) DEFAULT NULL,
  `KJJLB` varchar(16) DEFAULT NULL,
  `JLDJM` varchar(16) DEFAULT NULL,
  `HJJBM` varchar(16) DEFAULT NULL,
  `XKLYM` varchar(16) DEFAULT NULL,
  `BJDW` varchar(16) DEFAULT NULL,
  `SSXMBH` varchar(16) DEFAULT NULL,
  `DWPM` varchar(16) DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `FZRYH` varchar(16) DEFAULT NULL,
  `FZRXM` varchar(16) DEFAULT NULL,
  `YJXK` varchar(16) DEFAULT NULL,
  `DWMC` varchar(16) DEFAULT NULL,
  `YJSMC` varchar(16) DEFAULT NULL,
  `CGXS` varchar(16) DEFAULT NULL,
  `HJMC` varchar(16) DEFAULT NULL,
  `HJBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HJCGBH` (`HJCGBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_hjcgjbsjxx
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
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `JZGH` (`JZGH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_jzgjcsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kcsjsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_kcsjsjxx`;
CREATE TABLE `dc_kcsjsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `SXZS` float DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_kcsjsjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kcsjsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kcsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_kcsjxx`;
CREATE TABLE `dc_kcsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JZGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `KCMC` varchar(16) DEFAULT NULL,
  `ZXS` varchar(16) DEFAULT NULL,
  `LLXS` float DEFAULT NULL,
  `SYXS` float DEFAULT NULL,
  `SJXS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `KCH` (`KCH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kcsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kjcgryxx_jl
-- ----------------------------
DROP TABLE IF EXISTS `dc_kjcgryxx_jl`;
CREATE TABLE `dc_kjcgryxx_jl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `ZXZS` varchar(16) DEFAULT NULL,
  `PMZRS` varchar(16) DEFAULT NULL,
  `GXL` float DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `SZDW` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `HJCGBH` varchar(16) DEFAULT NULL,
  `KJCGRYBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_kjcgryxx_jl_ryh_hjcgbh_uc` (`RYH`,`HJCGBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kjcgryxx_jl
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kjcgryxx_lw
-- ----------------------------
DROP TABLE IF EXISTS `dc_kjcgryxx_lw`;
CREATE TABLE `dc_kjcgryxx_lw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `ZXZS` varchar(16) DEFAULT NULL,
  `PMZRS` varchar(16) DEFAULT NULL,
  `GXL` float DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `SZDW` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `LWBH` varchar(16) DEFAULT NULL,
  `KJCGRYBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kjcgryxx_lw
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kjcgryxx_zl
-- ----------------------------
DROP TABLE IF EXISTS `dc_kjcgryxx_zl`;
CREATE TABLE `dc_kjcgryxx_zl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `ZXZS` varchar(16) DEFAULT NULL,
  `PMZRS` varchar(16) DEFAULT NULL,
  `GXL` float DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `SZDW` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `ZLCGBH` varchar(16) DEFAULT NULL,
  `KJCGRYBH` varchar(16) DEFAULT NULL,
  `SMSX` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kjcgryxx_zl
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kjlwfbxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_kjlwfbxx`;
CREATE TABLE `dc_kjlwfbxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `KWMC` varchar(16) DEFAULT NULL,
  `LWBH` varchar(16) DEFAULT NULL,
  `FBRQ` datetime DEFAULT NULL,
  `JH` varchar(16) DEFAULT NULL,
  `QH` varchar(16) DEFAULT NULL,
  `LRSJ` datetime DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kjlwfbxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kjlwslqk
-- ----------------------------
DROP TABLE IF EXISTS `dc_kjlwslqk`;
CREATE TABLE `dc_kjlwslqk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `LWBH` varchar(16) DEFAULT NULL,
  `SLLX` varchar(16) DEFAULT NULL,
  `SLBH` varchar(16) DEFAULT NULL,
  `SLSJ` varchar(16) DEFAULT NULL,
  `SLQH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kjlwslqk
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_kjqklwjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_kjqklwjbsjxx`;
CREATE TABLE `dc_kjqklwjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `LWBH` varchar(16) DEFAULT NULL,
  `LWMC` varchar(128) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `LWLXM` varchar(16) DEFAULT NULL,
  `LZLBM` varchar(16) DEFAULT NULL,
  `XKLYM` varchar(16) DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `XMLYM` varchar(16) DEFAULT NULL,
  `ZGYZM` varchar(16) DEFAULT NULL,
  `YZM` varchar(16) DEFAULT NULL,
  `SSXMBH` varchar(16) DEFAULT NULL,
  `SSJSLY` varchar(16) DEFAULT NULL,
  `LZSLQKM` varchar(16) DEFAULT NULL,
  `QTSLQK` varchar(16) DEFAULT NULL,
  `DYZZ` varchar(16) DEFAULT NULL,
  `DYZZBH` varchar(16) DEFAULT NULL,
  `XXSM` varchar(16) DEFAULT NULL,
  `YJXK` varchar(16) DEFAULT NULL,
  `CYRY` varchar(128) DEFAULT NULL,
  `TXZZ` varchar(16) DEFAULT NULL,
  `JSQK` varchar(128) DEFAULT NULL,
  `JQY` varchar(128) DEFAULT NULL,
  `WDWZZPX` varchar(16) DEFAULT NULL,
  `BZXYBJZDSYS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_kjqklwjbsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_ksapxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_ksapxx`;
CREATE TABLE `dc_ksapxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `KSRQ` datetime DEFAULT NULL,
  `KSSC` float DEFAULT NULL,
  `KSFSLXM` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JKRGH` varchar(16) DEFAULT NULL,
  `KSJSH` varchar(16) DEFAULT NULL,
  `JKRXM` varchar(16) DEFAULT NULL,
  `KSRS` varchar(16) DEFAULT NULL,
  `SSXY` varchar(16) DEFAULT NULL,
  `JSSSXY` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_ksapxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_pksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_pksjxx`;
CREATE TABLE `dc_pksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZKJHXS` varchar(16) DEFAULT NULL,
  `SYZS` varchar(16) DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  `WYKCTJM` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `ZLXS` float DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `DWMC` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_pksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`,`SKBJH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_pksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_pkzksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_pkzksjxx`;
CREATE TABLE `dc_pkzksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZKJHXS` float DEFAULT NULL,
  `SYZS` varchar(16) DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  `WYKCTJM` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `DWMC` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_pkzksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`,`SKBJH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_pkzksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_sspksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_sspksjxx`;
CREATE TABLE `dc_sspksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `SXZS` float DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_sspksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_sspksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_sypksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_sypksjxx`;
CREATE TABLE `dc_sypksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `SYZS` float DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_sypksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_sypksjxx
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
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `XMBH` (`XMBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_xmjfxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_xmryxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_xmryxx`;
CREATE TABLE `dc_xmryxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `GZL` float DEFAULT NULL,
  `MNGZYS` float DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `SMSX` varchar(16) DEFAULT NULL,
  `XMBH` varchar(16) DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_xmryxx_xmbh_ryh_uc` (`XMBH`,`RYH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_xmryxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_xnxqxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_xnxqxx`;
CREATE TABLE `dc_xnxqxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JZGH` varchar(16) DEFAULT NULL,
  `XQMC` varchar(16) DEFAULT NULL,
  `XQQSSJ` datetime DEFAULT NULL,
  `XNXQM` varchar(16) DEFAULT NULL,
  `XNDM` varchar(16) DEFAULT NULL,
  `XQDM` varchar(16) DEFAULT NULL,
  `XNMC` varchar(16) DEFAULT NULL,
  `QSSKZ` varchar(16) DEFAULT NULL,
  `ZZSKZ` varchar(16) DEFAULT NULL,
  `XQLXDM` varchar(16) DEFAULT NULL,
  `XQLXMC` varchar(16) DEFAULT NULL,
  `SFDQXQ` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_sypksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`XNDM`,`XQDM`,`XQQSSJ`),
  UNIQUE KEY `XQQSSJ` (`XQQSSJ`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_xnxqxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_xwlwxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_xwlwxx`;
CREATE TABLE `dc_xwlwxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `LWTM` varchar(16) DEFAULT NULL,
  `LWQSRQ` datetime DEFAULT NULL,
  `LWZZRQ` datetime DEFAULT NULL,
  `XH` varchar(16) DEFAULT NULL,
  `XSXM` varchar(16) DEFAULT NULL,
  `XSSSXY` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_xwlwxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_yjspksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_yjspksjxx`;
CREATE TABLE `dc_yjspksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZKJHXS` varchar(16) DEFAULT NULL,
  `SYZS` varchar(16) DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  `WYKCTJM` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_yjspksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_yjspksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_zdbylwsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_zdbylwsjxx`;
CREATE TABLE `dc_zdbylwsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `JZGH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `ZDZS` float DEFAULT NULL,
  `XQ` datetime DEFAULT NULL,
  `ZDPTXSS` float DEFAULT NULL,
  `ZDSYXSS` float DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_zdbylwsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_zlcgjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_zlcgjbsjxx`;
CREATE TABLE `dc_zlcgjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ZLCGBH` varchar(16) DEFAULT NULL,
  `ZLCGMC` varchar(128) DEFAULT NULL,
  `DWH` varchar(128) DEFAULT NULL,
  `SQBH` varchar(16) DEFAULT NULL,
  `XKLYM` varchar(16) DEFAULT NULL,
  `ZLLXM` varchar(16) DEFAULT NULL,
  `PZRQ` datetime DEFAULT NULL,
  `PZXSM` varchar(16) DEFAULT NULL,
  `ZLZSBH` varchar(16) DEFAULT NULL,
  `FLZTM` varchar(16) DEFAULT NULL,
  `JNZLNFRQ` datetime DEFAULT NULL,
  `JNJE` varchar(16) DEFAULT NULL,
  `SSXMBH` varchar(16) DEFAULT NULL,
  `GJDQM` varchar(16) DEFAULT NULL,
  `GJZLZFLH` varchar(16) DEFAULT NULL,
  `PCTHZLGJDQM` varchar(16) DEFAULT NULL,
  `SQGGH` varchar(16) DEFAULT NULL,
  `SQGGRQ` datetime DEFAULT NULL,
  `SQMC` varchar(16) DEFAULT NULL,
  `ZLDLJG` varchar(30) DEFAULT NULL,
  `ZLDLR` varchar(16) DEFAULT NULL,
  `ZLQR` varchar(16) DEFAULT NULL,
  `ZLZZRQ` datetime DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `ZLSQRQ` varchar(16) DEFAULT NULL,
  `ZZM` varchar(16) DEFAULT NULL,
  `ZZBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dc_zlcgjbsjxx_zlcgbh_sqbh_uc` (`ZLCGBH`,`SQBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_zlcgjbsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dc_zlcsxx
-- ----------------------------
DROP TABLE IF EXISTS `dc_zlcsxx`;
CREATE TABLE `dc_zlcsxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CSRQ` datetime DEFAULT NULL,
  `CSJE` float DEFAULT NULL,
  `SSDW` varchar(16) DEFAULT NULL,
  `GJDQM` varchar(16) DEFAULT NULL,
  `BNSJSR` float DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `ZLCGBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_zlcsxx
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
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `DWH` (`DWH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dc_zzjgjbsjxx
-- ----------------------------
BEGIN;
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
INSERT INTO `django_session` VALUES ('lij68n96k1hhl0lqqjcbta95y5itdkwb', '.eJxVjE0OwiAYBe_C2hCgUMCle89A3sePVA1NSrsy3l2bdKHbNzPvxQK2tYat5yVMiZ2ZZKffjRAfue0g3dFuM49zW5eJ-K7wg3Z-nVN-Xg7376Ci1289luRHAaWTRfHewkVRYLwjaJNBcUCKRTolCdblAVrBUFFKCmkNOfb-AAYIOIY:1lU8bF:65PEhlIxtJQtG8l6NNVB6xE_Ki0EMcU7IgUB0Yza9Go', '2021-04-21 21:52:05.017749');
COMMIT;

-- ----------------------------
-- Table structure for dr_bjsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_bjsjxx`;
CREATE TABLE `dr_bjsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `BH` varchar(16) DEFAULT NULL,
  `BJ` varchar(16) DEFAULT NULL,
  `JBNY` datetime DEFAULT NULL,
  `RXNF` datetime DEFAULT NULL,
  `FDYH` varchar(16) DEFAULT NULL,
  `BDS` varchar(16) DEFAULT NULL,
  `SSXY` varchar(16) DEFAULT NULL,
  `SSZY` varchar(16) DEFAULT NULL,
  `XSLB` varchar(16) DEFAULT NULL,
  `QYBZ` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_bjsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_bks_jpkc
-- ----------------------------
DROP TABLE IF EXISTS `dr_bks_jpkc`;
CREATE TABLE `dr_bks_jpkc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `KCH` varchar(16) DEFAULT NULL,
  `KCMC` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `FZRGH` varchar(16) DEFAULT NULL,
  `FZRXM` varchar(16) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `KCH` (`KCH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_bks_jpkc
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_hjcgjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_hjcgjbsjxx`;
CREATE TABLE `dr_hjcgjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `HJCGBH` varchar(16) DEFAULT NULL,
  `HJCGMC` varchar(16) DEFAULT NULL,
  `XMLYM` varchar(16) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `HJRQ` datetime DEFAULT NULL,
  `CGHJLBM` varchar(16) DEFAULT NULL,
  `KJJLB` varchar(16) DEFAULT NULL,
  `JLDJM` varchar(16) DEFAULT NULL,
  `HJJBM` varchar(16) DEFAULT NULL,
  `XKLYM` varchar(16) DEFAULT NULL,
  `BJDW` varchar(16) DEFAULT NULL,
  `SSXMBH` varchar(16) DEFAULT NULL,
  `DWPM` varchar(16) DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `FZRYH` varchar(16) DEFAULT NULL,
  `FZRXM` varchar(16) DEFAULT NULL,
  `YJXK` varchar(16) DEFAULT NULL,
  `DWMC` varchar(16) DEFAULT NULL,
  `YJSMC` varchar(16) DEFAULT NULL,
  `CGXS` varchar(16) DEFAULT NULL,
  `HJMC` varchar(16) DEFAULT NULL,
  `HJBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HJCGBH` (`HJCGBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_hjcgjbsjxx
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
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_jzgjcsjxx
-- ----------------------------
BEGIN;
INSERT INTO `dr_jzgjcsjxx` VALUES (1, 'admin', '00000A', '超级管理员', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2021-02-18 12:14:46.670939');
INSERT INTO `dr_jzgjcsjxx` VALUES (4, '00001B', '00000C', '李四', 'lishi', NULL, NULL, '女', NULL, NULL, NULL, NULL, NULL, '名校', '2021-03-30 07:03:35.203331');
INSERT INTO `dr_jzgjcsjxx` VALUES (5, '000001C', '00000B', '王武', 'ww', NULL, NULL, '男', NULL, NULL, NULL, NULL, NULL, '', '2021-03-30 07:03:59.617772');
INSERT INTO `dr_jzgjcsjxx` VALUES (6, '000001D', '1234', '赵六', 'ZHAO LIU', NULL, NULL, '女', NULL, NULL, NULL, NULL, NULL, '', '2021-03-17 12:55:39.265364');
INSERT INTO `dr_jzgjcsjxx` VALUES (7, '00000S', '00000D', '王二', 'we', 'wr', 'wr', '男', '2021-03-04 00:00:00', '', '', '', '', NULL, '2021-03-30 07:05:58.550906');
INSERT INTO `dr_jzgjcsjxx` VALUES (8, '00XW1306', '00000B', '王洪洋', 'Wang Hongyang', 'WANG HONGYANG', NULL, '男', NULL, NULL, NULL, NULL, NULL, NULL, '2021-05-14 06:09:29.460407');
COMMIT;

-- ----------------------------
-- Table structure for dr_kcsjsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_kcsjsjxx`;
CREATE TABLE `dr_kcsjsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `SXZS` float DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_kcsjsjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kcsjsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_kcsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_kcsjxx`;
CREATE TABLE `dr_kcsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JZGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `KCMC` varchar(16) DEFAULT NULL,
  `ZXS` varchar(16) DEFAULT NULL,
  `LLXS` float DEFAULT NULL,
  `SYXS` float DEFAULT NULL,
  `SJXS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `KCH` (`KCH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kcsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_kjcgryxx_jl
-- ----------------------------
DROP TABLE IF EXISTS `dr_kjcgryxx_jl`;
CREATE TABLE `dr_kjcgryxx_jl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `ZXZS` varchar(16) DEFAULT NULL,
  `PMZRS` varchar(16) DEFAULT NULL,
  `GXL` float DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `SZDW` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `HJCGBH` varchar(16) DEFAULT NULL,
  `KJCGRYBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_kjcgryxx_jl_ryh_hjcgbh_uc` (`RYH`,`HJCGBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kjcgryxx_jl
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_kjcgryxx_lw
-- ----------------------------
DROP TABLE IF EXISTS `dr_kjcgryxx_lw`;
CREATE TABLE `dr_kjcgryxx_lw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `ZXZS` varchar(16) DEFAULT NULL,
  `PMZRS` varchar(16) DEFAULT NULL,
  `GXL` float DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `SZDW` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `LWBH` varchar(16) DEFAULT NULL,
  `KJCGRYBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kjcgryxx_lw
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_kjcgryxx_zl
-- ----------------------------
DROP TABLE IF EXISTS `dr_kjcgryxx_zl`;
CREATE TABLE `dr_kjcgryxx_zl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `ZXZS` varchar(16) DEFAULT NULL,
  `PMZRS` varchar(16) DEFAULT NULL,
  `GXL` float DEFAULT NULL,
  `XM` varchar(16) DEFAULT NULL,
  `SZDW` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `ZLCGBH` varchar(16) DEFAULT NULL,
  `KJCGRYBH` varchar(16) DEFAULT NULL,
  `SMSX` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kjcgryxx_zl
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_kjlwfbxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_kjlwfbxx`;
CREATE TABLE `dr_kjlwfbxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `KWMC` varchar(16) DEFAULT NULL,
  `LWBH` varchar(16) DEFAULT NULL,
  `FBRQ` datetime DEFAULT NULL,
  `JH` varchar(16) DEFAULT NULL,
  `QH` varchar(16) DEFAULT NULL,
  `LRSJ` datetime DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kjlwfbxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_kjlwslqk
-- ----------------------------
DROP TABLE IF EXISTS `dr_kjlwslqk`;
CREATE TABLE `dr_kjlwslqk` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `LWBH` varchar(16) DEFAULT NULL,
  `SLLX` varchar(16) DEFAULT NULL,
  `SLBH` varchar(16) DEFAULT NULL,
  `SLSJ` varchar(16) DEFAULT NULL,
  `SLQH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kjlwslqk
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_kjqklwjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_kjqklwjbsjxx`;
CREATE TABLE `dr_kjqklwjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `LWBH` varchar(16) DEFAULT NULL,
  `LWMC` varchar(128) DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `LWLXM` varchar(16) DEFAULT NULL,
  `LZLBM` varchar(16) DEFAULT NULL,
  `XKLYM` varchar(16) DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `XMLYM` varchar(16) DEFAULT NULL,
  `ZGYZM` varchar(16) DEFAULT NULL,
  `YZM` varchar(16) DEFAULT NULL,
  `SSXMBH` varchar(16) DEFAULT NULL,
  `SSJSLY` varchar(16) DEFAULT NULL,
  `LZSLQKM` varchar(16) DEFAULT NULL,
  `QTSLQK` varchar(16) DEFAULT NULL,
  `DYZZ` varchar(16) DEFAULT NULL,
  `DYZZBH` varchar(16) DEFAULT NULL,
  `XXSM` varchar(16) DEFAULT NULL,
  `YJXK` varchar(16) DEFAULT NULL,
  `CYRY` varchar(128) DEFAULT NULL,
  `TXZZ` varchar(16) DEFAULT NULL,
  `JSQK` varchar(128) DEFAULT NULL,
  `JQY` varchar(128) DEFAULT NULL,
  `WDWZZPX` varchar(16) DEFAULT NULL,
  `BZXYBJZDSYS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_kjqklwjbsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_ksapxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_ksapxx`;
CREATE TABLE `dr_ksapxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `KSRQ` datetime DEFAULT NULL,
  `KSSC` float DEFAULT NULL,
  `KSFSLXM` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JKRGH` varchar(16) DEFAULT NULL,
  `KSJSH` varchar(16) DEFAULT NULL,
  `JKRXM` varchar(16) DEFAULT NULL,
  `KSRS` varchar(16) DEFAULT NULL,
  `SSXY` varchar(16) DEFAULT NULL,
  `JSSSXY` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_ksapxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_pksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_pksjxx`;
CREATE TABLE `dr_pksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZKJHXS` varchar(16) DEFAULT NULL,
  `SYZS` varchar(16) DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  `WYKCTJM` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `ZLXS` float DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `DWMC` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_pksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`,`SKBJH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_pksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_pkzksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_pkzksjxx`;
CREATE TABLE `dr_pkzksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZKJHXS` float DEFAULT NULL,
  `SYZS` varchar(16) DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  `WYKCTJM` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `DWH` varchar(16) DEFAULT NULL,
  `DWMC` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_pkzksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`,`SKBJH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_pkzksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_sspksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_sspksjxx`;
CREATE TABLE `dr_sspksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `SXZS` float DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` float DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_sspksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_sspksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_sypksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_sypksjxx`;
CREATE TABLE `dr_sypksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `SYZS` float DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_sypksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_sypksjxx
-- ----------------------------
BEGIN;
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
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_xmjfxx
-- ----------------------------
BEGIN;
INSERT INTO `dr_xmjfxx` VALUES (1, 18001, '12', '2020-02-01 00:00:00', 20000, '1970-01-01 00:00:00', 0, 'XS12344', '李四', 'BH8888', 9000, '00001B', NULL, '2021-03-15 06:34:47.746371');
INSERT INTO `dr_xmjfxx` VALUES (3, 18000, '12', '2020-02-01 00:00:00', 20001, '1970-01-01 00:00:00', 0, 'XS12344', '李四', 'BH8877', 9000, '00001B', NULL, '2021-03-11 18:08:52.270447');
INSERT INTO `dr_xmjfxx` VALUES (4, 18000, '12', '2021-02-01 00:00:00', 20001, '1970-01-01 00:00:00', 0, 'XS12344', '李四', 'BH8879', 9000, '00001B', NULL, '2021-03-15 06:36:38.414020');
INSERT INTO `dr_xmjfxx` VALUES (5, 10, 'qwe', '2021-03-02 00:00:00', 110, '2021-03-10 00:00:00', 340, 'sg', 'adsg', 'BH8765', 10, '00XW1306', NULL, '2021-03-15 12:18:19.846104');
INSERT INTO `dr_xmjfxx` VALUES (6, 0, 'rrr', '2021-03-02 00:00:00', 0, '2021-03-04 00:00:00', 0, '222', '222', '2222', 0, '00001B', NULL, '2021-03-15 12:24:23.927505');
INSERT INTO `dr_xmjfxx` VALUES (10, 100000, 'LN0001', '2021-03-02 00:00:00', 100000, '2021-03-02 00:00:00', 0, 'LN0001-01', '王武', 'XX0001', 9999, '000001C', NULL, '2021-03-17 03:27:18.585589');
INSERT INTO `dr_xmjfxx` VALUES (11, 100000, 'LN00002', '2021-03-17 00:00:00', 110000, '2021-03-17 00:00:00', 0, 'LN0002-1', '王武', 'XX0002', 9990, '000001C', NULL, '2021-03-17 03:26:53.208529');
COMMIT;

-- ----------------------------
-- Table structure for dr_xmryxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_xmryxx`;
CREATE TABLE `dr_xmryxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `RYH` varchar(16) DEFAULT NULL,
  `GZL` float DEFAULT NULL,
  `MNGZYS` float DEFAULT NULL,
  `JSM` varchar(16) DEFAULT NULL,
  `RYLX` varchar(16) DEFAULT NULL,
  `SMSX` varchar(16) DEFAULT NULL,
  `XMBH` varchar(16) DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_xmryxx_xmbh_ryh_uc` (`XMBH`,`RYH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_xmryxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_xnxqxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_xnxqxx`;
CREATE TABLE `dr_xnxqxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JZGH` varchar(16) DEFAULT NULL,
  `XQMC` varchar(16) DEFAULT NULL,
  `XQQSSJ` datetime DEFAULT NULL,
  `XNXQM` varchar(16) DEFAULT NULL,
  `XNDM` varchar(16) DEFAULT NULL,
  `XQDM` varchar(16) DEFAULT NULL,
  `XNMC` varchar(16) DEFAULT NULL,
  `QSSKZ` varchar(16) DEFAULT NULL,
  `ZZSKZ` varchar(16) DEFAULT NULL,
  `XQLXDM` varchar(16) DEFAULT NULL,
  `XQLXMC` varchar(16) DEFAULT NULL,
  `SFDQXQ` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_sypksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`XNDM`,`XQDM`,`XQQSSJ`),
  UNIQUE KEY `XQQSSJ` (`XQQSSJ`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_xnxqxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_xwlwxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_xwlwxx`;
CREATE TABLE `dr_xwlwxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `LWTM` varchar(16) DEFAULT NULL,
  `LWQSRQ` datetime DEFAULT NULL,
  `LWZZRQ` datetime DEFAULT NULL,
  `XH` varchar(16) DEFAULT NULL,
  `XSXM` varchar(16) DEFAULT NULL,
  `XSSSXY` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_xwlwxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_yjspksjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_yjspksjxx`;
CREATE TABLE `dr_yjspksjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `JSGH` varchar(16) DEFAULT NULL,
  `KCH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `KKXND` varchar(16) DEFAULT NULL,
  `SKBJH` varchar(16) DEFAULT NULL,
  `KKXQM` datetime DEFAULT NULL,
  `ZXXS` varchar(16) DEFAULT NULL,
  `ZKJHXS` varchar(16) DEFAULT NULL,
  `SYZS` varchar(16) DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  `WYKCTJM` varchar(16) DEFAULT NULL,
  `KCJBM` varchar(16) DEFAULT NULL,
  `ZLXS` varchar(16) DEFAULT NULL,
  `HBS` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_yjspksjxx_jsgh_kch_kkxnd_kkxqm_skbjh_uc` (`JSGH`,`KCH`,`KKXND`,`KKXQM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_yjspksjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_zdbylwsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_zdbylwsjxx`;
CREATE TABLE `dr_zdbylwsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  `JZGH` varchar(16) DEFAULT NULL,
  `JSXM` varchar(16) DEFAULT NULL,
  `ZDZS` float DEFAULT NULL,
  `XQ` datetime DEFAULT NULL,
  `ZDPTXSS` float DEFAULT NULL,
  `ZDSYXSS` float DEFAULT NULL,
  `JXMSJBM` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_zdbylwsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_zlcgjbsjxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_zlcgjbsjxx`;
CREATE TABLE `dr_zlcgjbsjxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ZLCGBH` varchar(16) DEFAULT NULL,
  `ZLCGMC` varchar(128) DEFAULT NULL,
  `DWH` varchar(128) DEFAULT NULL,
  `SQBH` varchar(16) DEFAULT NULL,
  `XKLYM` varchar(16) DEFAULT NULL,
  `ZLLXM` varchar(16) DEFAULT NULL,
  `PZRQ` datetime DEFAULT NULL,
  `PZXSM` varchar(16) DEFAULT NULL,
  `ZLZSBH` varchar(16) DEFAULT NULL,
  `FLZTM` varchar(16) DEFAULT NULL,
  `JNZLNFRQ` datetime DEFAULT NULL,
  `JNJE` varchar(16) DEFAULT NULL,
  `SSXMBH` varchar(16) DEFAULT NULL,
  `GJDQM` varchar(16) DEFAULT NULL,
  `GJZLZFLH` varchar(16) DEFAULT NULL,
  `PCTHZLGJDQM` varchar(16) DEFAULT NULL,
  `SQGGH` varchar(16) DEFAULT NULL,
  `SQGGRQ` datetime DEFAULT NULL,
  `SQMC` varchar(16) DEFAULT NULL,
  `ZLDLJG` varchar(30) DEFAULT NULL,
  `ZLDLR` varchar(16) DEFAULT NULL,
  `ZLQR` varchar(16) DEFAULT NULL,
  `ZLZZRQ` datetime DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `ZLSQRQ` varchar(16) DEFAULT NULL,
  `ZZM` varchar(16) DEFAULT NULL,
  `ZZBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_dr_zlcgjbsjxx_zlcgbh_sqbh_uc` (`ZLCGBH`,`SQBH`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_zlcgjbsjxx
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for dr_zlcsxx
-- ----------------------------
DROP TABLE IF EXISTS `dr_zlcsxx`;
CREATE TABLE `dr_zlcsxx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CSRQ` datetime DEFAULT NULL,
  `CSJE` float DEFAULT NULL,
  `SSDW` varchar(16) DEFAULT NULL,
  `GJDQM` varchar(16) DEFAULT NULL,
  `BNSJSR` float DEFAULT NULL,
  `XKMLKJM` varchar(16) DEFAULT NULL,
  `ZLCGBH` varchar(16) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of dr_zlcsxx
-- ----------------------------
BEGIN;
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
INSERT INTO `dr_zzjgjbsjxx` VALUES (13, '00000D', '金属研究所', 'ITC', '', '', '', '', '', '00000C', '', '', '', '2099-12-31 00:00:00', '', '1954-01-01 00:00:00', '', '', '2021-03-28 13:56:12.904036');
INSERT INTO `dr_zzjgjbsjxx` VALUES (14, '1234', '机器人研究所', '', '机器人', '', '', '', '', '00000B', '', '', '', '2021-01-01 00:00:00', '', '1920-01-01 00:00:00', '', '', '2021-03-17 02:45:15.226933');
INSERT INTO `dr_zzjgjbsjxx` VALUES (28, '00000A', '东北大学', 'NEU', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2099-12-31 00:00:00', NULL, '1909-01-01 00:00:00', NULL, '985', '2021-02-18 12:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (29, '00000B', '信息工程学院', 'ITC', '信息', '', '', '', '', '00000A', '', '', NULL, '2099-01-01 00:00:00', '', '1909-01-01 00:00:00', '', '名校', '2021-02-18 12:14:40.767352');
INSERT INTO `dr_zzjgjbsjxx` VALUES (30, '00000C', '冶金工程学院', 'MTC', '冶金', NULL, NULL, NULL, NULL, '00000A', NULL, NULL, NULL, '2099-12-31 00:00:00', NULL, '1935-01-01 00:00:00', NULL, '', '2021-05-14 05:15:52.930510');
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
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jx_menu
-- ----------------------------
BEGIN;
INSERT INTO `jx_menu` VALUES (1, '角色管理', '系统管理', '/jx/role_manage/', 'z11');
INSERT INTO `jx_menu` VALUES (2, '权限分配', '系统管理', '/jx/role_assign/', 'z12');
INSERT INTO `jx_menu` VALUES (3, '组织机构基本数据信息', '公共管理', '/jx/base/zzjgjbsjxx/', '211');
INSERT INTO `jx_menu` VALUES (4, '教职工基础数据信息', '公共管理', '/jx/base/jzgjcsjxx/', '212');
INSERT INTO `jx_menu` VALUES (5, '项目经费信息', '科研管理', '/jx/base/xmjfxx/', '611');
INSERT INTO `jx_menu` VALUES (6, '考核批次', '系统管理', '/jx/khpc/', 'y11');
INSERT INTO `jx_menu` VALUES (7, '绩效考核规则', '系统管理', '/jx/jxkhgz/', 'y12');
INSERT INTO `jx_menu` VALUES (8, '考核规则定制', '系统管理', '/jx/khgzdz/', 'y13');
INSERT INTO `jx_menu` VALUES (9, '绩效考核结果', '系统管理', '/jx/khjgmx/', 'y14');
INSERT INTO `jx_menu` VALUES (10, '考核结果汇总', '系统管理', '/jx/khjghz/', 'y15');
INSERT INTO `jx_menu` VALUES (12, '不参与考核', '系统管理', '/jx/bcykh/', 'y16');
INSERT INTO `jx_menu` VALUES (13, '获奖成果基本数据信息', '科研管理', '/jx/base/hjcgjbsjxx/', '612');
INSERT INTO `jx_menu` VALUES (14, '项目人员信息', '科研管理', '/jx/base/xmryxx/', '623');
INSERT INTO `jx_menu` VALUES (15, '科技成果(获奖成果)人员信息', '科研管理', '/jx/base/kjcgryxx_jl/', '630');
INSERT INTO `jx_menu` VALUES (16, '科技成果(论文)人员信息', '科研管理', '/jx/base/kjcgryxx_lw/', '631');
INSERT INTO `jx_menu` VALUES (17, '本科生教学总学时', '教学管理', '/jx/base/bksjxzxs/', '400');
INSERT INTO `jx_menu` VALUES (18, '实习学时数', '教学管理', '/jx/base/sxxss/', '401');
INSERT INTO `jx_menu` VALUES (19, '指导实验学时数', '教学管理', '/jx/base/zdsyxss/', '402');
INSERT INTO `jx_menu` VALUES (20, '监考学时数', '教学管理', '/jx/base/jkxss/', '403');
INSERT INTO `jx_menu` VALUES (21, '专利', '科研管理', '/jx/base/zlcgjbsjxx/', '633');
INSERT INTO `jx_menu` VALUES (22, '学术会议信息', '科研管理', '/jx/base/xshyxx/', '632');
INSERT INTO `jx_menu` VALUES (23, '教材基本数据信息', '教学管理', '/jx/base/jcjbsjxx/', '404');
INSERT INTO `jx_menu` VALUES (24, '专著及学术译著工作量', '科研管理', '/jx/base/kjcgryxx_zz/', '634');
INSERT INTO `jx_menu` VALUES (25, '指导毕业论文学时数', '教学管理', '/jx/base/zdbylwxss/', '405');
INSERT INTO `jx_menu` VALUES (26, '学期学年信息', '教学管理', '/jx/base/xnxqxx/', '424');
INSERT INTO `jx_menu` VALUES (27, '课程数据信息', '教学管理', '/jx/base/kcsjxx/', '425');
INSERT INTO `jx_menu` VALUES (29, '课程设计学时数', '教学管理', '/jx/base/kcsjxss/', '426');
INSERT INTO `jx_menu` VALUES (30, '研究生理论课学时数', '教学管理', '/jx/base/yjsjxzxs/', '427');
INSERT INTO `jx_menu` VALUES (31, '本科生理论课助课学时数', '教学管理', '/jx/base/bkszkjxzxs/', '428');
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
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8;

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
INSERT INTO `jx_role_menu` VALUES (12, 1, 7, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (13, 1, 8, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (14, 1, 9, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (18, 1, 13, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (21, 1, 10, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (22, 1, 12, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (25, 2, 6, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (26, 2, 3, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (27, 2, 4, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (28, 2, 5, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (29, 2, 7, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (30, 2, 8, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (31, 2, 9, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (32, 2, 10, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (33, 2, 12, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (34, 2, 13, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (35, 2, 2, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (37, 3, 3, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (38, 3, 4, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (39, 3, 5, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (40, 3, 6, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (41, 3, 7, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (42, 3, 8, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (43, 3, 9, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (44, 3, 10, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (45, 3, 12, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (46, 3, 13, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (48, 4, 3, 'n,n,n,y,n,y');
INSERT INTO `jx_role_menu` VALUES (49, 4, 4, 'n,n,y,y,n,y');
INSERT INTO `jx_role_menu` VALUES (50, 4, 5, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (52, 4, 7, 'n,n,n,y,n,n');
INSERT INTO `jx_role_menu` VALUES (53, 4, 8, 'n,n,n,y,n,n');
INSERT INTO `jx_role_menu` VALUES (54, 4, 9, 'n,n,n,y,n,y');
INSERT INTO `jx_role_menu` VALUES (55, 4, 10, 'n,n,n,y,n,n');
INSERT INTO `jx_role_menu` VALUES (56, 4, 12, 'n,n,n,y,n,n');
INSERT INTO `jx_role_menu` VALUES (57, 4, 13, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (58, 4, 6, 'n,n,n,y,n,n');
INSERT INTO `jx_role_menu` VALUES (59, 1, 14, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (60, 1, 15, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (61, 1, 16, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (62, 1, 17, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (63, 1, 18, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (64, 1, 19, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (65, 1, 20, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (66, 1, 21, 'y,y,y,y,y,y');
INSERT INTO `jx_role_menu` VALUES (67, 1, 22, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (68, 1, 23, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (69, 2, 14, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (70, 2, 15, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (71, 2, 16, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (72, 2, 17, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (73, 2, 18, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (74, 2, 19, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (75, 2, 20, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (76, 2, 21, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (77, 2, 22, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (78, 2, 23, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (79, 3, 14, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (80, 3, 15, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (81, 3, 16, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (82, 3, 17, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (83, 3, 18, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (84, 3, 19, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (85, 3, 20, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (86, 3, 21, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (87, 3, 22, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (88, 3, 23, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (89, 1, 24, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (90, 1, 25, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (91, 2, 24, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (92, 2, 25, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (93, 3, 24, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (94, 3, 25, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (95, 4, 14, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (96, 4, 15, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (97, 4, 16, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (98, 4, 17, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (99, 4, 18, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (100, 4, 19, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (101, 4, 20, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (102, 4, 21, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (103, 4, 22, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (104, 4, 23, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (105, 4, 24, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (106, 4, 25, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (107, 3, 2, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (108, 1, 26, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (109, 1, 27, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (110, 1, 29, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (111, 1, 30, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (112, 1, 31, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (113, 2, 26, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (114, 2, 27, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (115, 2, 29, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (116, 2, 30, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (117, 2, 31, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (118, 3, 26, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (119, 3, 27, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (120, 3, 29, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (121, 3, 30, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (122, 3, 31, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (123, 4, 26, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (124, 4, 27, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (125, 4, 29, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (126, 4, 30, 'n,n,n,n,n,n');
INSERT INTO `jx_role_menu` VALUES (127, 4, 31, 'n,n,n,n,n,n');
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of jx_sysuser
-- ----------------------------
BEGIN;
INSERT INTO `jx_sysuser` VALUES (1, '00000S', 'OWIwNWZiOGZjZTM4NjRhMGVkNjVlOTQ3MmRlNTQ2N2Q=', '2021-02-06 23:51:43.981236', 3, 3);
INSERT INTO `jx_sysuser` VALUES (2, 'admin', 'ZjJjYzIwNzFhNzM3MjdjNGY0MTE3ZTRiNTkwYjAzMWM=', '2021-03-21 23:08:54.000000', 1, 1);
INSERT INTO `jx_sysuser` VALUES (3, '00001B', 'OWIwNWZiOGZjZTM4NjRhMGVkNjVlOTQ3MmRlNTQ2N2Q=', '2021-02-06 23:52:14.803931', 2, 2);
INSERT INTO `jx_sysuser` VALUES (4, '000001C', 'OWIwNWZiOGZjZTM4NjRhMGVkNjVlOTQ3MmRlNTQ2N2Q=', '2021-02-08 08:30:49.536812', 2, 2);
INSERT INTO `jx_sysuser` VALUES (5, '000001D', 'OWIwNWZiOGZjZTM4NjRhMGVkNjVlOTQ3MmRlNTQ2N2Q=', '2021-02-09 19:57:47.163106', 4, 4);
INSERT INTO `jx_sysuser` VALUES (6, '00XW1306', 'OWIwNWZiOGZjZTM4NjRhMGVkNjVlOTQ3MmRlNTQ2N2Q=', '2021-03-21 23:08:54.000000', 2, 2);
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
-- Table structure for kh_bcykh
-- ----------------------------
DROP TABLE IF EXISTS `kh_bcykh`;
CREATE TABLE `kh_bcykh` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DWH` varchar(16) DEFAULT NULL,
  `KHNF` datetime DEFAULT NULL,
  `JZGH` varchar(16) DEFAULT NULL,
  `CYZT` enum('不参与','参与') DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(2056) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_kh_bcykh_dwh_khnf_jzgh_uc` (`DWH`,`KHNF`,`JZGH`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_bcykh
-- ----------------------------
BEGIN;
INSERT INTO `kh_bcykh` VALUES (1, '00000C', '2021-01-01 00:00:00', '000001C', '参与', '2021-03-30 07:15:04.545660', NULL);
INSERT INTO `kh_bcykh` VALUES (2, '00000C', '2021-01-01 00:00:00', '00001B', '参与', '2021-03-03 13:57:25.851100', NULL);
INSERT INTO `kh_bcykh` VALUES (3, '00000C', '2021-01-01 00:00:00', '000001D', '参与', '2021-02-28 13:24:30.717130', NULL);
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
  `XXKHZL` varchar(32) DEFAULT NULL,
  `KHMC` varchar(256) DEFAULT NULL,
  `KHSJDX` varchar(64) DEFAULT NULL,
  `GZTJ` varchar(2056) DEFAULT NULL,
  `JXFSJS` varchar(2056) DEFAULT NULL,
  `KHMXMB` text,
  `KHJGDX` varchar(64) DEFAULT NULL,
  `note` varchar(2056) DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`),
  UNIQUE KEY `kh_jxkhgz_UN` (`KHLX`,`KHZL`,`XXKHZL`,`GZH`),
  UNIQUE KEY `kh_jxkhgz_gzh_dwh_uc` (`GZH`,`DWH`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_jxkhgz
-- ----------------------------
BEGIN;
INSERT INTO `kh_jxkhgz` VALUES (1, 'A1', '00000B', 'A', 'A-1', 'A-1-1', '项目经费信息额度1', 'XMJFXX', 'JHJFZE > 10000', '1.5', '%(GZH)s->教职工：%(JZGH)s %(XMBH)s元', 'KHJGMX', '测试', '2021-05-14 07:12:33.128866');
INSERT INTO `kh_jxkhgz` VALUES (2, 'A2', '00000B', 'A', 'A-1', 'A-1-2', '项目经费信息额度', 'XMJFXX', 'JHJFZE > 1000', '2 * JHJFZE', '教职工：%(JZGH)s %(XMBH)s元', 'KHJGMX', '测试', '2021-05-14 07:12:36.404580');
INSERT INTO `kh_jxkhgz` VALUES (4, 'XX-001', '00000C', 'A', 'A-1', 'A-1-3', '项目经费信息额度3', 'XMJFXX', 'JHJFZE == 11000', '0', 'hello world', 'KHJGMX', '', '2021-03-17 03:32:21.418425');
INSERT INTO `kh_jxkhgz` VALUES (5, 'ZJ-1', '00000B', 'ZJ', 'ZZ', 'ZZZ', '增减业绩点', '', '0', '0', '', '', '', '2021-05-14 07:12:40.945631');
INSERT INTO `kh_jxkhgz` VALUES (6, 'XX-001', '00000B', 'AB', 'AB-1', 'AB-1-2', '项目经费信息额度', 'XMJFXX', 'JHJFZE > 100000', '20', '%(GZH)s->教职工：%(JZGH)s', '', '', '2021-03-17 03:37:55.100899');
INSERT INTO `kh_jxkhgz` VALUES (7, 'XX-002', '00000B', 'ABC', 'AB-1', 'AB-1-2', '项目经费信息额度1', 'XMJFXX', 'JHJFZE <= 100000', '10', '%(GZH)s->教职工：%(JZGH)s %(XMBH)s元', '', '', '2021-03-17 03:37:36.940028');
INSERT INTO `kh_jxkhgz` VALUES (8, 'C1-1-1', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'10\' and CGHJLBM==\'01\' and JLDJM==\'1\'', '2000 * GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', '', NULL, '2021-03-07 18:38:04.489486');
INSERT INTO `kh_jxkhgz` VALUES (9, 'C1-1-2', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'10\' and CGHJLBM==\'03\' and JLJBM==\'2\'', '2000*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', '', NULL, '2021-03-07 18:37:12.155462');
INSERT INTO `kh_jxkhgz` VALUES (10, 'C1-1-3', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'10\' and CGHJLBM==\'03\' and JLJBM==\'3\'', '1500*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', NULL, NULL, '2021-03-07 18:37:12.104667');
INSERT INTO `kh_jxkhgz` VALUES (11, 'C1-1-4', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'10\' and CGHJLBM==\'01\' and JLJBM==\'2\'', '1500*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', NULL, NULL, '2021-03-07 18:41:53.648769');
INSERT INTO `kh_jxkhgz` VALUES (12, 'C1-1-5', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'10\' and CGHJLBM==\'02\' and JLJBM==\'2\'', '1500*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', NULL, NULL, '2021-03-07 18:52:13.297528');
INSERT INTO `kh_jxkhgz` VALUES (13, 'C1-1-6', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'10\' and CGHJLBM==\'02\' and JLJBM==\'3\'', '1000*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', NULL, NULL, '2021-03-07 18:52:13.353287');
INSERT INTO `kh_jxkhgz` VALUES (14, 'C1-1-7', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'10\' and CGHJLBM==\'01\' and JLJBM==\'3\'', '1000*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', NULL, NULL, '2021-03-07 18:58:09.234760');
INSERT INTO `kh_jxkhgz` VALUES (15, 'C1-1-8', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'20\' and CGHJLBM==\'01\' and JLJBM==\'2\'', '200*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', NULL, NULL, '2021-03-07 18:58:09.234760');
INSERT INTO `kh_jxkhgz` VALUES (16, 'C1-1-9', '00000B', '学术水平和成果工作量', '科研成果工作量', '获奖成果', '奖励成果', 'KJCGRYXX_JL', 'HJJBM==\'20\' and CGHJLBM==\'01\' and JLJBM==\'3\'', '100*GXL', '负责人教师：%(FZRXM)s,参与项目编号:%(HJCGBH)s,贡献率为：%(GXL)s', NULL, NULL, '2021-03-07 19:00:27.618331');
INSERT INTO `kh_jxkhgz` VALUES (18, 'AX6-1', '00000B', '教学工作量', '一般教学工作量', '指导毕业论文学', '指导毕业论文学时数-1', 'ZDBYLWXSS', 'JXMSJBM==\'1\'', '2*ZDZS*1*(ZDSYXSS+ZDPTXSS*3)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:13:58.251613');
INSERT INTO `kh_jxkhgz` VALUES (19, 'AX8', '00000B', '教学工作量', '一般教学工作量', '监考', '监考学时数', 'JKXSS', 'KSSC>0', '1*KSSC', '监考人姓名：%(JKRXM)s,本次考试所属学院：%(SSXY)s,考试时长：%(KSSC)s', '', NULL, '2021-05-14 07:14:01.100389');
INSERT INTO `kh_jxkhgz` VALUES (20, 'AX6-2', '00000B', '教学工作量', '一般教学工作量', '指导毕业论文学', '指导毕业论文学时数-2', 'ZDBYLWXSS', 'JXMSJBM==\'2\'', '2*ZDZS*2*(ZDSYXSS+ZDPTXSS*3)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:03.509202');
INSERT INTO `kh_jxkhgz` VALUES (21, 'AX6-3', '00000B', '教学工作量', '一般教学工作量', '指导毕业论文学', '指导毕业论文学时数-3', 'ZDBYLWXSS', 'JXMSJBM==\'3\'', '2*ZDZS*3*(ZDSYXSS+ZDPTXSS*3)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:05.383902');
INSERT INTO `kh_jxkhgz` VALUES (22, 'AX3', '00000B', '教学工作量', '一般教学工作量', '实习', '实习学时数', 'SXXSS', 'HBS>0', '48*HBS*SXZS', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:07.310890');
INSERT INTO `kh_jxkhgz` VALUES (23, 'AX4', '00000B', '教学工作量', '一般教学工作量', '课程设计', '课程设计学时数', 'KCSJXSS', 'HBS>0', '20*HBS*SXZS', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:10.916376');
INSERT INTO `kh_jxkhgz` VALUES (24, 'AX1-2-1-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-211', 'BKSJXZXS', 'WYKCTJM==\'2\' and JXMSJBM==\'1\' and KCJBM==\'1\'', 'JHXSS*ZLXS*(1.8+2)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:13.026014');
INSERT INTO `kh_jxkhgz` VALUES (25, 'AX1-1-1-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-111', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'1\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(2+2)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:14.960759');
INSERT INTO `kh_jxkhgz` VALUES (26, 'AX1-3-1-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-311', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'1\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1.6+2)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:17.075396');
INSERT INTO `kh_jxkhgz` VALUES (27, 'AX1-1-2-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-121', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'2\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(2+1.8)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:18.732409');
INSERT INTO `kh_jxkhgz` VALUES (28, 'AX1-1-3-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-131', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'3\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(2+1.6)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:20.299797');
INSERT INTO `kh_jxkhgz` VALUES (29, 'AX1-1-1-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-112', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'1\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(2+2)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:32.045591');
INSERT INTO `kh_jxkhgz` VALUES (30, 'AX1-1-1-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-113', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'1\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(2+2)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:33.414024');
INSERT INTO `kh_jxkhgz` VALUES (31, 'AX1-1-2-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-122', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'2\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(2+1.8)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:34.716973');
INSERT INTO `kh_jxkhgz` VALUES (32, 'AX1-1-2-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-123', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'2\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(2+1.8)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:35.963390');
INSERT INTO `kh_jxkhgz` VALUES (33, 'AX1-1-3-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-132', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'3\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(2+1.6)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:37.195901');
INSERT INTO `kh_jxkhgz` VALUES (34, 'AX1-1-3-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-133', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'3\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(2+1.6)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:38.364256');
INSERT INTO `kh_jxkhgz` VALUES (35, 'AX1-1-9-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-191', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'9\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(2+1)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:39.791978');
INSERT INTO `kh_jxkhgz` VALUES (36, 'AX1-1-9-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-192', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'9\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(2+1)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:41.177747');
INSERT INTO `kh_jxkhgz` VALUES (37, 'AX1-1-9-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-193', 'BKSJXZXS', 'KCJBM==\'1\' and JXMSJBM==\'9\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(2+1)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:42.625021');
INSERT INTO `kh_jxkhgz` VALUES (38, 'AX5-1', '00000B', '教学工作量', '一般教学工作量', '实验', '指导实验学时数-1', 'ZDSYXSS', 'KCJBM==\'1\'', 'SYXS*SYZS*2*0.6', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:43.979212');
INSERT INTO `kh_jxkhgz` VALUES (39, 'AX5-2', '00000B', '教学工作量', '一般教学工作量', '实验', '指导实验学时数-2', 'ZDSYXSS', 'KCJBM==\'2\'', 'SYXS*SYZS*1.8*0.6', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:45.278883');
INSERT INTO `kh_jxkhgz` VALUES (40, 'AX5-3', '00000B', '教学工作量', '一般教学工作量', '实验', '指导实验学时数-3', 'ZDSYXSS', 'KCJBM==\'3\'', 'SYXS*SYZS*1.6*0.6', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:46.586736');
INSERT INTO `kh_jxkhgz` VALUES (41, 'AX5-9', '00000B', '教学工作量', '一般教学工作量', '实验', '指导实验学时数-9', 'ZDSYXSS', 'KCJBM==\'9\'', 'SYXS*SYZS*1*0.6', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:47.894656');
INSERT INTO `kh_jxkhgz` VALUES (42, 'AY1-1-1', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-11', 'YJSJXZXS', 'KCJBM==\'1\' and WYKCTJM==\'1\'', 'JHXSS*2*4', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:49.237405');
INSERT INTO `kh_jxkhgz` VALUES (43, 'AY1-1-2', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-12', 'YJSJXZXS', 'KCJBM==\'1\' and WYKCTJM==\'2\'', 'JHXSS*2*3', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:50.737042');
INSERT INTO `kh_jxkhgz` VALUES (44, 'AY1-1-3', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-13', 'YJSJXZXS', 'KCJBM==\'1\' and WYKCTJM==\'3\'', 'JHXSS*2*1', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:52.106280');
INSERT INTO `kh_jxkhgz` VALUES (45, 'AX6-9', '00000B', '教学工作量', '一般教学工作量', '指导毕业论文学', '指导毕业论文学时数-9', 'ZDBYLWXSS', 'JXMSJBM==\'9\'', '2*ZDZS*9*(ZDSYXSS+ZDPTXSS*3)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:53.636689');
INSERT INTO `kh_jxkhgz` VALUES (46, 'AX2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课助课', '本科生理论课助课学时数', 'BKSZKJXZXS', 'ZKJHXS>0', 'ZKJHXS*0.4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:54.953664');
INSERT INTO `kh_jxkhgz` VALUES (47, 'AY1-2-1', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-21', 'YJSJXZXS', 'KCJBM==\'2\' and WYKCTJM==\'1\'', 'JHXSS*1.8*4', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:56.438173');
INSERT INTO `kh_jxkhgz` VALUES (48, 'AY1-2-2', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-22', 'YJSJXZXS', 'KCJBM==\'2\' and WYKCTJM==\'2\'', 'JHXSS*1.8*3', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:57.989590');
INSERT INTO `kh_jxkhgz` VALUES (49, 'AY1-2-3', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-23', 'YJSJXZXS', 'KCJBM==\'2\' and WYKCTJM==\'3\'', 'JHXSS*1.8*1', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:14:59.657824');
INSERT INTO `kh_jxkhgz` VALUES (50, 'AY1-3-1', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-31', 'YJSJXZXS', 'KCJBM==\'3\' and WYKCTJM==\'1\'', 'JHXSS*1.6*4', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:00.936326');
INSERT INTO `kh_jxkhgz` VALUES (51, 'AY1-3-2', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-32', 'YJSJXZXS', 'KCJBM==\'3\' and WYKCTJM==\'2\'', 'JHXSS*1.6*3', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:02.675254');
INSERT INTO `kh_jxkhgz` VALUES (52, 'AY1-3-3', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-33', 'YJSJXZXS', 'KCJBM==\'3\' and WYKCTJM==\'3\'', 'JHXSS*1.6*1', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:04.791043');
INSERT INTO `kh_jxkhgz` VALUES (53, 'AY1-9-1', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-91', 'YJSJXZXS', 'KCJBM==\'9\' and WYKCTJM==\'1\'', 'JHXSS*1*4', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:06.107316');
INSERT INTO `kh_jxkhgz` VALUES (54, 'AY1-9-2', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-92', 'YJSJXZXS', 'KCJBM==\'9\' and WYKCTJM==\'2\'', 'JHXSS*1*3', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:07.387411');
INSERT INTO `kh_jxkhgz` VALUES (55, 'AY1-9-3', '00000B', '教学工作量', '一般教学工作量', '研究生教学', '研究生理论课学时数-93', 'YJSJXZXS', 'KCJBM==\'9\' and WYKCTJM==\'3\'', 'JHXSS*1*1', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:08.931913');
INSERT INTO `kh_jxkhgz` VALUES (56, 'AX1-2-2-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-221', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'2\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1.8+1.8)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:10.219187');
INSERT INTO `kh_jxkhgz` VALUES (57, 'AX1-2-3-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-231', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'3\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1.8+1.6)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:11.542541');
INSERT INTO `kh_jxkhgz` VALUES (58, 'AX1-2-1-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-212', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'1\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.8+2)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:12.937978');
INSERT INTO `kh_jxkhgz` VALUES (59, 'AX1-2-1-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-213', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'1\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.8+2)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:14.242570');
INSERT INTO `kh_jxkhgz` VALUES (60, 'AX1-2-2-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-222', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'2\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.8+1.8)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:15.672602');
INSERT INTO `kh_jxkhgz` VALUES (61, 'AX1-2-2-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-223', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'2\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.8+1.8)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:17.276067');
INSERT INTO `kh_jxkhgz` VALUES (62, 'AX1-2-3-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-232', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'3\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.8+1.6)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:18.636817');
INSERT INTO `kh_jxkhgz` VALUES (63, 'AX1-2-3-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-233', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'3\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.8+1.6)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:20.039438');
INSERT INTO `kh_jxkhgz` VALUES (64, 'AX1-2-9-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-291', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'9\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1.8+1)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:21.343329');
INSERT INTO `kh_jxkhgz` VALUES (65, 'AX1-2-9-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-292', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'9\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.8+1)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:22.616284');
INSERT INTO `kh_jxkhgz` VALUES (66, 'AX1-2-9-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-293', 'BKSJXZXS', 'KCJBM==\'2\' and JXMSJBM==\'9\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.8+1)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:23.987352');
INSERT INTO `kh_jxkhgz` VALUES (67, 'AX1-3-2-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-321', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'2\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1.6+1.8)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:25.501785');
INSERT INTO `kh_jxkhgz` VALUES (68, 'AX1-3-3-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-331', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'3\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1.6+1.6)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:26.952123');
INSERT INTO `kh_jxkhgz` VALUES (69, 'AX1-3-1-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-312', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'1\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.6+2)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:28.535478');
INSERT INTO `kh_jxkhgz` VALUES (70, 'AX1-3-1-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-313', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'1\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.6+2)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:30.082942');
INSERT INTO `kh_jxkhgz` VALUES (71, 'AX1-3-2-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-322', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'2\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.6+1.8)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:31.589354');
INSERT INTO `kh_jxkhgz` VALUES (72, 'AX1-3-2-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-323', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'2\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.6+1.8)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:33.526775');
INSERT INTO `kh_jxkhgz` VALUES (73, 'AX1-3-9-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-391', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'9\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1.6+1)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:35.110719');
INSERT INTO `kh_jxkhgz` VALUES (74, 'AX1-3-9-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-392', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'9\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.6+1)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:36.624610');
INSERT INTO `kh_jxkhgz` VALUES (75, 'AX1-3-9-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-393', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'9\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.6+1)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:38.141947');
INSERT INTO `kh_jxkhgz` VALUES (76, 'AX1-3-3-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-332', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'3\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1.6+1.6)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:39.713045');
INSERT INTO `kh_jxkhgz` VALUES (77, 'AX1-3-3-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-333', 'BKSJXZXS', 'KCJBM==\'3\' and JXMSJBM==\'3\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1.6+1.6)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:41.274002');
INSERT INTO `kh_jxkhgz` VALUES (78, 'AX1-9-2-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-921', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'2\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1+1.8)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:42.784461');
INSERT INTO `kh_jxkhgz` VALUES (79, 'AX1-9-3-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-931', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'3\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1+1.6)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:44.218797');
INSERT INTO `kh_jxkhgz` VALUES (80, 'AX1-9-1-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-912', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'1\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1+2)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:45.704493');
INSERT INTO `kh_jxkhgz` VALUES (81, 'AX1-9-1-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-913', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'1\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1+2)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:47.211955');
INSERT INTO `kh_jxkhgz` VALUES (82, 'AX1-9-2-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-922', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'2\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1+1.8)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:48.697287');
INSERT INTO `kh_jxkhgz` VALUES (83, 'AX1-9-2-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-923', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'2\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1+1.8)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:50.123114');
INSERT INTO `kh_jxkhgz` VALUES (84, 'AX1-9-9-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-991', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'9\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1+1)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:51.507394');
INSERT INTO `kh_jxkhgz` VALUES (85, 'AX1-9-9-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-992', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'9\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1+1)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:52.948849');
INSERT INTO `kh_jxkhgz` VALUES (86, 'AX1-9-9-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-993', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'9\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1+1)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:54.396797');
INSERT INTO `kh_jxkhgz` VALUES (87, 'AX1-9-3-2', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-932', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'3\' and WYKCTJM==\'2\'', 'JHXSS*ZLXS*(1+1.6)*3*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:55.834751');
INSERT INTO `kh_jxkhgz` VALUES (88, 'AX1-9-3-3', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-933', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'3\' and WYKCTJM==\'3\'', 'JHXSS*ZLXS*(1+1.6)*1*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:57.286009');
INSERT INTO `kh_jxkhgz` VALUES (89, 'AX1-9-1-1', '00000B', '教学工作量', '一般教学工作量', '本科生理论课', '本科生理论课学时数-911', 'BKSJXZXS', 'KCJBM==\'9\' and JXMSJBM==\'1\' and WYKCTJM==\'1\'', 'JHXSS*ZLXS*(1+2)*4*((HBS-1)*0.3+1)', '教师姓名：%(JSXM)s', '', NULL, '2021-05-14 07:15:58.595028');
INSERT INTO `kh_jxkhgz` VALUES (90, 'L-1-2', '00000B', '学术水平与成果工作量', '学术论文', '学术论文SCI1区', 'SCI-1区-外单位是第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==\'一区\' and WDWZZPX==\'1\' and BZXYBJZDSYS==\'无\' and GXL!=0', '20*0.5*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', '', NULL, '2021-05-14 07:15:59.916063');
INSERT INTO `kh_jxkhgz` VALUES (95, 'L-1-1', '00000B', '学术水平与成果工作量', '学术论文', '学术论文SCI1区', 'SCI-1区-外单位非第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==\'一区\' and WDWZZPX==\'2\' and BZXYBJZDSYS==\'无\' and GXL!=0', '20*0.7*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', '', NULL, '2021-05-14 07:16:01.474732');
INSERT INTO `kh_jxkhgz` VALUES (96, 'L-2-1', '00000B', '学术水平与成果工作量', '学术论文', '学术论文SCI2区', 'SCI-2区-外单位是第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==‘二区’ and WDWZZPX==‘1’ and BZXYBJZDSYS==’无‘ and GXL!=0', '15*0.5*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', '', NULL, '2021-05-14 07:16:02.905107');
INSERT INTO `kh_jxkhgz` VALUES (97, 'L-2-2', '00000B', '学术水平与成果工作量', '学术论文', '学术论文SCI2区', 'SCI-2区-外单位非第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==\'二区\'and WDWZZPX==\'2\' and  BZXYBJZDSYS==\'无\' and GXL!=0', '15*0.7*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', '', NULL, '2021-05-14 07:16:04.273574');
INSERT INTO `kh_jxkhgz` VALUES (98, 'L-3-1', '00000B', '学术水平和成果工作量', '学术论文', '学术论文SCI3区', 'SCI-3区-外单位是第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==\'三区\'and WDWZZPX==\'1\' and  BZXYBJZDSYS==\'无\' and GXL!=0', '10*0.5*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', '', NULL, '2021-05-14 07:16:05.749712');
INSERT INTO `kh_jxkhgz` VALUES (99, 'L-3-2', '00000B', '学术水平和成果工作量', '学术论文', '学术论文SCI3区', 'SCI-3区-外单位非第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==\'三区\'and WDWZZPX==\'2\' and  BZXYBJZDSYS==\'无\' and GXL!=0', '10*0.7*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', NULL, NULL, '2021-05-14 07:16:10.369434');
INSERT INTO `kh_jxkhgz` VALUES (100, 'L-4-1', '00000B', '学术水平和成果工作量', '学术论文', '学术论文SCI4区', 'SCI-4区-外单位是第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==\'四区\'and WDWZZPX==\'1\' and  BZXYBJZDSYS==\'无\' and GXL!=0', '8*0.5*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', NULL, NULL, '2021-05-14 07:16:08.906220');
INSERT INTO `kh_jxkhgz` VALUES (101, 'L-4-2', '00000B', '学术水平和成果工作量', '学术论文', '学术论文SCI4区', 'SCI-4区-外单位非第一作者', 'KJCGRYXX_LW', 'SLLX==\'1\' and SLQH==\'四区\'and WDWZZPX==\'2\' and  BZXYBJZDSYS==\'无\' and GXL!=0', '8*0.7*GXL', '教职工：%(DYZZ)s ,贡献率：%(GXL)s,论文名称：%(LWMC)s', NULL, NULL, '2021-05-14 07:16:13.616358');
COMMIT;

-- ----------------------------
-- Table structure for kh_khgzdz
-- ----------------------------
DROP TABLE IF EXISTS `kh_khgzdz`;
CREATE TABLE `kh_khgzdz` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DWH` varchar(16) DEFAULT NULL,
  `KHNF` datetime DEFAULT NULL,
  `GZH` varchar(128) DEFAULT NULL,
  `GZQY` enum('未启用','已启用') DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(2056) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_kh_khgzdz_dwh_khnf_gzh_uc` (`DWH`,`KHNF`,`GZH`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_khgzdz
-- ----------------------------
BEGIN;
INSERT INTO `kh_khgzdz` VALUES (27, '00000C', '2021-01-01 00:00:00', 'A1', '未启用', '2021-03-24 07:46:04.847960', '');
INSERT INTO `kh_khgzdz` VALUES (28, '00000C', '2021-01-01 00:00:00', 'A2', '已启用', '2021-03-17 06:19:33.000000', '');
INSERT INTO `kh_khgzdz` VALUES (29, '00000C', '2021-01-01 00:00:00', 'XX-001', '已启用', '2021-03-17 06:19:33.000000', '');
INSERT INTO `kh_khgzdz` VALUES (30, '00000C', '2021-01-01 00:00:00', 'ZJ-1', '已启用', '2021-03-17 06:19:33.000000', '');
INSERT INTO `kh_khgzdz` VALUES (31, '00000B', '2021-01-01 00:00:00', 'XX-001', '已启用', '2021-03-17 12:52:39.000000', '');
INSERT INTO `kh_khgzdz` VALUES (32, '00000B', '2021-01-01 00:00:00', 'XX-002', '已启用', '2021-03-17 12:52:39.000000', '');
INSERT INTO `kh_khgzdz` VALUES (33, '00000A', '2021-01-01 00:00:00', 'A1', '已启用', '2021-03-24 07:45:14.000000', '');
INSERT INTO `kh_khgzdz` VALUES (34, '00000A', '2021-01-01 00:00:00', 'A2', '已启用', '2021-03-24 07:45:14.000000', '');
INSERT INTO `kh_khgzdz` VALUES (36, '00000A', '2021-01-01 00:00:00', 'ZJ-1', '已启用', '2021-03-24 07:45:14.000000', '');
INSERT INTO `kh_khgzdz` VALUES (37, '00000A', '2021-01-01 00:00:00', 'XX-001', '已启用', '2021-03-24 07:45:14.000000', '');
INSERT INTO `kh_khgzdz` VALUES (38, '00000A', '2021-01-01 00:00:00', 'XX-002', '已启用', '2021-03-24 07:45:14.000000', '');
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
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=239 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_khjgmx
-- ----------------------------
BEGIN;
INSERT INTO `kh_khjgmx` VALUES (143, '00001B', '00000C', 'ZJ-1', '2021-01-01 00:00:00', 20, 'da', '', '2021-03-06 15:38:57.000000');
INSERT INTO `kh_khjgmx` VALUES (233, '00001B', '00000C', 'A1', '2021-01-01 00:00:00', 1.5, 'A1->教职工：00001B BH8877元', '', '2021-05-14 06:08:05.000000');
INSERT INTO `kh_khjgmx` VALUES (234, '00001B', '00000C', 'A1', '2021-01-01 00:00:00', 1.5, 'A1->教职工：00001B BH8888元', '', '2021-05-14 06:08:05.000000');
INSERT INTO `kh_khjgmx` VALUES (235, '00001B', '00000C', 'A2', '2021-01-01 00:00:00', 36000, '教职工：00001B BH8877元', '', '2021-05-14 06:08:05.000000');
INSERT INTO `kh_khjgmx` VALUES (236, '00001B', '00000C', 'A2', '2021-01-01 00:00:00', 36002, '教职工：00001B BH8888元', '', '2021-05-14 06:08:05.000000');
INSERT INTO `kh_khjgmx` VALUES (237, '00001B', '00000B', 'XX-002', '2021-01-01 00:00:00', 10, 'XX-002->教职工：00001B BH8877元', '', '2021-05-14 06:08:05.000000');
INSERT INTO `kh_khjgmx` VALUES (238, '00001B', '00000B', 'XX-002', '2021-01-01 00:00:00', 10, 'XX-002->教职工：00001B BH8888元', '', '2021-05-14 06:08:05.000000');
COMMIT;

-- ----------------------------
-- Table structure for kh_khpc
-- ----------------------------
DROP TABLE IF EXISTS `kh_khpc`;
CREATE TABLE `kh_khpc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DWH` varchar(16) DEFAULT NULL,
  `KHNF` datetime DEFAULT NULL,
  `RQQD` datetime DEFAULT NULL,
  `RQZD` datetime DEFAULT NULL,
  `JHZT` enum('未激活','已激活') DEFAULT NULL,
  `FBZT` enum('未发布','已发布') DEFAULT NULL,
  `stamp` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `note` varchar(2056) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `_kh_khpc_dwh_khnf_uc` (`DWH`,`KHNF`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kh_khpc
-- ----------------------------
BEGIN;
INSERT INTO `kh_khpc` VALUES (5, '00000C', '2021-01-01 00:00:00', '2020-01-01 00:00:00', '2020-12-31 00:00:00', '已激活', '已发布', '2021-03-30 07:15:58.186218', NULL);
INSERT INTO `kh_khpc` VALUES (6, '00000B', '2021-01-01 00:00:00', '2020-01-01 00:00:00', '2021-12-31 00:00:00', '已激活', '已发布', '2021-03-17 03:28:14.039283', NULL);
COMMIT;

-- ----------------------------
-- Table structure for st_jldj
-- ----------------------------
DROP TABLE IF EXISTS `st_jldj`;
CREATE TABLE `st_jldj` (
  `DM` varchar(3) NOT NULL,
  `MC` varchar(10) NOT NULL,
  PRIMARY KEY (`DM`) USING BTREE,
  UNIQUE KEY `st_jldj_DM_uindex` (`DM`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of st_jldj
-- ----------------------------
BEGIN;
INSERT INTO `st_jldj` VALUES ('1', '特等');
INSERT INTO `st_jldj` VALUES ('2', '一等');
INSERT INTO `st_jldj` VALUES ('3', '二等');
INSERT INTO `st_jldj` VALUES ('4', '三等');
INSERT INTO `st_jldj` VALUES ('5', '四等');
INSERT INTO `st_jldj` VALUES ('6', '未评等级');
INSERT INTO `st_jldj` VALUES ('9', '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_jxmsjbm
-- ----------------------------
DROP TABLE IF EXISTS `st_jxmsjbm`;
CREATE TABLE `st_jxmsjbm` (
  `DM` varchar(32) NOT NULL,
  `MC` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_jxmsjbm_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='教学名师级别码';

-- ----------------------------
-- Records of st_jxmsjbm
-- ----------------------------
BEGIN;
INSERT INTO `st_jxmsjbm` VALUES ('1', '国家级教学名师');
INSERT INTO `st_jxmsjbm` VALUES ('2', '省级教学名师');
INSERT INTO `st_jxmsjbm` VALUES ('3', '校级教学名师');
INSERT INTO `st_jxmsjbm` VALUES ('9', '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_kcjbm
-- ----------------------------
DROP TABLE IF EXISTS `st_kcjbm`;
CREATE TABLE `st_kcjbm` (
  `DM` varchar(10) NOT NULL,
  `MC` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_kcjbm_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='课程级别码';

-- ----------------------------
-- Records of st_kcjbm
-- ----------------------------
BEGIN;
INSERT INTO `st_kcjbm` VALUES ('1', '国家级精品课');
INSERT INTO `st_kcjbm` VALUES ('2', '省级精品课');
INSERT INTO `st_kcjbm` VALUES ('3', '校级精品课');
INSERT INTO `st_kcjbm` VALUES ('4', '校级重点课程');
INSERT INTO `st_kcjbm` VALUES ('9', '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_cbs
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_cbs`;
CREATE TABLE `st_ky_cbs` (
  `MC` varchar(10) DEFAULT NULL,
  `DM` varchar(3) NOT NULL,
  PRIMARY KEY (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_cbs
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_cbs` VALUES ('国外著名出版社', '1');
INSERT INTO `st_ky_cbs` VALUES ('其他', '10');
INSERT INTO `st_ky_cbs` VALUES ('科学出版社', '2');
INSERT INTO `st_ky_cbs` VALUES ('高等教育出版社', '3');
INSERT INTO `st_ky_cbs` VALUES ('机械工业出版社', '4');
INSERT INTO `st_ky_cbs` VALUES ('电子工业出版社', '5');
INSERT INTO `st_ky_cbs` VALUES ('人民教育出版社', '6');
INSERT INTO `st_ky_cbs` VALUES ('国防工业出版社', '7');
INSERT INTO `st_ky_cbs` VALUES ('清华大学出版社', '8');
INSERT INTO `st_ky_cbs` VALUES ('人民邮电出版社', '9');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_cbsjb
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_cbsjb`;
CREATE TABLE `st_ky_cbsjb` (
  `MC` varchar(16) DEFAULT NULL,
  `DM` varchar(16) NOT NULL,
  PRIMARY KEY (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_cbsjb
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_cbsjb` VALUES ('A类', '1');
INSERT INTO `st_ky_cbsjb` VALUES ('B类', '2');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_cghjlb
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_cghjlb`;
CREATE TABLE `st_ky_cghjlb` (
  `DM` varchar(3) NOT NULL,
  `MC` varchar(10) NOT NULL,
  PRIMARY KEY (`DM`) USING BTREE,
  UNIQUE KEY `st_ky_cghjlb_DM_uindex` (`DM`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of st_ky_cghjlb
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_cghjlb` VALUES ('01', '科学技术');
INSERT INTO `st_ky_cghjlb` VALUES ('02', '发明');
INSERT INTO `st_ky_cghjlb` VALUES ('03', '自然科学');
INSERT INTO `st_ky_cghjlb` VALUES ('04', '哲学社会科学');
INSERT INTO `st_ky_cghjlb` VALUES ('05', '科技进步');
INSERT INTO `st_ky_cghjlb` VALUES ('06', '优秀教材');
INSERT INTO `st_ky_cghjlb` VALUES ('07', '合理化和技术改造');
INSERT INTO `st_ky_cghjlb` VALUES ('08', '技术展览');
INSERT INTO `st_ky_cghjlb` VALUES ('09', '星火计划');
INSERT INTO `st_ky_cghjlb` VALUES ('10', '教学成果');
INSERT INTO `st_ky_cghjlb` VALUES ('11', '教学软件');
INSERT INTO `st_ky_cghjlb` VALUES ('12', '实验技术成果');
INSERT INTO `st_ky_cghjlb` VALUES ('99', '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_hyjbxs
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_hyjbxs`;
CREATE TABLE `st_ky_hyjbxs` (
  `DM` int(11) NOT NULL,
  `MC` varchar(11) NOT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_ky_hyjbxsm_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_hyjbxs
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_hyjbxs` VALUES (1, '本校独立举办');
INSERT INTO `st_ky_hyjbxs` VALUES (2, '与外单位合办');
INSERT INTO `st_ky_hyjbxs` VALUES (3, '主办');
INSERT INTO `st_ky_hyjbxs` VALUES (4, '协办');
INSERT INTO `st_ky_hyjbxs` VALUES (5, '承办');
INSERT INTO `st_ky_hyjbxs` VALUES (9, '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_js
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_js`;
CREATE TABLE `st_ky_js` (
  `MC` varchar(10) DEFAULT NULL,
  `DM` varchar(3) NOT NULL,
  PRIMARY KEY (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_js
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_js` VALUES ('独著人', '200');
INSERT INTO `st_ky_js` VALUES ('第一主编', '211');
INSERT INTO `st_ky_js` VALUES ('普通主编', '219');
INSERT INTO `st_ky_js` VALUES ('作者', '230');
INSERT INTO `st_ky_js` VALUES ('第一作者', '231');
INSERT INTO `st_ky_js` VALUES ('第二作者', '232');
INSERT INTO `st_ky_js` VALUES ('第三作者', '233');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_lzlb
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_lzlb`;
CREATE TABLE `st_ky_lzlb` (
  `DM` varchar(3) NOT NULL,
  `MC` varchar(10) NOT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_ky_lzlb_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_lzlb
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_lzlb` VALUES ('10', '著作');
INSERT INTO `st_ky_lzlb` VALUES ('11', '专著');
INSERT INTO `st_ky_lzlb` VALUES ('12', '编著');
INSERT INTO `st_ky_lzlb` VALUES ('13', '译著');
INSERT INTO `st_ky_lzlb` VALUES ('14', '教材');
INSERT INTO `st_ky_lzlb` VALUES ('21', '手册');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_lzsl
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_lzsl`;
CREATE TABLE `st_ky_lzsl` (
  `DM` varchar(3) NOT NULL,
  `MC` varchar(16) NOT NULL,
  PRIMARY KEY (`DM`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of st_ky_lzsl
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_lzsl` VALUES ('1', 'SCI');
INSERT INTO `st_ky_lzsl` VALUES ('10', 'B 类');
INSERT INTO `st_ky_lzsl` VALUES ('11', '校内权威期刊');
INSERT INTO `st_ky_lzsl` VALUES ('2', 'EI');
INSERT INTO `st_ky_lzsl` VALUES ('3', 'STP');
INSERT INTO `st_ky_lzsl` VALUES ('4', 'ISTP');
INSERT INTO `st_ky_lzsl` VALUES ('5', 'CSSCI');
INSERT INTO `st_ky_lzsl` VALUES ('6', 'AHCI');
INSERT INTO `st_ky_lzsl` VALUES ('7', 'SSCI');
INSERT INTO `st_ky_lzsl` VALUES ('8', '其他');
INSERT INTO `st_ky_lzsl` VALUES ('9', 'A 类');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_xkmlkj
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_xkmlkj`;
CREATE TABLE `st_ky_xkmlkj` (
  `DM` varchar(4) NOT NULL,
  `MC` varchar(15) NOT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_ky_xkmlkj_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_xkmlkj
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_xkmlkj` VALUES ('1', '自然科学');
INSERT INTO `st_ky_xkmlkj` VALUES ('2', '农业科学');
INSERT INTO `st_ky_xkmlkj` VALUES ('3', '医药科学');
INSERT INTO `st_ky_xkmlkj` VALUES ('4', '工程与技术');
INSERT INTO `st_ky_xkmlkj` VALUES ('5', '人文与社会科学');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_xmjfly
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_xmjfly`;
CREATE TABLE `st_ky_xmjfly` (
  `DM` varchar(4) NOT NULL,
  `MC` varchar(20) NOT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_ky_xmjfly_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_xmjfly
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_xmjfly` VALUES ('1', '主管部门专项费');
INSERT INTO `st_ky_xmjfly` VALUES ('10', '企、事业单位委托项目经费');
INSERT INTO `st_ky_xmjfly` VALUES ('11', '各种收入中转为当年研究与发展经费');
INSERT INTO `st_ky_xmjfly` VALUES ('12', '自筹经费');
INSERT INTO `st_ky_xmjfly` VALUES ('13', '贷款');
INSERT INTO `st_ky_xmjfly` VALUES ('14', '国外资金');
INSERT INTO `st_ky_xmjfly` VALUES ('15', '港、澳、台地区资金');
INSERT INTO `st_ky_xmjfly` VALUES ('2', '国家发改委、科技部专项费');
INSERT INTO `st_ky_xmjfly` VALUES ('4', '国家社科规划、基金项目经费');
INSERT INTO `st_ky_xmjfly` VALUES ('5', '国家自然科学基金');
INSERT INTO `st_ky_xmjfly` VALUES ('6', '中央、国家其他部门专项费');
INSERT INTO `st_ky_xmjfly` VALUES ('7', '省、市、自治区专项费');
INSERT INTO `st_ky_xmjfly` VALUES ('8', '地(市、州)专项费');
INSERT INTO `st_ky_xmjfly` VALUES ('9', '县(区、旗)专项费');
INSERT INTO `st_ky_xmjfly` VALUES ('99', '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_ky_xshydj
-- ----------------------------
DROP TABLE IF EXISTS `st_ky_xshydj`;
CREATE TABLE `st_ky_xshydj` (
  `DM` int(11) NOT NULL,
  `MC` varchar(20) NOT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_ky_xshydj_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_ky_xshydj
-- ----------------------------
BEGIN;
INSERT INTO `st_ky_xshydj` VALUES (1, '世界性、区域性、国际间学术会议');
INSERT INTO `st_ky_xshydj` VALUES (2, '两国间双边学术会议');
INSERT INTO `st_ky_xshydj` VALUES (3, '全国、地区性学术会议');
INSERT INTO `st_ky_xshydj` VALUES (4, '省内学术会议');
INSERT INTO `st_ky_xshydj` VALUES (5, '港、澳、台学术会议');
INSERT INTO `st_ky_xshydj` VALUES (6, '校内学术会议');
INSERT INTO `st_ky_xshydj` VALUES (9, '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_wykctjm
-- ----------------------------
DROP TABLE IF EXISTS `st_wykctjm`;
CREATE TABLE `st_wykctjm` (
  `DM` varchar(32) NOT NULL,
  `MC` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_wykctjm_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='外语课程调节码';

-- ----------------------------
-- Records of st_wykctjm
-- ----------------------------
BEGIN;
INSERT INTO `st_wykctjm` VALUES ('1', '外语');
INSERT INTO `st_wykctjm` VALUES ('2', '双语');
INSERT INTO `st_wykctjm` VALUES ('3', '普通');
COMMIT;

-- ----------------------------
-- Table structure for st_xs_pyfs
-- ----------------------------
DROP TABLE IF EXISTS `st_xs_pyfs`;
CREATE TABLE `st_xs_pyfs` (
  `MC` varchar(16) NOT NULL,
  `DM` varchar(16) NOT NULL,
  PRIMARY KEY (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_xs_pyfs
-- ----------------------------
BEGIN;
INSERT INTO `st_xs_pyfs` VALUES ('非定向', '11');
INSERT INTO `st_xs_pyfs` VALUES ('定向', '12');
INSERT INTO `st_xs_pyfs` VALUES ('留学生', '30');
COMMIT;

-- ----------------------------
-- Table structure for st_xs_xsdqzt
-- ----------------------------
DROP TABLE IF EXISTS `st_xs_xsdqzt`;
CREATE TABLE `st_xs_xsdqzt` (
  `DM` varchar(16) NOT NULL,
  `MC` varchar(16) NOT NULL,
  PRIMARY KEY (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_xs_xsdqzt
-- ----------------------------
BEGIN;
INSERT INTO `st_xs_xsdqzt` VALUES ('1', '在读');
INSERT INTO `st_xs_xsdqzt` VALUES ('2', '休学');
INSERT INTO `st_xs_xsdqzt` VALUES ('3', '退学');
INSERT INTO `st_xs_xsdqzt` VALUES ('7', '毕业');
COMMIT;

-- ----------------------------
-- Table structure for st_xs_xslb
-- ----------------------------
DROP TABLE IF EXISTS `st_xs_xslb`;
CREATE TABLE `st_xs_xslb` (
  `MC` varchar(16) NOT NULL,
  `DM` varchar(16) NOT NULL,
  PRIMARY KEY (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_xs_xslb
-- ----------------------------
BEGIN;
INSERT INTO `st_xs_xslb` VALUES ('全日制硕士研究生', '4313');
INSERT INTO `st_xs_xslb` VALUES ('非全日制研究生', '4314');
INSERT INTO `st_xs_xslb` VALUES ('博士研究生', '432');
COMMIT;

-- ----------------------------
-- Table structure for st_xx_jb
-- ----------------------------
DROP TABLE IF EXISTS `st_xx_jb`;
CREATE TABLE `st_xx_jb` (
  `DM` varchar(3) NOT NULL,
  `MC` varchar(20) NOT NULL,
  PRIMARY KEY (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Records of st_xx_jb
-- ----------------------------
BEGIN;
INSERT INTO `st_xx_jb` VALUES ('10', '国家级');
INSERT INTO `st_xx_jb` VALUES ('20', '省、部委级');
INSERT INTO `st_xx_jb` VALUES ('21', '教育部');
INSERT INTO `st_xx_jb` VALUES ('22', '中央其他部委');
INSERT INTO `st_xx_jb` VALUES ('23', '省（自治区、直辖市）级');
INSERT INTO `st_xx_jb` VALUES ('30', '省部门级、地（市、州）级');
INSERT INTO `st_xx_jb` VALUES ('31', '省级教育行政部门');
INSERT INTO `st_xx_jb` VALUES ('32', '省级其他部门');
INSERT INTO `st_xx_jb` VALUES ('33', '地（市、州）级');
INSERT INTO `st_xx_jb` VALUES ('40', '地（市、州）部门级、县（区、旗）级');
INSERT INTO `st_xx_jb` VALUES ('41', '地级教育行政部门');
INSERT INTO `st_xx_jb` VALUES ('42', '地级其他部门');
INSERT INTO `st_xx_jb` VALUES ('43', '县级');
INSERT INTO `st_xx_jb` VALUES ('50', '县部门级、乡（镇）级');
INSERT INTO `st_xx_jb` VALUES ('51', '县级教育行政部门');
INSERT INTO `st_xx_jb` VALUES ('52', '县级其他部门');
INSERT INTO `st_xx_jb` VALUES ('53', '乡（镇）级');
INSERT INTO `st_xx_jb` VALUES ('60', '学校级');
INSERT INTO `st_xx_jb` VALUES ('70', '国际');
INSERT INTO `st_xx_jb` VALUES ('99', '其他');
COMMIT;

-- ----------------------------
-- Table structure for st_xx_sfbz
-- ----------------------------
DROP TABLE IF EXISTS `st_xx_sfbz`;
CREATE TABLE `st_xx_sfbz` (
  `DM` varchar(4) NOT NULL,
  `MC` varchar(4) NOT NULL,
  PRIMARY KEY (`DM`),
  UNIQUE KEY `st_xx_sfbz_DM_uindex` (`DM`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of st_xx_sfbz
-- ----------------------------
BEGIN;
INSERT INTO `st_xx_sfbz` VALUES ('0', '否');
INSERT INTO `st_xx_sfbz` VALUES ('1', '是');
COMMIT;

-- ----------------------------
-- View structure for view_bcykh
-- ----------------------------
DROP VIEW IF EXISTS `view_bcykh`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_bcykh` AS select `kh`.`id` AS `id`,`kh`.`DWH` AS `DWH`,`dr`.`DWMC` AS `DWMC`,`kh`.`KHNF` AS `KHNF`,`kh`.`JZGH` AS `JZGH`,`zg`.`XM` AS `XM`,`kh`.`CYZT` AS `CYZT`,`kh`.`stamp` AS `stamp`,`kh`.`note` AS `note` from (((`kh_bcykh` `kh` left join `dr_zzjgjbsjxx` `dr` on((`dr`.`DWH` = `kh`.`DWH`))) left join `dr_jzgjcsjxx` `zg` on((`zg`.`JZGH` = `kh`.`JZGH`))) left join `kh_khpc` `pc` on(((`pc`.`DWH` = `kh`.`DWH`) and (`pc`.`KHNF` = `kh`.`KHNF`)))) where (1 = 1);

-- ----------------------------
-- View structure for view_bjsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_bjsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_bjsjxx` AS select `dr`.`id` AS `id`,`dr`.`BH` AS `BH`,`dr`.`BJ` AS `BJ`,`dr`.`JBNY` AS `JBNY`,`dr`.`RXNF` AS `RXNF`,`dr`.`FDYH` AS `FDYH`,`fdy`.`XM` AS `FDYXM`,`dr`.`BDS` AS `BDS`,`bds`.`XM` AS `BDSXM`,`dr`.`SSXY` AS `DWH`,`dr`.`SSXY` AS `SSXY`,`zzjg`.`DWMC` AS `SSXYMC`,`dr`.`SSZY` AS `SSZY`,`dr`.`XSLB` AS `XSLB`,`dr`.`QYBZ` AS `QYBZ`,`dr`.`stamp` AS `stamp`,`dr`.`note` AS `note` from (((`dr_bjsjxx` `dr` left join `dr_jzgjcsjxx` `bds` on((`bds`.`JZGH` = `dr`.`BDS`))) left join `dr_jzgjcsjxx` `fdy` on((`fdy`.`JZGH` = `dr`.`FDYH`))) left join `dr_zzjgjbsjxx` `zzjg` on((`zzjg`.`DWH` = `dr`.`SSXY`))) where (1 = 1);

-- ----------------------------
-- View structure for view_bksjxzxs
-- ----------------------------
DROP VIEW IF EXISTS `view_bksjxzxs`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_bksjxzxs` AS select `pk`.`id` AS `id`,`pk`.`JSGH` AS `JSGH`,`pk`.`JSGH` AS `JZGH`,`pk`.`JSXM` AS `JSXM`,`pk`.`KKXND` AS `KKXND`,`pk`.`KKXQM` AS `KKXQM`,`kc`.`LLXS` AS `JHXSS`,`pk`.`ZKJHXS` AS `ZKJHXS`,`pk`.`ZLXS` AS `ZLXS`,`pk`.`HBS` AS `HBS`,`pk`.`SKBJH` AS `SKBJH`,`pk`.`WYKCTJM` AS `WYKCTJM`,`pk`.`JXMSJBM` AS `JXMSJBM`,`pk`.`KCJBM` AS `KCJBM`,`kc`.`KCH` AS `KCH`,`pk`.`DWH` AS `DWH`,`pk`.`DWMC` AS `DWMC`,`xn`.`XQQSSJ` AS `stamp`,`pk`.`note` AS `note` from (((`dr_pksjxx` `pk` left join `dr_kcsjxx` `kc` on((`kc`.`KCH` = `pk`.`KCH`))) left join `dr_xnxqxx` `xn` on((`xn`.`XQQSSJ` = `pk`.`KKXQM`))) left join `dr_zzjgjbsjxx` `zz` on((`zz`.`DWH` = `pk`.`DWH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_bkszkjxzxs
-- ----------------------------
DROP VIEW IF EXISTS `view_bkszkjxzxs`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_bkszkjxzxs` AS select `pk`.`id` AS `id`,`pk`.`JSGH` AS `JSGH`,`pk`.`JSGH` AS `JZGH`,`pk`.`JSXM` AS `JSXM`,`pk`.`KKXND` AS `KKXND`,`pk`.`KKXQM` AS `KKXQM`,`kc`.`LLXS` AS `JHXSS`,`pk`.`ZKJHXS` AS `ZKJHXS`,`pk`.`ZLXS` AS `ZLXS`,`pk`.`HBS` AS `HBS`,`pk`.`SKBJH` AS `SKBJH`,`pk`.`WYKCTJM` AS `WYKCTJM`,`pk`.`JXMSJBM` AS `JXMSJBM`,`pk`.`KCJBM` AS `KCJBM`,`kc`.`KCH` AS `KCH`,`pk`.`DWH` AS `DWH`,`pk`.`DWMC` AS `DWMC`,`xn`.`XQQSSJ` AS `stamp`,`pk`.`note` AS `note` from (((`dr_pkzksjxx` `pk` left join `dr_kcsjxx` `kc` on((`kc`.`KCH` = `pk`.`KCH`))) left join `dr_xnxqxx` `xn` on((`xn`.`XQQSSJ` = `pk`.`KKXQM`))) left join `dr_zzjgjbsjxx` `zz` on((`zz`.`DWH` = `pk`.`DWH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_bks_jpkc
-- ----------------------------
DROP VIEW IF EXISTS `view_bks_jpkc`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_bks_jpkc` AS select `jp`.`id` AS `id`,`jp`.`KCH` AS `KCH`,`jp`.`KCMC` AS `KCMC`,`jp`.`KCJBM` AS `KCJBM`,`jp`.`FZRGH` AS `FZRGH`,`jp`.`FZRXM` AS `FZRXM`,`jp`.`DWH` AS `DWH`,`jp`.`stamp` AS `stamp`,`jp`.`note` AS `note` from (((`dr_bks_jpkc` `jp` left join `dr_kcsjxx` `kc` on((`kc`.`KCH` = `jp`.`KCH`))) left join `dr_zzjgjbsjxx` `zzjg` on((`zzjg`.`DWH` = `jp`.`DWH`))) left join `dr_jzgjcsjxx` `dr_jzg` on((`dr_jzg`.`JZGH` = `jp`.`FZRGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_hjcgjbsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_hjcgjbsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_hjcgjbsjxx` AS select `dr_hjcg`.`id` AS `id`,`dr_hjcg`.`HJCGBH` AS `HJCGBH`,`dr_hjcg`.`HJCGMC` AS `HJCGMC`,`dr_hjcg`.`XMLYM` AS `XMLYM`,`dr_hjcg`.`DWH` AS `DWH`,`dr_hjcg`.`HJRQ` AS `HJRQ`,`dr_hjcg`.`CGHJLBM` AS `CGHJLBM`,`dr_hjcg`.`KJJLB` AS `KJJLB`,`dr_hjcg`.`JLDJM` AS `JLDJM`,`dr_hjcg`.`HJJBM` AS `HJJBM`,`dr_hjcg`.`XKLYM` AS `XKLYM`,`dr_hjcg`.`BJDW` AS `BJDW`,`dr_hjcg`.`SSXMBH` AS `SSXMBH`,`dr_hjcg`.`DWPM` AS `DWPM`,`dr_hjcg`.`XKMLKJM` AS `XKMLKJM`,`dr_hjcg`.`FZRYH` AS `FZRYH`,`dr_hjcg`.`FZRYH` AS `JZGH`,`dr_hjcg`.`FZRXM` AS `FZRXM`,`dr_hjcg`.`YJXK` AS `YJXK`,`dr_hjcg`.`DWMC` AS `DWMC`,`dr_hjcg`.`YJSMC` AS `YJSMC`,`dr_hjcg`.`CGXS` AS `CGXS`,`dr_hjcg`.`HJMC` AS `HJMC`,`dr_hjcg`.`HJBH` AS `HJBH`,`dr_hjcg`.`HJRQ` AS `stamp`,`dr_hjcg`.`note` AS `note` from (`dr_hjcgjbsjxx` `dr_hjcg` left join `dc_hjcgjbsjxx` `dc_hjcg` on((`dr_hjcg`.`HJCGBH` = `dr_hjcg`.`HJCGBH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_jkxss
-- ----------------------------
DROP VIEW IF EXISTS `view_jkxss`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_jkxss` AS select `dr`.`id` AS `id`,`dr`.`KSRQ` AS `KSRQ`,`dr`.`KSSC` AS `KSSC`,`dr`.`KSFSLXM` AS `KSFSLXM`,`dr`.`KCH` AS `KCH`,`dr`.`JKRGH` AS `JZGH`,`dr`.`JKRGH` AS `JKRGH`,`dr`.`KSJSH` AS `KSJSH`,`dr`.`JKRXM` AS `JKRXM`,`dr`.`KSRS` AS `KSRS`,`dr`.`SSXY` AS `SSXY`,`jkr`.`DWH` AS `JSSSXY`,`jkr`.`DWH` AS `DWH`,`dr`.`KSRQ` AS `stamp`,`dr`.`note` AS `note` from ((`dr_ksapxx` `dr` left join `dr_jzgjcsjxx` `jkr` on((`jkr`.`JZGH` = `dr`.`JKRGH`))) left join `dr_pksjxx` `pk` on((`pk`.`KCH` = `dr`.`KCH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_jxkhgz
-- ----------------------------
DROP VIEW IF EXISTS `view_jxkhgz`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_jxkhgz` AS select `kh`.`id` AS `id`,`kh`.`GZH` AS `GZH`,`kh`.`DWH` AS `DWH`,`dw`.`DWMC` AS `DWMC`,`kh`.`KHLX` AS `KHLX`,`kh`.`KHZL` AS `KHZL`,`kh`.`XXKHZL` AS `XXKHZL`,`kh`.`KHMC` AS `KHMC`,`kh`.`KHSJDX` AS `KHSJDX`,`kh`.`GZTJ` AS `GZTJ`,`kh`.`JXFSJS` AS `JXFSJS`,`kh`.`KHMXMB` AS `KHMXMB`,`kh`.`KHJGDX` AS `KHJGDX`,`kh`.`stamp` AS `stamp`,`kh`.`note` AS `note` from (`kh_jxkhgz` `kh` left join `dr_zzjgjbsjxx` `dw` on((`dw`.`DWH` = `kh`.`DWH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_jzgjcsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_jzgjcsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_jzgjcsjxx` AS select `dr`.`id` AS `id`,`dr`.`JZGH` AS `JZGH`,`dr`.`DWH` AS `DWH`,`zzjg`.`DWMC` AS `DWMC`,`dr`.`XM` AS `XM`,`dr`.`YWXM` AS `YWXM`,`dr`.`XMPY` AS `XMPY`,`dr`.`CYM` AS `CYM`,`dr`.`XBM` AS `XBM`,`dr`.`CSRQ` AS `CSRQ`,`dr`.`CSDM` AS `CSDM`,`dr`.`BZLBM` AS `BZLBM`,`dr`.`JZGLBM` AS `JZGLBM`,`dr`.`DQZTM` AS `DQZTM`,`dr`.`stamp` AS `stamp`,`dr`.`note` AS `note` from ((`dr_jzgjcsjxx` `dr` left join `dc_jzgjcsjxx` `dc` on((`dc`.`JZGH` = `dr`.`JZGH`))) left join `dr_zzjgjbsjxx` `zzjg` on((`zzjg`.`DWH` = `dr`.`DWH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_kcsjxss
-- ----------------------------
DROP VIEW IF EXISTS `view_kcsjxss`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_kcsjxss` AS select `pk`.`id` AS `id`,`pk`.`JSGH` AS `JSGH`,`pk`.`JSGH` AS `JZGH`,`pk`.`JSXM` AS `JSXM`,`pk`.`KKXND` AS `KKXND`,`pk`.`KKXQM` AS `KKXQM`,`pk`.`HBS` AS `HBS`,`pk`.`ZLXS` AS `ZLXS`,`kc`.`KCH` AS `KCH`,`dr_jzg`.`DWH` AS `DWH`,`pk`.`SXZS` AS `SXZS`,`xn`.`XQQSSJ` AS `stamp`,`pk`.`note` AS `note` from (((`dr_kcsjsjxx` `pk` left join `dr_kcsjxx` `kc` on((`kc`.`KCH` = `pk`.`KCH`))) left join `dr_xnxqxx` `xn` on((`xn`.`XQQSSJ` = `pk`.`KKXQM`))) left join `dr_jzgjcsjxx` `dr_jzg` on((`dr_jzg`.`JZGH` = `pk`.`JSGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_kcsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_kcsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_kcsjxx` AS select `kc`.`id` AS `id`,`kc`.`JZGH` AS `JZGH`,`kc`.`KCH` AS `KCH`,`kc`.`KCMC` AS `KCMC`,`kc`.`ZXS` AS `ZXS`,`kc`.`LLXS` AS `LLXS`,`kc`.`SYXS` AS `SYXS`,`kc`.`SJXS` AS `SJXS`,`dr_jzg`.`DWH` AS `DWH`,`kc`.`stamp` AS `stamp`,`kc`.`note` AS `note` from (`dr_kcsjxx` `kc` left join `dr_jzgjcsjxx` `dr_jzg` on((`dr_jzg`.`JZGH` = `kc`.`JZGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_khgzdz
-- ----------------------------
DROP VIEW IF EXISTS `view_khgzdz`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_khgzdz` AS select `kh`.`id` AS `id`,`kh`.`DWH` AS `DWH`,`dr`.`DWMC` AS `DWMC`,`kh`.`KHNF` AS `KHNF`,`kh`.`GZH` AS `GZH`,`kh`.`GZQY` AS `GZQY`,`gz`.`KHMC` AS `KHMC`,`kh`.`stamp` AS `stamp`,`kh`.`note` AS `note` from ((`kh_khgzdz` `kh` left join `dr_zzjgjbsjxx` `dr` on((`dr`.`DWH` = `kh`.`DWH`))) left join `kh_jxkhgz` `gz` on((`gz`.`GZH` = `kh`.`GZH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_khjghz
-- ----------------------------
DROP VIEW IF EXISTS `view_khjghz`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_khjghz` AS select `kh`.`id` AS `id`,`kh`.`JZGH` AS `JZGH`,`zg`.`XM` AS `XM`,`kh`.`DWH` AS `DWH`,`dr`.`DWMC` AS `DWMC`,`kh`.`LSDWH` AS `LSDWH`,`ls`.`DWMC` AS `LSDWMC`,`kh`.`KHNF` AS `KHNF`,`kh`.`GZH` AS `GZH`,`gz`.`KHMC` AS `KHMC`,`gz`.`KHLX` AS `KHLX`,`gz`.`KHZL` AS `KHZL`,`gz`.`XXKHZL` AS `XXKHZL`,`kh`.`KHJDHJ` AS `KHJDHJ`,`kh`.`stamp` AS `stamp`,`kh`.`note` AS `note` from ((((`kh_khjghz` `kh` left join `dr_zzjgjbsjxx` `dr` on((`dr`.`DWH` = `kh`.`DWH`))) left join `dr_zzjgjbsjxx` `ls` on((`ls`.`DWH` = `kh`.`LSDWH`))) left join `dr_jzgjcsjxx` `zg` on((`zg`.`JZGH` = `kh`.`JZGH`))) left join `kh_jxkhgz` `gz` on((`gz`.`GZH` = `kh`.`GZH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_khjgmx
-- ----------------------------
DROP VIEW IF EXISTS `view_khjgmx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_khjgmx` AS select `kh`.`id` AS `id`,`kh`.`KHNF` AS `KHNF`,`kh`.`JZGH` AS `JZGH`,`zg`.`XM` AS `XM`,`kh`.`DWH` AS `DWH`,`dr`.`DWMC` AS `DWMC`,`kh`.`GZH` AS `GZH`,`gz`.`KHMC` AS `KHMC`,`kh`.`KHJD` AS `KHJD`,`kh`.`KHMX` AS `KHMX`,`kh`.`stamp` AS `stamp`,`kh`.`note` AS `note` from (((`kh_khjgmx` `kh` left join `dr_zzjgjbsjxx` `dr` on((`dr`.`DWH` = `kh`.`DWH`))) left join `dr_jzgjcsjxx` `zg` on((`zg`.`JZGH` = `kh`.`JZGH`))) left join `kh_jxkhgz` `gz` on((`gz`.`GZH` = `kh`.`GZH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_khpc
-- ----------------------------
DROP VIEW IF EXISTS `view_khpc`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_khpc` AS select `kh`.`id` AS `id`,`kh`.`DWH` AS `DWH`,`dr`.`DWMC` AS `DWMC`,`kh`.`KHNF` AS `KHNF`,`kh`.`RQQD` AS `RQQD`,`kh`.`RQZD` AS `RQZD`,`kh`.`JHZT` AS `JHZT`,`kh`.`FBZT` AS `FBZT`,`kh`.`stamp` AS `stamp`,`kh`.`note` AS `note` from (`kh_khpc` `kh` left join `dr_zzjgjbsjxx` `dr` on((`dr`.`DWH` = `kh`.`DWH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_kjcgryxx_jl
-- ----------------------------
DROP VIEW IF EXISTS `view_kjcgryxx_jl`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_kjcgryxx_jl` AS select `dr_kjcg_jl`.`id` AS `id`,`dr_kjcg_jl`.`RYH` AS `RYH`,`dr_kjcg_jl`.`XM` AS `XM`,`dr_kjcg_jl`.`JSM` AS `JSM`,`dr_kjcg_jl`.`ZXZS` AS `ZXZS`,`dr_kjcg_jl`.`PMZRS` AS `PMZRS`,`dr_kjcg_jl`.`GXL` AS `GXL`,`dr_kjcg_jl`.`SZDW` AS `SZDW`,`dr_kjcg_jl`.`RYLX` AS `RYLX`,`dr_kjcg_jl`.`HJCGBH` AS `HJCGBH`,`dr_kjcg_jl`.`KJCGRYBH` AS `KJCGRYBH`,`dr_kjcg_jl`.`RYH` AS `JZGH`,`dr_hjcg`.`HJRQ` AS `stamp`,`dr_kjcg_jl`.`note` AS `note`,`dr_hjcg`.`HJRQ` AS `HJRQ`,`dr_hjcg`.`FZRXM` AS `FZRXM`,`dr_hjcg`.`DWMC` AS `DWMC`,`dr_hjcg`.`DWH` AS `DWH`,`dr_hjcg`.`CGHJLBM` AS `CGHJLBM`,`dr_hjcg`.`JLDJM` AS `JLDJM`,`dr_hjcg`.`HJJBM` AS `HJJBM` from (`dr_kjcgryxx_jl` `dr_kjcg_jl` left join `dr_hjcgjbsjxx` `dr_hjcg` on((`dr_kjcg_jl`.`HJCGBH` = `dr_hjcg`.`HJCGBH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_kjcgryxx_lw
-- ----------------------------
DROP VIEW IF EXISTS `view_kjcgryxx_lw`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_kjcgryxx_lw` AS select `dr`.`id` AS `id`,`jz`.`DWH` AS `DWH`,`sl`.`SLLX` AS `SLLX`,`sl`.`SLBH` AS `SLBH`,`sl`.`SLSJ` AS `SLSJ`,`sl`.`SLQH` AS `SLQH`,`dr`.`RYH` AS `RYH`,`dr`.`RYH` AS `JZGH`,`dr`.`JSM` AS `JSM`,`dr`.`ZXZS` AS `ZXZS`,`dr`.`PMZRS` AS `PMZRS`,`dr`.`GXL` AS `GXL`,`dr`.`XM` AS `XM`,`dr`.`SZDW` AS `SZDW`,`dr`.`RYLX` AS `RYLX`,`dr`.`LWBH` AS `LWBH`,`dr`.`KJCGRYBH` AS `KJCGRYBH`,`qk`.`LWMC` AS `LWMC`,`qk`.`LWLXM` AS `LWLXM`,`qk`.`DYZZ` AS `DYZZ`,`qk`.`CYRY` AS `CYRY`,`qk`.`TXZZ` AS `TXZZ`,`qk`.`JSQK` AS `JSQK`,`qk`.`JQY` AS `JQY`,`qk`.`WDWZZPX` AS `WDWZZPX`,`qk`.`BZXYBJZDSYS` AS `BZXYBJZDSYS`,`kj`.`FBRQ` AS `FBRQ`,`kj`.`JH` AS `JH`,`kj`.`QH` AS `QH`,`kj`.`LRSJ` AS `LRSJ`,`kj`.`FBRQ` AS `stamp`,`dr`.`note` AS `note` from (((((`dr_kjcgryxx_lw` `dr` left join `dc_kjcgryxx_lw` `dc` on((`dc`.`LWBH` = `dr`.`LWBH`))) left join `dr_kjlwslqk` `sl` on((`sl`.`LWBH` = `dr`.`LWBH`))) left join `dr_kjqklwjbsjxx` `qk` on((`qk`.`LWBH` = `dr`.`LWBH`))) left join `dr_kjlwfbxx` `kj` on((`kj`.`LWBH` = `dr`.`LWBH`))) left join `dr_jzgjcsjxx` `jz` on((`jz`.`JZGH` = `dr`.`RYH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_ksapxx
-- ----------------------------
DROP VIEW IF EXISTS `view_ksapxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_ksapxx` AS select `dr`.`id` AS `id`,`dr`.`JKRGH` AS `JZGH`,`dr`.`KSRQ` AS `stamp`,`dr`.`note` AS `note`,`dr`.`KSRQ` AS `KSRQ`,`dr`.`KSSC` AS `KSSC`,`dr`.`KSFSLXM` AS `KSFSLXM`,`dr`.`KCH` AS `KCH`,`dr`.`KSJSH` AS `KSJSH`,`dr`.`JKRXM` AS `JKRXM`,`dr`.`KSRS` AS `KSRS`,`dr`.`SSXY` AS `SSXY`,`jkr`.`DWH` AS `JSSSXY` from ((`dr_ksapxx` `dr` left join `dr_jzgjcsjxx` `jkr` on((`jkr`.`JZGH` = `dr`.`JKRGH`))) left join `dr_pksjxx` `pk` on((`pk`.`KCH` = `dr`.`KCH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_sxxss
-- ----------------------------
DROP VIEW IF EXISTS `view_sxxss`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_sxxss` AS select `pk`.`id` AS `id`,`pk`.`JSGH` AS `JSGH`,`pk`.`JSGH` AS `JZGH`,`pk`.`JSXM` AS `JSXM`,`pk`.`KKXND` AS `KKXND`,`pk`.`KKXQM` AS `KKXQM`,`pk`.`HBS` AS `HBS`,`pk`.`SXZS` AS `SXZS`,`pk`.`ZLXS` AS `ZLXS`,`kc`.`KCH` AS `KCH`,`dr_jzg`.`DWH` AS `DWH`,`xn`.`XQQSSJ` AS `stamp`,`pk`.`note` AS `note` from (((`dr_sspksjxx` `pk` left join `dr_kcsjxx` `kc` on((`kc`.`KCH` = `pk`.`KCH`))) left join `dr_xnxqxx` `xn` on((`xn`.`XQQSSJ` = `pk`.`KKXQM`))) left join `dr_jzgjcsjxx` `dr_jzg` on((`dr_jzg`.`JZGH` = `pk`.`JSGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_xmjfxx
-- ----------------------------
DROP VIEW IF EXISTS `view_xmjfxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_xmjfxx` AS select `dr`.`id` AS `id`,`dr`.`JHJFZE` AS `JHJFZE`,`dr`.`XMJFLYM` AS `XMJFLYM`,`dr`.`BRRQ` AS `BRRQ`,`dr`.`BKS` AS `BKS`,`dr`.`ZCRQ` AS `ZCRQ`,`dr`.`BFXZDWJF` AS `BFXZDWJF`,`dr`.`XMPZBH` AS `XMPZBH`,`dr`.`JBRXM` AS `JBRXM`,`dr`.`XMBH` AS `XMBH`,`dr`.`ZZKS` AS `ZZKS`,`dr`.`JZGH` AS `JZGH`,`jz`.`DWH` AS `DWH`,`dw`.`DWMC` AS `DWMC`,`dr`.`BRRQ` AS `stamp`,`dr`.`note` AS `note` from (((`dr_xmjfxx` `dr` left join `dc_xmjfxx` `dc` on((`dc`.`XMBH` = `dr`.`XMBH`))) left join `dr_jzgjcsjxx` `jz` on((`jz`.`JZGH` = `dr`.`JZGH`))) left join `dr_zzjgjbsjxx` `dw` on((`dw`.`DWH` = `jz`.`DWH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_xmryxx
-- ----------------------------
DROP VIEW IF EXISTS `view_xmryxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_xmryxx` AS select `dr`.`id` AS `id`,`dr`.`RYH` AS `RYH`,`dr`.`RYH` AS `JZGH`,`jz`.`XM` AS `XM`,`jz`.`DWH` AS `DWH`,`jz`.`DWMC` AS `DWMC`,`jz`.`CSRQ` AS `CSRQ`,`dr`.`XMBH` AS `XMBH`,`dr`.`GZL` AS `GZL`,`dr`.`MNGZYS` AS `MNGZYS`,`dr`.`JSM` AS `JSM`,`dr`.`RYLX` AS `RYLX`,`dr`.`SMSX` AS `SMSX`,`dr`.`XKMLKJM` AS `XKMLKJM`,`dr`.`stamp` AS `stamp`,`dr`.`note` AS `note` from (`dr_xmryxx` `dr` left join `view_jzgjcsjxx` `jz` on((`jz`.`JZGH` = `dr`.`RYH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_xnxqxx
-- ----------------------------
DROP VIEW IF EXISTS `view_xnxqxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_xnxqxx` AS select `xn`.`id` AS `id`,`xn`.`JZGH` AS `JZGH`,`xn`.`XQMC` AS `XQMC`,`xn`.`XQQSSJ` AS `XQQSSJ`,`xn`.`XNXQM` AS `XNXQM`,`xn`.`XNDM` AS `XNDM`,`xn`.`XQDM` AS `XQDM`,`xn`.`XNMC` AS `XNMC`,`xn`.`QSSKZ` AS `QSSKZ`,`xn`.`ZZSKZ` AS `ZZSKZ`,`xn`.`XQLXDM` AS `XQLXDM`,`xn`.`XQLXMC` AS `XQLXMC`,`xn`.`SFDQXQ` AS `SFDQXQ`,`dr_jzg`.`DWH` AS `DWH`,`xn`.`XQQSSJ` AS `stamp`,`xn`.`note` AS `note` from (`dr_xnxqxx` `xn` left join `dr_jzgjcsjxx` `dr_jzg` on((`dr_jzg`.`JZGH` = `xn`.`JZGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_yjsjxzxs
-- ----------------------------
DROP VIEW IF EXISTS `view_yjsjxzxs`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_yjsjxzxs` AS select `pk`.`id` AS `id`,`pk`.`JSGH` AS `JSGH`,`pk`.`JSGH` AS `JZGH`,`pk`.`JSXM` AS `JSXM`,`pk`.`KKXND` AS `KKXND`,`pk`.`KKXQM` AS `KKXQM`,`kc`.`LLXS` AS `JHXSS`,`pk`.`ZKJHXS` AS `ZKJHXS`,`pk`.`ZLXS` AS `ZLXS`,`pk`.`HBS` AS `HBS`,`pk`.`SKBJH` AS `SKBJH`,`pk`.`WYKCTJM` AS `WYKCTJM`,`pk`.`JXMSJBM` AS `JXMSJBM`,`pk`.`KCJBM` AS `KCJBM`,`kc`.`KCH` AS `KCH`,`dr_jzg`.`DWH` AS `DWH`,`xn`.`XQQSSJ` AS `stamp`,`pk`.`note` AS `note` from (((`dr_yjspksjxx` `pk` left join `dr_kcsjxx` `kc` on((`kc`.`KCH` = `pk`.`KCH`))) left join `dr_xnxqxx` `xn` on((`xn`.`XQQSSJ` = `pk`.`KKXQM`))) left join `dr_jzgjcsjxx` `dr_jzg` on((`dr_jzg`.`JZGH` = `pk`.`JSGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_zdbylwxss
-- ----------------------------
DROP VIEW IF EXISTS `view_zdbylwxss`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_zdbylwxss` AS select `dr`.`id` AS `id`,`jkr`.`DWH` AS `DWH`,`dr`.`XQ` AS `stamp`,`dr`.`note` AS `note`,`dr`.`XQ` AS `XQ`,`dr`.`JZGH` AS `JZGH`,`dr`.`JSXM` AS `JSXM`,`dr`.`ZDZS` AS `ZDZS`,`dr`.`ZDPTXSS` AS `ZDPTXSS`,`dr`.`ZDSYXSS` AS `ZDSYXSS`,`dr`.`JXMSJBM` AS `JXMSJBM` from (`dr_zdbylwsjxx` `dr` left join `dr_jzgjcsjxx` `jkr` on((`jkr`.`JZGH` = `dr`.`JZGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_zdsyxss
-- ----------------------------
DROP VIEW IF EXISTS `view_zdsyxss`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_zdsyxss` AS select `pk`.`id` AS `id`,`pk`.`JSGH` AS `JSGH`,`pk`.`JSGH` AS `JZGH`,`pk`.`JSXM` AS `JSXM`,`pk`.`KKXND` AS `KKXND`,`pk`.`KKXQM` AS `KKXQM`,`kc`.`SYXS` AS `SYXS`,`pk`.`KCJBM` AS `KCJBM`,`pk`.`SYZS` AS `SYZS`,`kc`.`KCH` AS `KCH`,`dr_jzg`.`DWH` AS `DWH`,`xn`.`XQQSSJ` AS `stamp`,`pk`.`note` AS `note` from (((`dr_sypksjxx` `pk` left join `dr_kcsjxx` `kc` on((`kc`.`KCH` = `pk`.`KCH`))) left join `dr_xnxqxx` `xn` on((`xn`.`XQQSSJ` = `pk`.`KKXQM`))) left join `dr_jzgjcsjxx` `dr_jzg` on((`dr_jzg`.`JZGH` = `pk`.`JSGH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_zlcgjbsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_zlcgjbsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_zlcgjbsjxx` AS select `dr_zl`.`id` AS `id`,`dr_zl`.`ZLCGBH` AS `ZLCGBH`,`dr_zl`.`ZLCGMC` AS `ZLCGMC`,`dr_zl`.`DWH` AS `DWH`,`dr_zl`.`SQBH` AS `SQBH`,`dr_zl`.`XKLYM` AS `XKLYM`,`dr_zl`.`ZLLXM` AS `ZLLXM`,`dr_zl`.`PZRQ` AS `PZRQ`,`dr_zl`.`PZXSM` AS `PZXSM`,`dr_zl`.`ZLZSBH` AS `ZLZSBH`,`dr_zl`.`FLZTM` AS `FLZTM`,`dr_zl`.`JNZLNFRQ` AS `JNZLNFRQ`,`dr_zl`.`JNJE` AS `JNJE`,`dr_zl`.`SSXMBH` AS `SSXMBH`,`dr_zl`.`GJDQM` AS `GJDQM`,`dr_zl`.`GJZLZFLH` AS `GJZLZFLH`,`dr_zl`.`PCTHZLGJDQM` AS `PCTHZLGJDQM`,`dr_zl`.`SQGGH` AS `SQGGH`,`dr_zl`.`SQGGRQ` AS `SQGGRQ`,`dr_zl`.`SQMC` AS `SQMC`,`dr_zl`.`ZLDLJG` AS `ZLDLJG`,`dr_zl`.`ZLDLR` AS `ZLDLR`,`dr_zl`.`ZLQR` AS `ZLQR`,`dr_zl`.`ZLZZRQ` AS `ZLZZRQ`,`dr_zl`.`XKMLKJM` AS `XKMLKJM`,`dr_zl`.`ZLSQRQ` AS `ZLSQRQ`,`dr_zl`.`ZZM` AS `ZZM`,`dr_zl`.`ZZBH` AS `ZZBH`,`dr_zl`.`PZRQ` AS `stamp`,`dr_zl`.`note` AS `note` from (`dr_zlcgjbsjxx` `dr_zl` left join `dc_zlcgjbsjxx` `dc_zl` on((`dr_zl`.`ZLCGBH` = `dc_zl`.`ZLCGBH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_zzjgjbsjxx
-- ----------------------------
DROP VIEW IF EXISTS `view_zzjgjbsjxx`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_zzjgjbsjxx` AS select `dr`.`id` AS `id`,`dr`.`DWH` AS `DWH`,`dr`.`DWMC` AS `DWMC`,`dr`.`DWYWMC` AS `DWYWMC`,`dr`.`DWJC` AS `DWJC`,`dr`.`DWYWJC` AS `DWYWJC`,`dr`.`DWJP` AS `DWJP`,`dr`.`DWDZ` AS `DWDZ`,`dr`.`SZXQ` AS `SZXQ`,`dr`.`LSDWH` AS `LSDWH`,`dr`.`DWLBM` AS `DWLBM`,`dr`.`DWBBM` AS `DWBBM`,`dr`.`DWYXBS` AS `DWYXBS`,`dr`.`SXRQ` AS `SXRQ`,`dr`.`SFST` AS `SFST`,`dr`.`JLNY` AS `JLNY`,`dr`.`DWFZRH` AS `DWFZRH`,`dr`.`stamp` AS `stamp`,`dr`.`note` AS `note` from (`dr_zzjgjbsjxx` `dr` left join `dc_zzjgjbsjxx` `dc` on((`dc`.`DWH` = `dr`.`DWH`))) where (1 = 1);

-- ----------------------------
-- View structure for view_sysuser
-- ----------------------------
DROP VIEW IF EXISTS `view_sysuser`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `view_sysuser` AS select `su`.`id` AS `id`,`su`.`payroll` AS `payroll`,`su`.`password` AS `password`,`su`.`time_pwd` AS `time_pwd`,`su`.`role_id` AS `role_id`,`su`.`usertype_id` AS `usertype_id`,`ro`.`role_name` AS `role_name`,`jg`.`JZGH` AS `JZGH`,`jg`.`XM` AS `XM`,`jg`.`DWH` AS `DWH`,`zz`.`DWMC` AS `DWMC` from (((`jx_sysuser` `su` left join `jx_role` `ro` on((`ro`.`id` = `su`.`role_id`))) left join `view_jzgjcsjxx` `jg` on((`jg`.`JZGH` = `su`.`payroll`))) left join `view_zzjgjbsjxx` `zz` on((`zz`.`DWH` = `jg`.`DWH`)));

SET FOREIGN_KEY_CHECKS = 1;
