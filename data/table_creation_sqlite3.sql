
CREATE TABLE `Device_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `last_modified` datetime,
  `template_name` varchar(100) DEFAULT NULL DEFAULT '',
  `model_name` varchar(100) DEFAULT NULL DEFAULT '',
  PRIMARY KEY (`device_group_name`)
);

CREATE TABLE `Radius` (
  `host` varchar(50),
  `port` varchar(50),
  `secret` varchar(50),
  PRIMARY KEY (`host`)
);

CREATE TABLE `Devices` (
  `vendor_id` varchar(20) NOT NULL DEFAULT '',
  `serial_number` varchar(20) NOT NULL PRIMARY KEY,
  `model_number` varchar(50) NOT NULL DEFAULT '',
  `device_status` varchar(32) NOT NULL DEFAULT 'UNAUTHORIZED',
  `last_modified` datetime NOT NULL,
  `IP` varchar(39) NOT NULL DEFAULT '',
  `config_file` varchar(500) DEFAULT NULL,
  `username` varchar(20) DEFAULT NULL,
  `password` varchar(20) DEFAULT NULL,
  `group` varchar(50) DEFAULT NULL,
  `date_added` datetime DEFAULT NULL,
  `date_provisioned` datetime DEFAULT NULL,
  `date_authorized` datetime DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `cert_required` varchar(32) DEFAULT NULL
);

CREATE TABLE `Devices_in_Groups` (
  `device_group_name` varchar(50) NOT NULL,
  `vendor_id` varchar(20) NOT NULL DEFAULT '',
  `serial_number` varchar(20) NOT NULL DEFAULT '',
  `model_number` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`device_group_name`,`vendor_id`,`serial_number`,`model_number`)
);

CREATE TABLE `ListParameters` (
  `param_name` varchar(50) NOT NULL,
  `param_value` varchar(50) NOT NULL,
  `index` smallint(255) NOT NULL,
  PRIMARY KEY (`param_name`,`param_value`,`index`)
);

CREATE TABLE `Logs` (
  `log_id` INTEGER PRIMARY KEY,
  `event_type` varchar(32) DEFAULT NULL,
  `log_message` varchar(100) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `role` varchar(32) DEFAULT NULL,
  `date_created` datetime DEFAULT NULL,
  `IP` varchar(39) DEFAULT NULL
);

CREATE TABLE `Parameters` (
  `param_name` varchar(50) NOT NULL PRIMARY KEY,
  `start_value` varchar(50) DEFAULT NULL,
  `end_value` varchar(50) DEFAULT NULL,
  `param_type` varchar(32) DEFAULT 'SCALAR',
  `date_created` datetime DEFAULT NULL,
  `current_offset` varchar(50) DEFAULT NULL,
  `interface` varchar(50) DEFAULT NULL
);

CREATE TABLE `Scep` (
  `id` INTEGER PRIMARY KEY,
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
  `client_cert_id` varchar(45) DEFAULT NULL
);

CREATE TABLE `Templates` (
  `name` varchar(100) NOT NULL PRIMARY KEY,
  `date_created` datetime DEFAULT NULL,
  `template_file` varchar(500) DEFAULT NULL
);

CREATE TABLE `User_Groups` (
  `role_type` varchar(128) NOT NULL DEFAULT 'OPERATOR',
  `group_name` varchar(50) NOT NULL,
  PRIMARY KEY (`group_name`)
);

CREATE TABLE `Users` (
  `id` INTEGER PRIMARY KEY,
  `username` varchar(50) NOT NULL,
  `passwordhash` varchar(128) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `role_type` varchar(32) NOT NULL DEFAULT 'OPERATOR',
  `email` varchar(50) DEFAULT NULL
);
