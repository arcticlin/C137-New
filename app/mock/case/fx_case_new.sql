INSERT INTO `c137`.`project` (`project_name`, `project_desc`, `public`, `project_avatar`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('飞项', 'no', 1, '', 1, 1, '2023-10-31 23:12:59', '2023-10-31 23:12:59', 0);
SELECT project_id INTO @t_project_id FROM project WHERE project_name = '飞项';
INSERT INTO `c137`.`project_member` (`project_id`, `user_id`, `role`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES (@t_project_id, 1, 3, 1, 1, '2023-10-31 23:12:59', '2023-10-31 23:12:59', 0);
INSERT INTO `c137`.`directory` (`project_id`, `name`, `parent_id`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES (@t_project_id, '根目录', NULL, 1, NULL, '2023-10-31 23:14:20', '2023-10-31 23:14:20', 0);
SELECT directory_id INTO @root_directory_id FROM directory WHERE name='根目录' AND project_id=@t_project_id;
INSERT INTO `c137`.`directory` (`project_id`, `name`, `parent_id`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES (@t_project_id, 'flyele', @root_directory_id, 1, NULL, '2023-10-31 23:14:20', '2023-10-31 23:14:20', 0);
SELECT directory_id INTO @flyele_directory_id FROM directory WHERE name='flyele' AND project_id=@t_project_id;
INSERT INTO `c137`.`envs` (`name`, `domain`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('飞项测试环境', 'https://api-test.flyele.vip', 1, 1, '2023-09-06 15:08:29', '2023-09-06 15:08:29', 0);
SELECT env_id INTO @env_id FROM envs WHERE name='飞项测试环境';
INSERT INTO `c137`.`api_case` (`name`, `request_type`, `url`, `temp_domain`, `method`, `body_type`, `body`, `directory_id`, `tag`, `status`, `priority`, `case_type`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('登录前置用例', 1, '/userc/v2/auth/phonelogin/code', NULL, 'PUT', 1, '{\"telephone\": \"${account1}\", \"verify_code\": \"123456\", \"channel_origin\": \"AppStore\", \"user_origin_type\": \"主动加入\", \"success_platform_type\": \"mobile\", \"device\": {\"client_version\": \"2.7.0\", \"device_id\": \"${device_uuid}\", \"device_name\": \"iPhone\", \"os\": \"iOS\", \"platform\": \"mobile\"}}', 3, '登录', 1, 'P0', 2, 1, 1, '2023-10-31 14:44:11', '2023-10-31 14:44:11', 0);
SELECT case_id INTO @login_case_id FROM api_case WHERE name='登录前置用例';
INSERT INTO `c137`.`api_case` ( `name`, `request_type`, `url`, `temp_domain`, `method`, `body_type`, `body`, `directory_id`, `tag`, `status`, `priority`, `case_type`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('普通测试', 1, 'userc/v1/system/now', NULL, 'GET', 0, NULL, 3, NULL, 1, 'P1', 1, 1, 1, '2023-10-31 23:29:15', '2023-10-31 23:29:15', 0);
INSERT INTO `c137`.`api_headers` (`key`, `value`, `value_type`, `enable`, `comment`, `case_id`, `env_id`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('authorization', '${token_1}', 1, 1, NULL, NULL, @env_id, 1, 1, '2023-10-31 14:53:35', '2023-10-31 14:53:35', 0);
INSERT INTO `c137`.`script` (`name`, `description`, `tag`, `var_key`, `var_script`, `public`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('uuid设备', NULL, '标识符', 'device_uuid', 'import uuid\ndevice_uuid = str(uuid.uuid4())', 1, 1, 1, '2023-10-31 14:50:15', '2023-10-31 14:50:15', 0);
SELECT script_id INTO @script_id FROM script WHERE name='uuid设备';
INSERT INTO `c137`.`common_suffix` (`suffix_type`, `name`, `description`, `enable`, `sort`, `execute_type`, `case_id`, `env_id`, `run_each_case`, `script_id`, `sql_id`, `redis_id`, `run_case_id`, `run_delay`, `fetch_one`, `run_command`, `run_out_name`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES (1, '获取设备device_id', NULL, 1, 1, 1, NULL, 1, 0, @script_id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 1, '2023-10-31 14:52:16', '2023-10-31 14:52:16', 0);
INSERT INTO `c137`.`common_suffix` (`suffix_type`, `name`, `description`, `enable`, `sort`, `execute_type`, `case_id`, `env_id`, `run_each_case`, `script_id`, `sql_id`, `redis_id`, `run_case_id`, `run_delay`, `fetch_one`, `run_command`, `run_out_name`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES (1, '登录获取Token', NULL, 1, 2, 6, NULL, 1, NULL, NULL, NULL, NULL, @login_case_id, NULL, NULL, NULL, '', 1, 1, '2023-10-31 16:32:26', '2023-10-31 16:32:26', 0);
INSERT INTO `c137`.`common_extract` (`name`, `description`, `enable`, `case_id`, `extract_from`, `extract_type`, `extract_exp`, `extract_out_name`, `extract_index`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`, `extract_to`) VALUES ('提取token', NULL, 1, @login_case_id, 2, 1, '$.data.Token', 'token1', 0, 1, 1, '2023-10-31 16:35:17', '2023-10-31 16:35:17', 0, 1);
INSERT INTO `c137`.`common_extract` (`name`, `description`, `enable`, `case_id`, `extract_from`, `extract_type`, `extract_exp`, `extract_out_name`, `extract_index`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`, `extract_to`) VALUES ('提取user_id', NULL, 1, @login_case_id, 2, 1, '$.data.user_id', 'user1_id', 0, 1, 1, '2023-10-31 16:34:37', '2023-10-31 16:34:39', 0, 1);
INSERT INTO `c137`.`common_assert` (`name`, `enable`, `case_id`, `env_id`, `assert_from`, `assert_type`, `assert_exp`, `assert_value`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('响应码200', 1, NULL, @env_id, 3, 1, NULL, '400', 2, 1, '2023-09-11 11:45:19', '2023-10-26 14:57:58', 0);