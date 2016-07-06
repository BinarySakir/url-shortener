CREATE TABLE `urls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `long_url` text COLLATE utf8_bin NOT NULL,
  `hits` int(11) NOT NULL,
  PRIMARY KEY (`id`)
)