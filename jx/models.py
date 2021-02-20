# coding=utf-8

from django.db import models


class Usertype(models.Model):
    usertype_name = models.CharField(max_length=64, default="")


class Menu(models.Model):
    menu_name = models.CharField(max_length=128)
    menu_classify = models.CharField(max_length=128)
    menu_addr = models.CharField(max_length=128, default="")
    menu_icon = models.CharField(max_length=128, null=True)


class Role(models.Model):
    role_name = models.CharField(max_length=64, default='')
    menu = models.ManyToManyField(Menu)


class SysUser(models.Model):
    payroll = models.CharField(max_length=32, default='')
    password = models.CharField(max_length=256, default='111111')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    usertype = models.ForeignKey(Usertype, on_delete=models.CASCADE)
    time_pwd = models.DateTimeField(auto_now_add=True)


"""
USE kpi;
DROP TABLE `jx_role_menu`;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
