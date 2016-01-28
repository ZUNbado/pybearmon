-- front-end tables
CREATE TABLE checks (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(64) NOT NULL, type VARCHAR(32) NOT NULL, data VARCHAR(512) NOT NULL, check_interval INT NOT NULL DEFAULT 60, status ENUM ('online', 'offline') DEFAULT 'online', last_checked TIMESTAMP DEFAULT '2010-01-01 00:00:00', confirmations INT NOT NULL DEFAULT 0, `lock` VARCHAR(16) NOT NULL DEFAULT '', last_locked TIMESTAMP DEFAULT '2010-01-01 00:00:00');
CREATE TABLE contacts (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, type VARCHAR(32) NOT NULL, data VARCHAR(512));
CREATE TABLE alerts (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, check_id INT NOT NULL, contact_id INT NOT NULL, type ENUM ('up', 'down', 'both') DEFAULT 'both');

-- data tables
CREATE TABLE check_events (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, check_id INT NOT NULL, type ENUM ('up', 'down'), time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- user table
CREATE TABLE IF NOT EXISTS `users` (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NOT NULL,
     `email` varchar(255) NOT NULL,
     `password` varchar(255) NOT NULL,
     PRIMARY KEY (`id`)
   ) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;
