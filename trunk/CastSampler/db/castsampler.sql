BEGIN TRANSACTION;
CREATE TABLE "auth_message" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "message" text NOT NULL
);
CREATE TABLE "auth_group" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(80) NOT NULL UNIQUE
);
CREATE TABLE "auth_user" (
    "id" integer NOT NULL PRIMARY KEY,
    "username" varchar(30) NOT NULL UNIQUE,
    "first_name" varchar(30) NOT NULL,
    "last_name" varchar(30) NOT NULL,
    "email" varchar(75) NOT NULL,
    "password" varchar(128) NOT NULL,
    "is_staff" bool NOT NULL,
    "is_active" bool NOT NULL,
    "is_superuser" bool NOT NULL,
    "last_login" datetime NOT NULL,
    "date_joined" datetime NOT NULL
);
INSERT INTO "auth_user" VALUES(1, 'test', '', '', 'oneoffcast@gmail.com', 'sha1$2113b$5ac39071f072894ce489992f8523afaec6516572', 1, 1, 1, '2006-11-05 09:40:10.547381', '2006-09-10 19:23:55');
INSERT INTO "auth_user" VALUES(2, 'nonadmin', '', '', 'doug-castsampler@hellfly.net', 'sha1$cbd2a$f69f91992e93d8bb23f40b11a0207f832994911d', 0, 1, 0, '2006-11-05 09:41:43.526678', '2006-11-05 09:41:43.526678');
CREATE TABLE "auth_permission" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(50) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" varchar(100) NOT NULL,
    UNIQUE ("content_type_id", "codename")
);
INSERT INTO "auth_permission" VALUES(1, 'Can add message', 1, 'add_message');
INSERT INTO "auth_permission" VALUES(2, 'Can change message', 1, 'change_message');
INSERT INTO "auth_permission" VALUES(3, 'Can delete message', 1, 'delete_message');
INSERT INTO "auth_permission" VALUES(4, 'Can add group', 2, 'add_group');
INSERT INTO "auth_permission" VALUES(5, 'Can change group', 2, 'change_group');
INSERT INTO "auth_permission" VALUES(6, 'Can delete group', 2, 'delete_group');
INSERT INTO "auth_permission" VALUES(7, 'Can add user', 3, 'add_user');
INSERT INTO "auth_permission" VALUES(8, 'Can change user', 3, 'change_user');
INSERT INTO "auth_permission" VALUES(9, 'Can delete user', 3, 'delete_user');
INSERT INTO "auth_permission" VALUES(10, 'Can add permission', 4, 'add_permission');
INSERT INTO "auth_permission" VALUES(11, 'Can change permission', 4, 'change_permission');
INSERT INTO "auth_permission" VALUES(12, 'Can delete permission', 4, 'delete_permission');
INSERT INTO "auth_permission" VALUES(13, 'Can add content type', 5, 'add_contenttype');
INSERT INTO "auth_permission" VALUES(14, 'Can change content type', 5, 'change_contenttype');
INSERT INTO "auth_permission" VALUES(15, 'Can delete content type', 5, 'delete_contenttype');
INSERT INTO "auth_permission" VALUES(16, 'Can add session', 6, 'add_session');
INSERT INTO "auth_permission" VALUES(17, 'Can change session', 6, 'change_session');
INSERT INTO "auth_permission" VALUES(18, 'Can delete session', 6, 'delete_session');
INSERT INTO "auth_permission" VALUES(19, 'Can add site', 7, 'add_site');
INSERT INTO "auth_permission" VALUES(20, 'Can change site', 7, 'change_site');
INSERT INTO "auth_permission" VALUES(21, 'Can delete site', 7, 'delete_site');
INSERT INTO "auth_permission" VALUES(22, 'Can add queue item', 8, 'add_queueitem');
INSERT INTO "auth_permission" VALUES(23, 'Can change queue item', 8, 'change_queueitem');
INSERT INTO "auth_permission" VALUES(24, 'Can delete queue item', 8, 'delete_queueitem');
INSERT INTO "auth_permission" VALUES(25, 'Can add podcast', 9, 'add_podcast');
INSERT INTO "auth_permission" VALUES(26, 'Can change podcast', 9, 'change_podcast');
INSERT INTO "auth_permission" VALUES(27, 'Can delete podcast', 9, 'delete_podcast');
INSERT INTO "auth_permission" VALUES(28, 'Can add log entry', 10, 'add_logentry');
INSERT INTO "auth_permission" VALUES(29, 'Can change log entry', 10, 'change_logentry');
INSERT INTO "auth_permission" VALUES(30, 'Can delete log entry', 10, 'delete_logentry');
INSERT INTO "auth_permission" VALUES(31, 'Can add user profile', 11, 'add_userprofile');
INSERT INTO "auth_permission" VALUES(32, 'Can change user profile', 11, 'change_userprofile');
INSERT INTO "auth_permission" VALUES(33, 'Can delete user profile', 11, 'delete_userprofile');
CREATE TABLE "auth_group_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("group_id", "permission_id")
);
CREATE TABLE "auth_user_groups" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "group_id" integer NOT NULL REFERENCES "auth_group" ("id"),
    UNIQUE ("user_id", "group_id")
);
CREATE TABLE "auth_user_user_permissions" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id"),
    UNIQUE ("user_id", "permission_id")
);
CREATE TABLE "django_content_type" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "app_label" varchar(100) NOT NULL,
    "model" varchar(100) NOT NULL,
    UNIQUE ("app_label", "model")
);
INSERT INTO "django_content_type" VALUES(1, 'message', 'auth', 'message');
INSERT INTO "django_content_type" VALUES(2, 'group', 'auth', 'group');
INSERT INTO "django_content_type" VALUES(3, 'user', 'auth', 'user');
INSERT INTO "django_content_type" VALUES(4, 'permission', 'auth', 'permission');
INSERT INTO "django_content_type" VALUES(5, 'content type', 'contenttypes', 'contenttype');
INSERT INTO "django_content_type" VALUES(6, 'session', 'sessions', 'session');
INSERT INTO "django_content_type" VALUES(7, 'site', 'sites', 'site');
INSERT INTO "django_content_type" VALUES(8, 'queue item', 'oneoffcast', 'queueitem');
INSERT INTO "django_content_type" VALUES(9, 'podcast', 'oneoffcast', 'podcast');
INSERT INTO "django_content_type" VALUES(10, 'log entry', 'admin', 'logentry');
INSERT INTO "django_content_type" VALUES(11, 'user profile', 'registration', 'userprofile');
CREATE TABLE "django_session" (
    "session_key" varchar(40) NOT NULL PRIMARY KEY,
    "session_data" text NOT NULL,
    "expire_date" datetime NOT NULL
);
INSERT INTO "django_session" VALUES('f3c15593af278a24e7120b32e666eaca', 'KGRwMQpTJ19hdXRoX3VzZXJfYmFja2VuZCcKcDIKUydkamFuZ28uY29udHJpYi5hdXRoLmJhY2tl
bmRzLk1vZGVsQmFja2VuZCcKcDMKc1MnX2F1dGhfdXNlcl9pZCcKcDQKSTEKcy5kYjI2ODY1ZjFh
MGNiNDA0YjJkNDhiODVhOGFlZWZmMQ==
', '2006-11-25 09:20:30.130806');
CREATE TABLE "django_site" (
    "id" integer NOT NULL PRIMARY KEY,
    "domain" varchar(100) NOT NULL,
    "name" varchar(50) NOT NULL
);
INSERT INTO "django_site" VALUES(1, 'localhost:7000', 'bender');
CREATE TABLE "django_admin_log" (
    "id" integer NOT NULL PRIMARY KEY,
    "action_time" datetime NOT NULL,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "content_type_id" integer NULL REFERENCES "django_content_type" ("id"),
    "object_id" text NULL,
    "object_repr" varchar(200) NOT NULL,
    "action_flag" smallint unsigned NOT NULL,
    "change_message" text NOT NULL
);
INSERT INTO "django_admin_log" VALUES(1, '2006-09-16 22:02:39.010593', 1, 7, '1', 'hellfly.net', 2, 'Changed domain name and display name.');
INSERT INTO "django_admin_log" VALUES(2, '2006-09-16 22:17:47.852025', 1, 9, '1', '43 Folders', 1, '');
INSERT INTO "django_admin_log" VALUES(3, '2006-09-16 22:30:41.800379', 1, 8, '1', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(4, '2006-09-17 09:01:58.993507', 1, 8, '1', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(5, '2006-09-17 09:04:27.128891', 1, 9, '2', 'InfoWorld Virtualization Podcast', 1, '');
INSERT INTO "django_admin_log" VALUES(6, '2006-09-17 09:05:47.261372', 1, 8, '2', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(7, '2006-09-17 09:52:12.750471', 1, 8, '1', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(8, '2006-09-17 10:00:25.569636', 1, 8, '1', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(9, '2006-09-17 10:02:23.220342', 1, 8, '1', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(10, '2006-09-17 10:15:20.871718', 1, 8, '2', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(11, '2006-09-17 12:13:37.314695', 1, 8, '3', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(12, '2006-09-17 16:01:47.752283', 1, 11, '4', 'UserProfile object', 3, '');
INSERT INTO "django_admin_log" VALUES(13, '2006-09-17 16:01:54.070826', 1, 11, '3', 'UserProfile object', 3, '');
INSERT INTO "django_admin_log" VALUES(14, '2006-09-17 16:02:29.798873', 1, 3, '3', 'dhellmann2', 3, '');
INSERT INTO "django_admin_log" VALUES(15, '2006-09-17 16:05:50.500136', 1, 11, '5', 'UserProfile object', 3, '');
INSERT INTO "django_admin_log" VALUES(16, '2006-09-24 20:22:25.450683', 1, 3, '5', 'dhellmann2', 3, '');
INSERT INTO "django_admin_log" VALUES(17, '2006-09-24 20:22:36.122827', 1, 3, '4', 'dhellmann3', 3, '');
INSERT INTO "django_admin_log" VALUES(18, '2006-09-24 20:22:46.297610', 1, 3, '6', 'dhellmann4', 3, '');
INSERT INTO "django_admin_log" VALUES(19, '2006-09-30 14:27:18.802755', 1, 3, '5', 'dhellmann2', 3, '');
INSERT INTO "django_admin_log" VALUES(20, '2006-09-30 14:27:27.812161', 1, 3, '6', 'dhellmann3', 3, '');
INSERT INTO "django_admin_log" VALUES(21, '2006-09-30 14:27:37.498153', 1, 3, '3', 'dhellmann4', 3, '');
INSERT INTO "django_admin_log" VALUES(22, '2006-09-30 14:27:45.416373', 1, 3, '4', 'dhellmann5', 3, '');
INSERT INTO "django_admin_log" VALUES(23, '2006-09-30 14:54:10.141752', 1, 8, '4', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(24, '2006-09-30 19:25:21.234453', 1, 8, '4', 'QueueItem object', 2, 'Changed description.');
INSERT INTO "django_admin_log" VALUES(25, '2006-09-30 19:25:30.884944', 1, 8, '3', 'QueueItem object', 2, 'Changed description.');
INSERT INTO "django_admin_log" VALUES(26, '2006-09-30 19:25:46.767055', 1, 8, '1', 'QueueItem object', 2, 'Changed description.');
INSERT INTO "django_admin_log" VALUES(27, '2006-10-07 08:41:48.607898', 1, 7, '1', 'hellfly.net', 3, '');
INSERT INTO "django_admin_log" VALUES(28, '2006-10-07 08:43:39.866451', 1, 7, '1', 'localhost', 1, '');
INSERT INTO "django_admin_log" VALUES(29, '2006-10-07 08:44:05.103641', 1, 7, '1', 'localhost', 2, 'Changed display name.');
INSERT INTO "django_admin_log" VALUES(30, '2006-10-07 08:44:24.870781', 1, 7, '1', 'localhost:7000', 2, 'Changed domain name.');
INSERT INTO "django_admin_log" VALUES(31, '2006-10-07 08:48:28.601685', 1, 7, '1', 'localhost:7000', 2, 'Changed display name.');
INSERT INTO "django_admin_log" VALUES(32, '2006-10-07 12:21:57.807866', 1, 8, '4', 'QueueItem object', 2, 'Changed item enclosure mime type.');
INSERT INTO "django_admin_log" VALUES(33, '2006-10-07 14:44:53.504958', 1, 9, '2', 'hackoff.com - podcast version', 3, '');
INSERT INTO "django_admin_log" VALUES(34, '2006-10-07 15:01:36.241473', 1, 9, '1', 'Agile Toolkit Podcast', 3, '');
INSERT INTO "django_admin_log" VALUES(35, '2006-10-07 15:01:44.594784', 1, 9, '2', 'hackoff.com - podcast version', 3, '');
INSERT INTO "django_admin_log" VALUES(36, '2006-10-14 11:00:36.950310', 1, 8, '1', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(37, '2006-10-14 11:04:09.408399', 1, 8, '1', 'QueueItem object', 2, 'Changed link.');
INSERT INTO "django_admin_log" VALUES(38, '2006-10-15 19:19:11.538797', 1, 8, '1', 'QueueItem object', 1, '');
INSERT INTO "django_admin_log" VALUES(39, '2006-10-21 11:17:12.545493', 1, 11, '3', 'UserProfile object', 3, '');
INSERT INTO "django_admin_log" VALUES(40, '2006-10-21 11:17:52.682106', 1, 3, '4', 'emailtest', 3, '');
INSERT INTO "django_admin_log" VALUES(41, '2006-10-21 11:33:26.004619', 1, 3, '4', 'emailtest', 3, '');
INSERT INTO "django_admin_log" VALUES(42, '2006-10-21 11:33:33.778706', 1, 3, '5', 'emailtest2', 3, '');
INSERT INTO "django_admin_log" VALUES(43, '2006-10-21 11:33:43.586740', 1, 3, '6', 'emailtest3', 3, '');
INSERT INTO "django_admin_log" VALUES(44, '2006-10-21 11:45:00.195302', 1, 3, '4', 'emailtest', 3, '');
INSERT INTO "django_admin_log" VALUES(45, '2006-10-21 12:26:30.167160', 1, 9, '2', 'hackoff.com - podcast version', 3, '');
INSERT INTO "django_admin_log" VALUES(46, '2006-10-21 12:29:03.930340', 1, 9, '1', 'Agile Toolkit Podcast', 3, '');
INSERT INTO "django_admin_log" VALUES(47, '2006-10-28 10:12:30.483418', 1, 8, '1', 'QueueItem object', 3, '');
INSERT INTO "django_admin_log" VALUES(48, '2006-10-29 08:04:10.586336', 1, 8, '7', 'QueueItem object', 3, '');
INSERT INTO "django_admin_log" VALUES(49, '2006-10-30 06:36:52.614230', 1, 3, '2', 'test', 3, '');
INSERT INTO "django_admin_log" VALUES(50, '2006-10-30 06:37:12.141228', 1, 3, '1', 'test', 2, 'Changed username, last login and date joined.');
INSERT INTO "django_admin_log" VALUES(51, '2006-11-04 15:49:53.444991', 1, 9, '12', 'Barnes & Noble''s Meet the Writers Podcast', 3, '');
INSERT INTO "django_admin_log" VALUES(52, '2006-11-05 09:41:23.322604', 1, 3, '3', 'nonadmin', 3, '');
CREATE TABLE "registration_userprofile" (
    "user_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id"),
    "activation_key" varchar(40) NOT NULL,
    "key_expires" datetime NOT NULL
);
CREATE TABLE "oneoffcast_podcast" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(256) NOT NULL,
    "description" text NOT NULL,
    "home_url" varchar(200) NOT NULL,
    "feed_url" varchar(200) NOT NULL,
    "registration_date" datetime NOT NULL,
    "contact_name" varchar(128) NOT NULL,
    "contact_email" varchar(75) NOT NULL,
    "notes" text NOT NULL,
    "allowed" bool NOT NULL
);
INSERT INTO "oneoffcast_podcast" VALUES(2, 'LOCAL hackoff.com - podcast version', 'hackoff.com: An historic murder mystery set in the internet bubble and rubble, by Tom Evslin', 'http://www.hackoff.com/blook/', 'http://localhost/~dhellmann/OneOffCast/hackoff.xml', '2006-10-21 12:26:45.396620', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(3, 'LOCAL Agile Toolkit Podcast', 'Talk for the Agile crowd.', 'http://agiletoolkit.libsyn.com', 'http://localhost/~dhellmann/OneOffCast/agile.xml', '2006-10-21 12:29:15.705540', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(4, 'Distributing the Future', '"Distributing the Future" is O''Reilly Media''s weekly podcast featuring the technology and the people behind what you use now and what you''ll use next.

This half hour program includes interviews and commentary on science, technology, related social issues, and just plain fun.', 'http://www.oreillynet.com/future/', 'http://www.oreillynet.com/pub/feed/37?format=rss2', '2006-10-22 10:31:27.898193', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(5, 'FOO Casts: Podcasts from O''Reilly and Friends', 'Podcasts from O''Reilly and Friends', 'http://www.oreillynet.com/podcasts/', 'http://www.oreillynet.com/pub/feed/32?format=rss2', '2006-10-22 10:41:42.330963', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(6, 'BusinessWeek - The Cutting Edge', 'Blogging and Podcasting', 'http://www.blogspotting.net/', 'http://www.businessweek.com/search/podcasts/podcasting.rss', '2006-10-25 19:10:05.169670', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(7, 'The it@cork Blog', 'The IT@Cork podcast - Tom Raftery interviews luminaries from the membership of IT@Cork', 'http://blog.itcork.ie', 'http://blog.itcork.ie/feed/', '2006-10-26 07:25:43.218234', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(8, 'PodTech News - powered by PodTech.net', '- powered by PodTech.net', 'http://www.podtech.net/home/category/PodTech+News', 'http://www.podtech.net/home/PodTech+News/feed', '2006-10-26 20:34:29.726580', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(9, 'web 2.0 - powered by PodTech.net', '- powered by PodTech.net', 'http://www.podtech.net/home/category/web+2.0', 'http://www.podtech.net/home/web+2.0/feed', '2006-10-29 08:03:08.562797', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(10, 'LOCAL web 2.0 - powered by PodTech.net', '- powered by PodTech.net', 'http://www.podtech.net/home/category/web+2.0', 'http://localhost/~dhellmann/OneOffCast/web20.xml', '2006-10-29 08:15:56.814293', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(11, 'Amateur Traveler Podcast | travel for the love of it', 'Travel for the love of it: travel stories, news, tips, tricks and resources', 'http://AmateurTraveler.com/', 'http://feeds.feedburner.com/AmateurTravelerPodcast', '2006-11-04 08:56:20.950751', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(12, 'Barnes & Noble''s Meet the Writers Podcast', 'Hear the latest word on today''s hottest authors with Barnes & Noble''s exclusive Meet the Writers Podcast. Listen as your favorite writers discuss their inspirations and influences, their favorite books, and the reasons they write.', 'http://www.barnesandnoble.com/writers', 'http://www.bn.com/rss/mtw.xml', '2006-11-04 15:50:05.860626', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(13, 'The Jason Calacanis Weblog', 'The Jason Calacanis Weblog', 'http://podcast.calacanis.com', 'http://podcast.calacanis.com/rss.xml', '2006-11-11 08:38:55.665308', '', '', '', 1);
CREATE TABLE "oneoffcast_podcast_users" (
    "id" integer NOT NULL PRIMARY KEY,
    "podcast_id" integer NOT NULL REFERENCES "oneoffcast_podcast" ("id"),
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("podcast_id", "user_id")
);
INSERT INTO "oneoffcast_podcast_users" VALUES(2, 2, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(4, 4, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(5, 5, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(6, 6, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(7, 7, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(8, 8, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(9, 9, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(10, 10, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(12, 12, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(13, 3, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(14, 11, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(15, 13, 1);
CREATE TABLE "oneoffcast_queueitem" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "podcast_id" integer NOT NULL REFERENCES "oneoffcast_podcast" ("id"),
    "title" varchar(512) NOT NULL,
    "summary" text NOT NULL,
    "link" varchar(200) NOT NULL,
    "item_enclosure_url" varchar(200) NOT NULL,
    "item_enclosure_length" integer NOT NULL,
    "item_enclosure_mime_type" varchar(200) NOT NULL,
    "add_date" datetime NOT NULL,
    "author_name" varchar(128) NOT NULL,
    "author_email" varchar(75) NOT NULL
);
INSERT INTO "oneoffcast_queueitem" VALUES(1, 1, 11, '#65 - Seattle, Washington', 'Seattle, Washington', 'http://m.podshow.com/media/2032/episodes/35114/amateurtraveler-35114-11-04-2006.mp3', 'http://m.podshow.com/media/2032/episodes/35114/amateurtraveler-35114-11-04-2006.mp3', 17732354, 'audio/mpeg', '2006-11-06 08:15:33.606753', 'Chris Christensen', 'n/a');
COMMIT;
