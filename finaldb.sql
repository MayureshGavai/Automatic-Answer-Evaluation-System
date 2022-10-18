/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - qanlp
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`qanlp` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `qanlp`;

/*Table structure for table `answers` */

DROP TABLE IF EXISTS `answers`;

CREATE TABLE `answers` (
  `id` int(11) NOT NULL auto_increment,
  `sid` varchar(30) default NULL,
  `answers` longtext,
  `img` longtext,
  `marks_given_not` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `answers` */

insert  into `answers`(`id`,`sid`,`answers`,`img`,`marks_given_not`) values (1,'1','last semister we had a group project that took approximately six weeks. Around week four, we realized that one of the grp members was not pulling his weight. The work he agreed to do ','geeks.jpg','Already image marks given to student'),(2,'1','ultimately, that person dropped the course, but by addressing the problem head-on the group was able to divide up our work and complete the project ontime. In the future, i would make sure that the group has wikly met','geeks.jpg','Already image marks given to student'),(3,'1','your new employer is going to invest a lot of tim and money in your treining and development','geeks.jpg','Already image marks given to student'),(4,'1','Your interviwer is trying to understand “why us” This is your chance to tell him what you know about the company and express a genuin enthusiasm for the role. Take a look at the company website and any recent press releases.','geeks.jpg','Already image marks given to student'),(5,'1','you know about the company and express a genuine enthusiasm for the role. Take a look at the company website and any recent press releases.','geeks.jpg','Already image marks given to student'),(6,'2','last semester we had a group project that took approximately six weeks. around week four, we realized that one of the group members was not pulling his weight. The work he agrid to do was not ','1.jpg',NULL),(7,'2','s, and the opportunity to see projects come to life. But if I had to pick one thing that I don’t enjoy as much, I would have to say it’s contract preparation','1.jpg',NULL),(8,'2','and development, and they don’t want to hear that you get bored easily and will likely look for opportunities elsewhere before too long','1.jpg',NULL),(9,'2','your new employr is going to invets a lot of time and money in your training and development','1.jpg',NULL),(10,'2','Your interviewer is trying to understand “Wy us?” Thes is your chance to tell hem ','1.jpg',NULL),(11,'2','last semester we had a group project that took approximately six weeks. around week four, we realized that one of the group members was not pulling his weight. The work he agrid to do was not ','1.jpg',NULL),(12,'2','s, and the opportunity to see projects come to life. But if I had to pick one thing that I don’t enjoy as much, I would have to say it’s contract preparation','1.jpg',NULL),(13,'2','and development, and they don’t want to hear that you get bored easily and will likely look for opportunities elsewhere before too long','1.jpg',NULL),(14,'2','your new employr is going to invets a lot of time and money in your training and development','1.jpg',NULL),(15,'2','Your interviewer is trying to understand “Wy us?” Thes is your chance to tell hem ','1.jpg',NULL);

/*Table structure for table `fuzzy_wuzzy` */

DROP TABLE IF EXISTS `fuzzy_wuzzy`;

CREATE TABLE `fuzzy_wuzzy` (
  `id` int(255) NOT NULL auto_increment,
  `sid` varchar(255) NOT NULL,
  `ans1_ratio` varchar(255) NOT NULL,
  `ans2_ratio` varchar(255) NOT NULL,
  `ans3_ratio` varchar(255) NOT NULL,
  `ans4_ratio` varchar(255) NOT NULL,
  `ans5_ratio` varchar(255) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `fuzzy_wuzzy` */

insert  into `fuzzy_wuzzy`(`id`,`sid`,`ans1_ratio`,`ans2_ratio`,`ans3_ratio`,`ans4_ratio`,`ans5_ratio`) values (1,'1','52','2','59','2','76'),(2,'2','54','78','78','21','52');

/*Table structure for table `marks` */

DROP TABLE IF EXISTS `marks`;

CREATE TABLE `marks` (
  `id` int(255) NOT NULL auto_increment,
  `sid` varchar(255) NOT NULL,
  `studname` varchar(255) NOT NULL,
  `q1` varchar(255) NOT NULL,
  `q2` varchar(255) NOT NULL,
  `q3` varchar(255) NOT NULL,
  `q4` varchar(255) NOT NULL,
  `q5` varchar(255) NOT NULL,
  `final_fuzz_marks` varchar(255) NOT NULL default '',
  `final_gram_marks` varchar(255) NOT NULL default '',
  `final_cosim_marks` varchar(255) NOT NULL,
  `final_length_marks` varchar(255) NOT NULL,
  `pred_marks` varchar(255) NOT NULL,
  `final_marks` varchar(255) default NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `marks` */

insert  into `marks`(`id`,`sid`,`studname`,`q1`,`q2`,`q3`,`q4`,`q5`,`final_fuzz_marks`,`final_gram_marks`,`final_cosim_marks`,`final_length_marks`,`pred_marks`,`final_marks`) values (1,'1','a','227','2.9','6.0','2.4','7.9','25','43','23','23','14','19'),(2,'2','s','227','7.6','7.8','2.2','5.0','28','44','28','23','14',NULL);

/*Table structure for table `student` */

DROP TABLE IF EXISTS `student`;

CREATE TABLE `student` (
  `id` int(255) NOT NULL auto_increment,
  `name` varchar(255) default NULL,
  `mobile` varchar(255) default NULL,
  `email` varchar(255) default NULL,
  `pass` varchar(255) default NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `student` */

insert  into `student`(`id`,`name`,`mobile`,`email`,`pass`) values (1,'a','9856321470','a@gmail.com','a'),(2,'s','8547963210','s@gmail.com','s');

/*Table structure for table `teacher` */

DROP TABLE IF EXISTS `teacher`;

CREATE TABLE `teacher` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(40) default NULL,
  `password` varchar(40) default NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `teacher` */

insert  into `teacher`(`id`,`email`,`password`) values (1,'prathamesh@gmail.com','123'),(2,'abc@gmail.com','456');

/*Table structure for table `teacherquestion` */

DROP TABLE IF EXISTS `teacherquestion`;

CREATE TABLE `teacherquestion` (
  `qid` int(11) NOT NULL auto_increment,
  `question` varchar(1500) character set latin1 default NULL,
  `answer` varchar(6000) character set latin1 default NULL,
  `marks` varchar(11) character set latin1 default NULL,
  UNIQUE KEY `qid` (`qid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `teacherquestion` */

insert  into `teacherquestion`(`qid`,`question`,`answer`,`marks`) values (1,'when a project or assignment didn’t go as planned. How would you approach the situation differently in the future?','Last semester we had a group project that took approximately six weeks. Around week four, we realized that one of the group members was not pulling his weight. The work he agreed to do was not getting done. I took charge of the situation and scheduled a group meeting to discuss the issue. Ultimately, that person dropped the course, but by addressing the problem head-on, the group was able to divide up our work and complete the project on-time. In the future, I would make sure that the group has weekly meet','10'),(2,'What do you enjoy most and least about engineering?','I really love the design work in engineering, the face-to-face interaction with clients, and the opportunity to see projects come to life. But if I had to pick one thing that I don’t enjoy as much, I would have to say it’s contract preparation','10'),(3,'Where do you see yourself five years from now?','Your new employer is going to invest a lot of time and money in your training and development, and they don’t want to hear that you get bored easily and will likely look for opportunities elsewhere before too long','10'),(4,'What new engineering skills have you recently developed?','Since graduating, I’ve been searching for work and also training myself on Civil 3D. I have a basic knowledge of Civil 3D from school, but I thought upgrading my skills would be a valuable investment in my career as an engineer','10'),(5,'Why are you interested in a position with our company?','Your interviewer is trying to understand “Why us?” This is your chance to tell him what you know about the company and express a genuine enthusiasm for the role. Take a look at the company website and any recent press releases.','10');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
