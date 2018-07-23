CREATE TABLE `Device_Group_Filter` (
  `device_group_name` varchar(50) NOT NULL DEFAULT '',
  `filter` varchar(64) NOT NULL DEFAULT '',
  `filter_value` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`device_group_name`,`filter`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Device_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `last_modified` datetime NOT NULL,
  `template_name` varchar(100) DEFAULT NULL,
  `attribute_value` varchar(512) DEFAULT NULL,
  `num_attributes` int(11) DEFAULT NULL,
  PRIMARY KEY (`device_group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Devices` (
  `vendor_id` varchar(20) DEFAULT NULL,
  `serial_number` varchar(20) NOT NULL DEFAULT '',
  `model_number` varchar(50) DEFAULT NULL,
  `device_status` enum('UNAUTHORIZED','AUTHORIZED','PROVISIONED') NOT NULL DEFAULT 'UNAUTHORIZED',
  `last_modified` datetime NOT NULL,
  `IP` varchar(39) DEFAULT NULL,
  `config_file` varchar(500) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  `date_provisioned` datetime DEFAULT NULL,
  `date_authorized` datetime DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `cert_required` enum('TRUE','FALSE') DEFAULT NULL,
  `device_group_filters` int(11) DEFAULT '0',
  `cert_set` enum('TRUE','FALSE','FAIL') DEFAULT NULL,
  `device_group` varchar(45) DEFAULT NULL,
  `device_access` enum('TRUE','FALSE') DEFAULT NULL,
  `config_available` enum('TRUE','FALSE') DEFAULT NULL,
  PRIMARY KEY (`serial_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Devices_in_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `vendor_id` varchar(20) NOT NULL DEFAULT '',
  `serial_number` varchar(20) NOT NULL DEFAULT '',
  `model_number` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`device_group_name`,`vendor_id`,`serial_number`,`model_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `ListParameters` (
  `param_name` varchar(50) NOT NULL,
  `param_value` varchar(50) NOT NULL,
  `index` smallint(255) NOT NULL,
  PRIMARY KEY (`param_name`,`param_value`,`index`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Logs` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type` varchar(32) DEFAULT NULL,
  `log_message` varchar(100) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `role` enum('ADMIN','OPERATOR') DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `IP` varchar(39) DEFAULT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5472 DEFAULT CHARSET=latin1;

CREATE TABLE `Parameters` (
  `param_name` varchar(50) NOT NULL,
  `start_value` varchar(50) DEFAULT NULL,
  `end_value` varchar(50) DEFAULT NULL,
  `param_type` enum('RANGE','SCALAR','LIST','DYNAMIC') DEFAULT 'SCALAR',
  `date_created` datetime DEFAULT NULL,
  `current_offset` varchar(50) DEFAULT NULL,
  `interface` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`param_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Radius` (
  `host` varchar(45) NOT NULL,
  `port` varchar(45) DEFAULT NULL,
  `secret` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`host`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Scep` (
  `id` int(11) NOT NULL,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  `server` varchar(45) DEFAULT NULL,
  `encryptalgo` varchar(45) DEFAULT NULL,
  `digestalgo` varchar(45) DEFAULT NULL,
  `cert_info_id` varchar(45) DEFAULT NULL,
  `ca_server_id` varchar(45) DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `state` varchar(45) DEFAULT NULL,
  `locale` varchar(45) DEFAULT NULL,
  `organization` varchar(45) DEFAULT NULL,
  `org_unit` varchar(45) DEFAULT NULL,
  `cert_server_id` varchar(45) DEFAULT NULL,
  `key_id` varchar(45) DEFAULT NULL,
  `ca_cert_id` varchar(45) DEFAULT NULL,
  `thumbprint` varchar(45) DEFAULT NULL,
  `client_cert_id` varchar(45) DEFAULT NULL,
  `sys_server` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Tasks` (
  `serial_number` varchar(45) NOT NULL,
  `status` enum('WAITING_CERT','WAITING_CONFIG','CERT','CONFIG') DEFAULT NULL,
  PRIMARY KEY (`serial_number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Templates` (
  `name` varchar(100) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `template_file` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `User_Groups` (
  `role_type` enum('ADMIN','OPERATOR') NOT NULL DEFAULT 'OPERATOR',
  `group_name` varchar(50) NOT NULL,
  PRIMARY KEY (`group_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `Users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `passwordhash` varchar(128) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `role_type` enum('ADMIN','OPERATOR') NOT NULL DEFAULT 'OPERATOR',
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=latin1;

CREATE TABLE `Users_in_Groups` (
  `group_name` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

