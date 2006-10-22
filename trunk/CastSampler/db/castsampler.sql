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
INSERT INTO "django_session" VALUES('32b61f225cb17bc7e027541916d4f99c', 'KGRwMQpTJ19hdXRoX3VzZXJfYmFja2VuZCcKcDIKUydkamFuZ28uY29udHJpYi5hdXRoLmJhY2tl
bmRzLk1vZGVsQmFja2VuZCcKcDMKc1MnX2F1dGhfdXNlcl9pZCcKcDQKSTEKcy5kYjI2ODY1ZjFh
MGNiNDA0YjJkNDhiODVhOGFlZWZmMQ==
', '2006-11-04 11:44:15.846512');
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
CREATE TABLE "registration_userprofile" (
    "user_id" integer NOT NULL PRIMARY KEY REFERENCES "auth_user" ("id"),
    "activation_key" varchar(40) NOT NULL,
    "key_expires" datetime NOT NULL
);
CREATE TABLE "oneoffcast_queueitem" (
    "id" integer NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "podcast_id" integer NOT NULL,
    "title" varchar(512) NOT NULL,
    "description" text NOT NULL,
    "link" varchar(200) NOT NULL,
    "item_enclosure_url" varchar(200) NOT NULL,
    "item_enclosure_length" integer NOT NULL,
    "item_enclosure_mime_type" varchar(200) NOT NULL,
    "add_date" datetime NOT NULL,
    "author_name" varchar(128) NOT NULL,
    "author_email" varchar(75) NOT NULL
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
INSERT INTO "oneoffcast_podcast" VALUES(2, 'hackoff.com - podcast version', 'hackoff.com: An historic murder mystery set in the internet bubble and rubble, by Tom Evslin', 'http://www.hackoff.com/blook/', 'http://localhost/~dhellmann/OneOffCast/hackoff.xml', '2006-10-21 12:26:45.396620', '', '', '', 1);
INSERT INTO "oneoffcast_podcast" VALUES(3, 'Agile Toolkit Podcast', 'Talk for the Agile crowd.', 'http://agiletoolkit.libsyn.com', 'http://localhost/~dhellmann/OneOffCast/agile.xml', '2006-10-21 12:29:15.705540', '', '', '', 1);
CREATE TABLE "oneoffcast_podcast_users" (
    "id" integer NOT NULL PRIMARY KEY,
    "podcast_id" integer NOT NULL REFERENCES "oneoffcast_podcast" ("id"),
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    UNIQUE ("podcast_id", "user_id")
);
INSERT INTO "oneoffcast_podcast_users" VALUES(2, 2, 1);
INSERT INTO "oneoffcast_podcast_users" VALUES(3, 3, 1);
COMMIT;
