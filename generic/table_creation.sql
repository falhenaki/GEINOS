CREATE TABLE `Device_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`device_group_name`)
);

CREATE TABLE `Devices` (
  `vendor_id` int(11) NOT NULL,
  `serial_number` int(11) NOT NULL,
  `model_number` varchar(50) NOT NULL DEFAULT '',
  `device_status` enum('UNAUTHORIZED','AUTHORIZED','PROVISIONED') NOT NULL DEFAULT 'UNAUTHORIZED',
  `last_modified` datetime NOT NULL,
  `IP` varchar(39) NOT NULL DEFAULT '',
  PRIMARY KEY (`vendor_id`,`serial_number`,`model_number`)
);

CREATE TABLE `Devices_in_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `vendor_id` int(11) NOT NULL,
  `serial_number` int(11) NOT NULL,
  `model_number` int(11) NOT NULL,
  PRIMARY KEY (`device_group_name`,`vendor_id`,`serial_number`,`model_number`)
);

CREATE TABLE `Logs` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type` tinyint(4) DEFAULT NULL,
  `log_message` varchar(100) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `role` enum('ADMIN','OPERATOR') DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  PRIMARY KEY (`log_id`)
);

CREATE TABLE `Templates` (
  `Name` varchar(100) NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `template_file` blob,
  PRIMARY KEY (`Name`)
);
CREATE TABLE `User_Groups` (
  `role_type` enum('ADMIN','OPERATOR') NOT NULL DEFAULT 'OPERATOR',
  `group_name` varchar(50) NOT NULL,
  PRIMARY KEY (`group_name`)
);

CREATE TABLE `Users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `passwordhash` varchar(128) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `role_type` enum('ADMIN','OPERATOR') NOT NULL DEFAULT 'OPERATOR',
  `email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `Users_in_Groups` (
  `group_name` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL
);

