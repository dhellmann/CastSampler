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
INSERT INTO "auth_user" VALUES(1, 'dhellmann', '', '', 'oneoffcast@gmail.com', 'sha1$2113b$5ac39071f072894ce489992f8523afaec6516572', 1, 1, 1, '2006-10-21 11:17:01.764001', '2006-09-10 19:23:55.357882');
INSERT INTO "auth_user" VALUES(2, 'test', '', '', '', 'sha1$5337a$d969ad84028e9f294f67d7963e77c5fa75032f4a', 0, 1, 0, '2006-09-17 10:14:13.000715', '2006-09-17 10:14:13.000715');
INSERT INTO "auth_user" VALUES(3, 'nonadmin', '', '', 'doug-oneoffcast@hellfly.net', 'sha1$ccd81$ed10601d1d8cb7c317f05269c4faba7db62a8166', 0, 0, 0, '2006-10-09 08:20:46.009972', '2006-10-09 08:20:46.009972');
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
INSERT INTO "django_session" VALUES('f9dae947ea47fa138711e884f3e81f36', 'KGRwMQpTJ19hdXRoX3VzZXJfYmFja2VuZCcKcDIKUydkamFuZ28uY29udHJpYi5hdXRoLmJhY2tl
bmRzLk1vZGVsQmFja2VuZCcKcDMKc1MnX2F1dGhfdXNlcl9pZCcKcDQKSTEKcy5kYjI2ODY1ZjFh
MGNiNDA0YjJkNDhiODVhOGFlZWZmMQ==
', '2006-11-11 13:04:01.421302');
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
CREATE TABLE "oneoffcast_podcast_users" (
    "id" integer NOT NULL PRIMARY KEY,
    "podcast_id" integer NOT NULL REFERENCES "oneoffcast_podcast" ("id"),
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("podcast_id", "user_id")
);
INSERT INTO "oneoffcast_podcast_users" VALUES(2, 2, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(3, 3, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(4, 4, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(5, 5, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(6, 6, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(7, 7, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(8, 8, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(9, 9, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(10, 10, 1);
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
INSERT INTO "oneoffcast_queueitem" VALUES(1, 1, 3, 'Agile06 - Ward Cunningham - Eclipse Foundation', 'Ward and I talk about his new position as the Director of Committer Community Development at Eclipse.  He discusses the release of Callisto by the Eclipse foundation, itâs Agile roots and other fun tool related topics.-bob', 'http://agiletoolkit.libsyn.com/index.php?post_id=131922', 'http://media.libsyn.com/media/agiletoolkit/Agile2006_WardCunningham.mp3', 11623852, 'audio/mpeg', '2006-10-28 13:46:13.047197', 'Bob Payne', 'n/a');
INSERT INTO "oneoffcast_queueitem" VALUES(2, 1, 3, 'Agile06 - Mary Lynn Manns - Fearless Chage and Agile 2007', 'Mary Lynn is the co author of Fearless Change and the Chair of the Agile 2007 Conference here in Washington DC.  What can I say ... the book is great and I look forward to working with her on Agile 2007.I did not get as much time to talk with her at the conference as I would have liked since she was swamped.  - bob ', 'http://agiletoolkit.libsyn.com/index.php?post_id=129015', 'http://media.libsyn.com/media/agiletoolkit/Agile2006_MaryLynnManns.mp3', 6550643, 'audio/mpeg', '2006-10-28 13:46:25.855880', 'Bob Payne', 'n/a');
INSERT INTO "oneoffcast_queueitem" VALUES(3, 1, 7, 'Pre-conference podcast - Hugh MacLeod', 'Download audio file (hugh_macleod_podcast.mp3)
Podcast length - 31:22
Welcome to the IT@Cork pre-conference PR podcasts. In this podcast series, kindly sponsored by Blacknight Solutions, we are talking to some of the speakers in the upcoming 2006 IT@Cork Business and Technology conference.
In this podcast, second in the series we are talking to Hugh MacLeod. Hugh is a blogger, [...]', 'http://blog.itcork.ie/pre-conference-podcast-hugh-macleod/', 'http://www.podtrac.com/pts/redirect.mp3?http://podcasts.tomrafteryit.net/hugh_macleod_podcast.mp3', 15058647, 'audio/mpeg', '2006-10-28 13:51:29.902883', 'IT@Cork', 'tom@tomrafteryit.net');
INSERT INTO "oneoffcast_queueitem" VALUES(4, 1, 6, 'Angel Money', 'Jeff Clavier, the founder of SoftTech VC, talks about his experiences as an angel investor in social media, search, and discovery startups. As we continue our series of interviews about the different states of startup investing, Clavier provides insight into angel investing, and its impact on the rest of the venture funding landscape', 'http://www.businessweek.com/mediacenter/qt/podcasts/podcasting/podcastbiz_10_04_06.mp3', 'http://www.businessweek.com/mediacenter/qt/podcasts/podcasting/podcastbiz_10_04_06.mp3', 7019212, 'audio/mpeg', '2006-10-28 13:52:07.596342', 'Jeff Clavier', 'n/a');
INSERT INTO "oneoffcast_queueitem" VALUES(5, 1, 6, 'New Valuations', 'Fred Wilson and Brad Burnham, the founders of Union Square Ventures in New York, talk about how the new economics of starting and running companies is creating a new way of valuing startups. They also discuss what needs to happen for enterprises to adopt this new generation of technology and why it''s important to be careful these days about the kinds of companies in which they invest', 'http://www.businessweek.com/mediacenter/qt/podcasts/podcasting/podcastbiz_09_27_06.mp3', 'http://www.businessweek.com/mediacenter/qt/podcasts/podcasting/podcastbiz_09_27_06.mp3', 7697277, 'audio/mpeg', '2006-10-28 13:52:11.640682', 'Brad Burnham & Fred Wilson', 'n/a');
INSERT INTO "oneoffcast_queueitem" VALUES(6, 1, 8, 'PodTech Weekly', 'From PodTech News, a closer look at Internet addiction, the all-important price of admission for next year''s gaming consoles, the FBI''s electronic eyes and who they''re watching, and a check-in with JibJab.', 'http://www.podtech.net/home/technology/1383/podtech-weekly', 'http://media.podtech.net/media/2006/10/PID_001287/Podtech_PodTech_News_Weekly_1.mp3', 27237925, 'audio/mpeg', '2006-10-28 13:53:20.213699', 'Editor', 'n/a');
INSERT INTO "oneoffcast_queueitem" VALUES(7, 1, 10, 'BlueDot, Share your favorite sites with your friends', 'Mike Arrington at TechCrunch says he uses BlueDot instead of other bookmarking for social Website sharing services. So, I headed up to Seattle to find out what was behind this innovative company. You’ll meet the entire team, get a demo, and more.', 'http://www.podtech.net/home/technology/1382/bluedot-share-your-favorite-sites-with-your-friends', 'http://media.podtech.net/media/2006/10/PID_001279/Podtech_bluedotvisit_350.mov', 90890592, 'video/mov', '2006-10-29 08:57:45.790780', 'Robert Scoble', 'n/a');
INSERT INTO "oneoffcast_queueitem" VALUES(8, 1, 10, 'LunchMeet Gets Political with TheBallot.org', 'Eddie Codel and Irina Slutsky talk political tech with Seth Walker of Radical Designs on the newly launched voter guide site TheBallot.org. Seth tells us how individuals and groups can use TheBallot.org to create voter guides, endorsements and voter blocs to help get the vote out this election season.', 'http://www.podtech.net/home/technology/1376/lunchmeet-gets-political-with-theballotorg', 'http://media.podtech.net/media/2006/10/PID_001274/Podtech_LM2-TheBallot.mov', 53708204, 'video/mov', '2006-10-29 08:57:49.854932', 'Editor', 'n/a');
COMMIT;
