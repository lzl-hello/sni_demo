/*
 Navicat Premium Data Transfer

 Source Server         : postgres
 Source Server Type    : PostgreSQL
 Source Server Version : 160004 (160004)
 Source Host           : localhost:5432
 Source Catalog        : postgres
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160004 (160004)
 File Encoding         : 65001

 Date: 09/10/2024 17:53:27
*/


-- ----------------------------
-- Table structure for app_protocol
-- ----------------------------
DROP TABLE IF EXISTS "public"."app_protocol";
CREATE TABLE "public"."app_protocol" (
  "app_id" int4 NOT NULL,
  "app_name" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of app_protocol
-- ----------------------------
INSERT INTO "public"."app_protocol" VALUES (1, '微信服务');
INSERT INTO "public"."app_protocol" VALUES (2, '谷歌API');
INSERT INTO "public"."app_protocol" VALUES (3, '哔哩哔哩');
INSERT INTO "public"."app_protocol" VALUES (4, '京东');
INSERT INTO "public"."app_protocol" VALUES (5, '企业微信');
INSERT INTO "public"."app_protocol" VALUES (6, '拼多多');
INSERT INTO "public"."app_protocol" VALUES (7, 'todesk升级');
INSERT INTO "public"."app_protocol" VALUES (8, '百度网盘');
INSERT INTO "public"."app_protocol" VALUES (9, 'QQ空间');
INSERT INTO "public"."app_protocol" VALUES (10, 'Office遥测服务');
INSERT INTO "public"."app_protocol" VALUES (11, 'Office后台服务');
INSERT INTO "public"."app_protocol" VALUES (12, 'Amazon CloudFront CDN服务');
INSERT INTO "public"."app_protocol" VALUES (13, 'Microsoft Edge服务');
INSERT INTO "public"."app_protocol" VALUES (14, '联想浏览器');
INSERT INTO "public"."app_protocol" VALUES (15, 'QQ');
INSERT INTO "public"."app_protocol" VALUES (16, 'Microsoft后台服务');
INSERT INTO "public"."app_protocol" VALUES (17, 'Microsoft账号登录');
INSERT INTO "public"."app_protocol" VALUES (18, 'Microsoft Bing服务');
INSERT INTO "public"."app_protocol" VALUES (19, 'Microsoft MSN');
INSERT INTO "public"."app_protocol" VALUES (20, 'SKype');
INSERT INTO "public"."app_protocol" VALUES (21, 'Windows升级服务');
INSERT INTO "public"."app_protocol" VALUES (22, '腾讯地图');
INSERT INTO "public"."app_protocol" VALUES (23, 'Office服务');
INSERT INTO "public"."app_protocol" VALUES (24, 'Office遥测服务');
INSERT INTO "public"."app_protocol" VALUES (25, 'Office CDN服务');
INSERT INTO "public"."app_protocol" VALUES (26, '百度公共资源');
INSERT INTO "public"."app_protocol" VALUES (27, '百度搜索');
INSERT INTO "public"."app_protocol" VALUES (28, '百度公共资源');
INSERT INTO "public"."app_protocol" VALUES (29, '百度静态资源');
INSERT INTO "public"."app_protocol" VALUES (30, '17K文学网');
INSERT INTO "public"."app_protocol" VALUES (31, '新浪读书');
INSERT INTO "public"."app_protocol" VALUES (32, '榕树下');
INSERT INTO "public"."app_protocol" VALUES (33, '逐浪小说网');
INSERT INTO "public"."app_protocol" VALUES (34, '言情小说吧');
INSERT INTO "public"."app_protocol" VALUES (35, '连城读书');
INSERT INTO "public"."app_protocol" VALUES (36, '猪窝小说网');
INSERT INTO "public"."app_protocol" VALUES (37, '腾讯读书');
INSERT INTO "public"."app_protocol" VALUES (38, '搜狐读书');
INSERT INTO "public"."app_protocol" VALUES (39, '青年文摘');
INSERT INTO "public"."app_protocol" VALUES (40, '西陆文学');
INSERT INTO "public"."app_protocol" VALUES (41, '起点中文网');
INSERT INTO "public"."app_protocol" VALUES (42, '飞卢小说网');
INSERT INTO "public"."app_protocol" VALUES (43, '小说阅读网');
INSERT INTO "public"."app_protocol" VALUES (44, '晋江文学城');
INSERT INTO "public"."app_protocol" VALUES (45, '百度阅读');
INSERT INTO "public"."app_protocol" VALUES (46, '纵横中文网');
INSERT INTO "public"."app_protocol" VALUES (47, '红袖添香');
INSERT INTO "public"."app_protocol" VALUES (48, '网易云阅读');
INSERT INTO "public"."app_protocol" VALUES (49, '搜狐账号登陆');
INSERT INTO "public"."app_protocol" VALUES (50, '微博账号登陆');
INSERT INTO "public"."app_protocol" VALUES (51, 'myqcloud图片服务');
INSERT INTO "public"."app_protocol" VALUES (52, 'myqcloud文件服务');
INSERT INTO "public"."app_protocol" VALUES (53, 'bcebosCDN服务');
INSERT INTO "public"."app_protocol" VALUES (54, '搜狐CDN');
INSERT INTO "public"."app_protocol" VALUES (55, '新浪图片服务');
INSERT INTO "public"."app_protocol" VALUES (56, '网易服务');
INSERT INTO "public"."app_protocol" VALUES (57, '起点账号登陆');
INSERT INTO "public"."app_protocol" VALUES (58, '搜狐汽车');
INSERT INTO "public"."app_protocol" VALUES (90, '唯品会');
INSERT INTO "public"."app_protocol" VALUES (91, '快手短视频');
INSERT INTO "public"."app_protocol" VALUES (92, '腾讯视频');
INSERT INTO "public"."app_protocol" VALUES (93, '爱奇艺');
INSERT INTO "public"."app_protocol" VALUES (94, '优酷');
INSERT INTO "public"."app_protocol" VALUES (95, '哔哩哔哩');
INSERT INTO "public"."app_protocol" VALUES (96, '飞猪旅行');
INSERT INTO "public"."app_protocol" VALUES (97, '12306车票查询');
INSERT INTO "public"."app_protocol" VALUES (98, '世纪佳缘');
INSERT INTO "public"."app_protocol" VALUES (99, 'BOSS直聘');
INSERT INTO "public"."app_protocol" VALUES (100, '新华英才网');
INSERT INTO "public"."app_protocol" VALUES (101, '智联招聘');
INSERT INTO "public"."app_protocol" VALUES (102, 'QQ音乐');
INSERT INTO "public"."app_protocol" VALUES (103, '酷我音乐');
INSERT INTO "public"."app_protocol" VALUES (104, '酷狗音乐');
INSERT INTO "public"."app_protocol" VALUES (105, '网易163邮箱');
INSERT INTO "public"."app_protocol" VALUES (106, '新浪邮箱');
INSERT INTO "public"."app_protocol" VALUES (107, '网易126邮箱');
INSERT INTO "public"."app_protocol" VALUES (108, 'QQ邮箱');
INSERT INTO "public"."app_protocol" VALUES (109, '东方财富网');
INSERT INTO "public"."app_protocol" VALUES (110, '新浪财经');
INSERT INTO "public"."app_protocol" VALUES (111, '证券之星');
INSERT INTO "public"."app_protocol" VALUES (112, '天天基金网');
INSERT INTO "public"."app_protocol" VALUES (113, '腾讯财经');
INSERT INTO "public"."app_protocol" VALUES (114, '中国证券网');
INSERT INTO "public"."app_protocol" VALUES (119, '国金证券');
INSERT INTO "public"."app_protocol" VALUES (121, '百度有驾');
INSERT INTO "public"."app_protocol" VALUES (123, '易车网');
INSERT INTO "public"."app_protocol" VALUES (125, '爱卡汽车');
INSERT INTO "public"."app_protocol" VALUES (126, '新浪汽车');
INSERT INTO "public"."app_protocol" VALUES (127, '搜狐汽车');
INSERT INTO "public"."app_protocol" VALUES (128, '凤凰汽车');
INSERT INTO "public"."app_protocol" VALUES (130, '人人车');
INSERT INTO "public"."app_protocol" VALUES (131, '瓜子二手车');
INSERT INTO "public"."app_protocol" VALUES (132, '汽车之家');
INSERT INTO "public"."app_protocol" VALUES (133, '懂车帝');
INSERT INTO "public"."app_protocol" VALUES (134, '一汽大众');
INSERT INTO "public"."app_protocol" VALUES (135, '一汽集团');
INSERT INTO "public"."app_protocol" VALUES (136, '华晨宝马');
INSERT INTO "public"."app_protocol" VALUES (137, '北京现代');
INSERT INTO "public"."app_protocol" VALUES (138, '陕西重汽');
INSERT INTO "public"."app_protocol" VALUES (139, '潍柴动力');
INSERT INTO "public"."app_protocol" VALUES (140, '雷沃');
INSERT INTO "public"."app_protocol" VALUES (141, '比亚迪');
INSERT INTO "public"."app_protocol" VALUES (142, '柳州重工');
INSERT INTO "public"."app_protocol" VALUES (143, '三一重工');
INSERT INTO "public"."app_protocol" VALUES (144, '中通客车');
INSERT INTO "public"."app_protocol" VALUES (145, '汉德车桥');
INSERT INTO "public"."app_protocol" VALUES (146, '徐工集团');
INSERT INTO "public"."app_protocol" VALUES (147, '山推股份');
INSERT INTO "public"."app_protocol" VALUES (148, '中联重科');
INSERT INTO "public"."app_protocol" VALUES (149, '山重建机');
INSERT INTO "public"."app_protocol" VALUES (150, '东风汽车');
INSERT INTO "public"."app_protocol" VALUES (151, '上汽红岩');
INSERT INTO "public"."app_protocol" VALUES (152, 'JAC江淮汽车');
INSERT INTO "public"."app_protocol" VALUES (153, '大运DAYUN');
INSERT INTO "public"."app_protocol" VALUES (154, '华菱星马CAMC');
INSERT INTO "public"."app_protocol" VALUES (155, '雷克萨斯');
INSERT INTO "public"."app_protocol" VALUES (156, '奔驰');
INSERT INTO "public"."app_protocol" VALUES (157, '福特');
INSERT INTO "public"."app_protocol" VALUES (158, '沃尔沃');
INSERT INTO "public"."app_protocol" VALUES (159, '长安汽车');
INSERT INTO "public"."app_protocol" VALUES (160, '凯迪拉克');
INSERT INTO "public"."app_protocol" VALUES (161, '本田');
INSERT INTO "public"."app_protocol" VALUES (162, '奇瑞');
INSERT INTO "public"."app_protocol" VALUES (163, 'NISSAN日产');
INSERT INTO "public"."app_protocol" VALUES (164, 'SUZUKI铃木');
INSERT INTO "public"."app_protocol" VALUES (165, '五菱');
INSERT INTO "public"."app_protocol" VALUES (166, '别克');
INSERT INTO "public"."app_protocol" VALUES (167, '雪佛兰');
INSERT INTO "public"."app_protocol" VALUES (168, '斗鱼TV');
INSERT INTO "public"."app_protocol" VALUES (169, '知乎');
INSERT INTO "public"."app_protocol" VALUES (170, '天涯社区');
INSERT INTO "public"."app_protocol" VALUES (171, '新浪微博');
INSERT INTO "public"."app_protocol" VALUES (172, '百合网');
INSERT INTO "public"."app_protocol" VALUES (173, '虎扑社区');
INSERT INTO "public"."app_protocol" VALUES (174, '百度贴吧');
INSERT INTO "public"."app_protocol" VALUES (175, '人人网');
INSERT INTO "public"."app_protocol" VALUES (176, '中国银行');
INSERT INTO "public"."app_protocol" VALUES (177, '工商银行');
INSERT INTO "public"."app_protocol" VALUES (178, '农业银行');
INSERT INTO "public"."app_protocol" VALUES (179, '交通银行');
INSERT INTO "public"."app_protocol" VALUES (180, '招商银行');
INSERT INTO "public"."app_protocol" VALUES (181, '兴业银行');
INSERT INTO "public"."app_protocol" VALUES (182, '浦发银行');
INSERT INTO "public"."app_protocol" VALUES (183, '新浪体育');
INSERT INTO "public"."app_protocol" VALUES (184, '虎扑体育');
INSERT INTO "public"."app_protocol" VALUES (185, '搜狐体育');
INSERT INTO "public"."app_protocol" VALUES (186, 'cctv5');
INSERT INTO "public"."app_protocol" VALUES (187, '网易体育');
INSERT INTO "public"."app_protocol" VALUES (188, 'PP体育');
INSERT INTO "public"."app_protocol" VALUES (189, '凤凰体育');
INSERT INTO "public"."app_protocol" VALUES (190, '爱奇艺体育');
INSERT INTO "public"."app_protocol" VALUES (192, '中关村在线');
INSERT INTO "public"."app_protocol" VALUES (193, 'IT之家');
INSERT INTO "public"."app_protocol" VALUES (194, '太平洋手机');
INSERT INTO "public"."app_protocol" VALUES (195, '华为');
INSERT INTO "public"."app_protocol" VALUES (196, '小米');
INSERT INTO "public"."app_protocol" VALUES (197, 'vivo');
INSERT INTO "public"."app_protocol" VALUES (198, '华军软件园');
INSERT INTO "public"."app_protocol" VALUES (199, '苹果手机');
INSERT INTO "public"."app_protocol" VALUES (200, '百度手机助手');
INSERT INTO "public"."app_protocol" VALUES (201, '联想');
INSERT INTO "public"."app_protocol" VALUES (202, '戴尔');
INSERT INTO "public"."app_protocol" VALUES (203, '华硕');
INSERT INTO "public"."app_protocol" VALUES (204, '新浪新闻');
INSERT INTO "public"."app_protocol" VALUES (205, '观察者网');
INSERT INTO "public"."app_protocol" VALUES (206, '环球网');
INSERT INTO "public"."app_protocol" VALUES (207, '参考消息');
INSERT INTO "public"."app_protocol" VALUES (208, '中国新闻网');
INSERT INTO "public"."app_protocol" VALUES (209, '搜狐新闻');
INSERT INTO "public"."app_protocol" VALUES (210, '凤凰军事');
INSERT INTO "public"."app_protocol" VALUES (211, '腾讯新闻');
INSERT INTO "public"."app_protocol" VALUES (212, '网易新闻');
INSERT INTO "public"."app_protocol" VALUES (213, '房天下');
INSERT INTO "public"."app_protocol" VALUES (214, '安居客');
INSERT INTO "public"."app_protocol" VALUES (215, '链家网');
INSERT INTO "public"."app_protocol" VALUES (216, '赶集网');
INSERT INTO "public"."app_protocol" VALUES (217, '爱企查');
INSERT INTO "public"."app_protocol" VALUES (218, '下厨房');
INSERT INTO "public"."app_protocol" VALUES (219, '百姓网');
INSERT INTO "public"."app_protocol" VALUES (220, '大众点评');
INSERT INTO "public"."app_protocol" VALUES (221, '美团网');
INSERT INTO "public"."app_protocol" VALUES (222, '天眼查');
INSERT INTO "public"."app_protocol" VALUES (223, '百度游戏');
INSERT INTO "public"."app_protocol" VALUES (224, '51游戏');
INSERT INTO "public"."app_protocol" VALUES (225, '4399游戏');
INSERT INTO "public"."app_protocol" VALUES (226, '阿里邮箱');
INSERT INTO "public"."app_protocol" VALUES (227, '139邮箱');
INSERT INTO "public"."app_protocol" VALUES (228, 'Outlook邮箱');
INSERT INTO "public"."app_protocol" VALUES (229, '搜狐邮箱');
INSERT INTO "public"."app_protocol" VALUES (230, 'foxmail邮箱');
INSERT INTO "public"."app_protocol" VALUES (231, '成都商报');
INSERT INTO "public"."app_protocol" VALUES (234, 'CSDN论坛');
INSERT INTO "public"."app_protocol" VALUES (235, '博客园');
INSERT INTO "public"."app_protocol" VALUES (263, ' 腾讯会议app');
INSERT INTO "public"."app_protocol" VALUES (264, ' 百度app');
INSERT INTO "public"."app_protocol" VALUES (265, ' 书旗小说app');
INSERT INTO "public"."app_protocol" VALUES (266, ' 安居客app');
INSERT INTO "public"."app_protocol" VALUES (267, ' 扫描全能王app');
INSERT INTO "public"."app_protocol" VALUES (268, ' 全民K歌app');
INSERT INTO "public"."app_protocol" VALUES (269, ' 艺龙旅行app');
INSERT INTO "public"."app_protocol" VALUES (270, ' 陌友app');
INSERT INTO "public"."app_protocol" VALUES (271, ' 飞猪旅行app');
INSERT INTO "public"."app_protocol" VALUES (272, ' 爱奇艺app');
INSERT INTO "public"."app_protocol" VALUES (273, ' 拼多多app');
INSERT INTO "public"."app_protocol" VALUES (274, ' 虎牙直播app');
INSERT INTO "public"."app_protocol" VALUES (275, ' 酷狗音乐app');
INSERT INTO "public"."app_protocol" VALUES (276, ' 今日头条极速版app');
INSERT INTO "public"."app_protocol" VALUES (277, ' 快手app');
INSERT INTO "public"."app_protocol" VALUES (278, ' 美团app');
INSERT INTO "public"."app_protocol" VALUES (279, ' 阿里巴巴1688app');
INSERT INTO "public"."app_protocol" VALUES (280, ' 腾讯视频app');
INSERT INTO "public"."app_protocol" VALUES (281, ' 58同城app');
INSERT INTO "public"."app_protocol" VALUES (282, ' 马蜂窝app');
INSERT INTO "public"."app_protocol" VALUES (283, ' 美团外卖app');
INSERT INTO "public"."app_protocol" VALUES (284, ' UC浏览器app');
INSERT INTO "public"."app_protocol" VALUES (285, ' 网易邮箱大师app');
INSERT INTO "public"."app_protocol" VALUES (286, ' WPS Officeapp');
INSERT INTO "public"."app_protocol" VALUES (287, ' 抖音火山版app');
INSERT INTO "public"."app_protocol" VALUES (288, ' 优酷视频app');
INSERT INTO "public"."app_protocol" VALUES (289, ' 斗鱼app');
INSERT INTO "public"."app_protocol" VALUES (290, ' 今日头条app');
INSERT INTO "public"."app_protocol" VALUES (291, ' 微信读书app');
INSERT INTO "public"."app_protocol" VALUES (292, ' 豆瓣app');
INSERT INTO "public"."app_protocol" VALUES (293, ' 今日水印相机app');
INSERT INTO "public"."app_protocol" VALUES (294, ' 铁路12306app');
INSERT INTO "public"."app_protocol" VALUES (295, ' 智慧树app');
INSERT INTO "public"."app_protocol" VALUES (296, ' 菜鸟app');
INSERT INTO "public"."app_protocol" VALUES (297, ' 云闪付app');
INSERT INTO "public"."app_protocol" VALUES (298, ' 同程旅行app');
INSERT INTO "public"."app_protocol" VALUES (299, ' 好看视频app');
INSERT INTO "public"."app_protocol" VALUES (300, ' 京东app');
INSERT INTO "public"."app_protocol" VALUES (301, ' 携程旅行app');
INSERT INTO "public"."app_protocol" VALUES (302, ' QQ音乐app');
INSERT INTO "public"."app_protocol" VALUES (303, ' 剪映app');
INSERT INTO "public"."app_protocol" VALUES (304, ' 途牛旅游app');
INSERT INTO "public"."app_protocol" VALUES (305, ' 天涯社区app');
INSERT INTO "public"."app_protocol" VALUES (306, ' 工银融e联app');
INSERT INTO "public"."app_protocol" VALUES (307, ' 交管12123app');
INSERT INTO "public"."app_protocol" VALUES (308, ' 唯品会app');
INSERT INTO "public"."app_protocol" VALUES (309, ' 流利说-英语app');
INSERT INTO "public"."app_protocol" VALUES (310, ' 京东金融app');
INSERT INTO "public"."app_protocol" VALUES (311, ' 搜狐新闻app');
INSERT INTO "public"."app_protocol" VALUES (312, ' 知乎app');
INSERT INTO "public"."app_protocol" VALUES (313, ' 网易新闻app');
INSERT INTO "public"."app_protocol" VALUES (314, ' e代驾app');
INSERT INTO "public"."app_protocol" VALUES (315, ' 中国联通app');
INSERT INTO "public"."app_protocol" VALUES (316, ' 中通快递app');
INSERT INTO "public"."app_protocol" VALUES (317, ' 淘特app');
INSERT INTO "public"."app_protocol" VALUES (318, ' 百度地图app');
INSERT INTO "public"."app_protocol" VALUES (319, ' MOMO陌陌app');
INSERT INTO "public"."app_protocol" VALUES (320, ' 淘宝app');
INSERT INTO "public"."app_protocol" VALUES (328, '世纪佳缘app');
INSERT INTO "public"."app_protocol" VALUES (329, 'CSDNapp');
INSERT INTO "public"."app_protocol" VALUES (330, 'e代驾app');
INSERT INTO "public"."app_protocol" VALUES (331, 'QQ音乐app');
INSERT INTO "public"."app_protocol" VALUES (332, '仁和药房网app');
INSERT INTO "public"."app_protocol" VALUES (333, '东方航空app');
INSERT INTO "public"."app_protocol" VALUES (334, '中通快递app');
INSERT INTO "public"."app_protocol" VALUES (335, '今日头条app');
INSERT INTO "public"."app_protocol" VALUES (336, '华商头条app');
INSERT INTO "public"."app_protocol" VALUES (337, '天涯社区app');
INSERT INTO "public"."app_protocol" VALUES (338, '微信app');
INSERT INTO "public"."app_protocol" VALUES (339, '新浪微博app');
INSERT INTO "public"."app_protocol" VALUES (340, '携程app');
INSERT INTO "public"."app_protocol" VALUES (341, '百度地图app');
INSERT INTO "public"."app_protocol" VALUES (342, '知乎app');
INSERT INTO "public"."app_protocol" VALUES (343, '糗事百科app');
INSERT INTO "public"."app_protocol" VALUES (344, '经济观察app');
INSERT INTO "public"."app_protocol" VALUES (345, '腾讯视频app');
INSERT INTO "public"."app_protocol" VALUES (346, '艺龙旅行app');
INSERT INTO "public"."app_protocol" VALUES (347, '菜鸟裹裹app');
INSERT INTO "public"."app_protocol" VALUES (348, '豆瓣app');
INSERT INTO "public"."app_protocol" VALUES (349, '好看视频');
INSERT INTO "public"."app_protocol" VALUES (350, 'YY直播');
INSERT INTO "public"."app_protocol" VALUES (351, '百搜视频');
INSERT INTO "public"."app_protocol" VALUES (352, '全民小视频');

-- ----------------------------
-- Primary Key structure for table app_protocol
-- ----------------------------
ALTER TABLE "public"."app_protocol" ADD CONSTRAINT "app_protocol_pkey" PRIMARY KEY ("app_id");
