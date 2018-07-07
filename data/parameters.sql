insert into Parameters values ('x_ip', '192.168.9.9', null, 'SCALAR', '2018-01-23 19:09:54', null, null);
insert into Parameters values ('y_ip', '1.1.1.2', null, 'SCALAR', '2018-03-10 13:44:32', null, null);
insert into Parameters values ('x_bool' 'True', null, 'SCALAR', '2016-09-26 16:12:11', null, null);
insert into Parameters values ('z_ip', '9.2.1.4', null, 'SCALAR', '2016-07-01 00:34:43', null, null);

insert into Parameters values ('y_range', '1.1.8.0', '1.1.8.255', 'RANGE', '2018-03-10 13:44:32', '1.1.8.0', null);
insert into Parameters values ('x_range' '1.2.3.4', '1.2.3.255', 'RANGE', '2016-09-26 16:12:11', '1.2.3.20', null);
insert into Parameters values ('z_range', '9.2.1.4', '9.2.1.30', 'RANGE', '2016-07-01 00:34:43', '9.2.1.4', null);

insert into Parameters values ('k_dynamic', '192.168.0.0/16', null, 'DYNAMIC', '2018-01-23 19:09:54', null, 'ntp');
insert into Parameters values ('y_dynamic', '1.1.1.0/24', null, 'DYNAMIC', '2018-03-10 13:44:32', null, 'ntp');
insert into Parameters values ('x_dynamic' '1.0.0.0/8', null, 'DYNAMIC', '2016-09-26 16:12:11', null, 'lo1');
insert into Parameters values ('z_dynamic', '9.2.1.0/24', null, 'DYNAMIC', '2016-07-01 00:34:43', null, 'lo1');

insert into Parameters values ('list_1', null, null, 'LIST', '2018-04-12 14:41:12', 3, null);
insert into Parameters values ('list_2', null, null, 'LIST', '2018-06-11 12:40:22', 1, null);
insert into Parameters values ('list_3', null, null, 'LIST', '2018-02-08 11:44:31', 0, null);
insert into Parameters values ('list_4', null, null, 'LIST', '2018-08-10 15:42:42', 0, null);