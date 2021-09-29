CREATE TABLE `scan_status` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `scan_request_id` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '',
  `scan_status` varchar(20) COLLATE utf8_bin NOT NULL DEFAULT 'IN PROGRESS',
  `scan_step` varchar(50) COLLATE utf8_bin NOT NULL DEFAULT '',
  `is_completed` tinyint(1) DEFAULT 0,
  `is_error` tinyint(1) DEFAULT 0,
  `modified` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
