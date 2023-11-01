INSERT INTO `C137`.`script` (`name`, `description`, `tag`, `var_key`, `var_script`, `public`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('今天0点', NULL, '时间', 'today_begin', 'from datetime import datetime\ntoday_begin = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())', 1, 1, 1, '2023-11-01 10:40:17', '2023-11-01 10:40:17', 0);
INSERT INTO `C137`.`script` (`name`, `description`, `tag`, `var_key`, `var_script`, `public`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('今天23点', NULL, '时间', 'today_end', 'from datetime import datetime\ntoday_end = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())', 1, 1, 1, '2023-11-01 10:41:30', '2023-11-01 10:41:30', 0);
INSERT INTO `C137`.`script` (`name`, `description`, `tag`, `var_key`, `var_script`, `public`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('当前时间事项名', NULL, '时间', 'task_title_now', 'from datetime import datetime\ncurrent_datetime = datetime.now()\nformatted_datetime = current_datetime.strftime("%m-%d-%H-%M-%S")\ntask_title_now = f"事项-{formatted_datetime}"', 1, 1, 1, '2023-11-01 10:41:30', '2023-11-01 10:41:30', 0);

INSERT INTO `c137`.`api_case` (`name`, `request_type`, `url`, `temp_domain`, `method`, `body_type`, `body`, `directory_id`, `tag`, `status`, `priority`, `case_type`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('创建事项', 1, '/flyele/v2/task', NULL, 'POST', 1, '{"title": "${task_title_now}", "files": [], "is_dispatch": 0, "matter_type": 10701, "priority_level": 1, "repeat_type": 0, "repeat_config": {}, "operate_type": 2, "takers": [], "start_time_full_day": 2, "start_time": "${today_begin}", "end_time": "${today_end}", "end_time_full_day": 2, "remind_at": {"start_remind": ["${today_begin}"], "max_alone_total": 0}, "widget": {"execute_addr": false, "remind": true, "time": true, "repeat": true}, "_tagIds": [], "_tagArr": [], "_create_type": "详细创建"}', 3, '事项', 1, 'P0', 2, 1, 1, '2023-10-31 14:44:11', '2023-10-31 14:44:11', 0);
INSERT INTO `c137`.`api_case` (`name`, `request_type`, `url`, `temp_domain`, `method`, `body_type`, `body`, `directory_id`, `tag`, `status`, `priority`, `case_type`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('查询事项', 1, '/flyele/v2/task/{task_id}', NULL, 'GET', 0, '', 3, '事项', 1, 'P0', 1, 1, 1, '2023-10-31 14:44:11', '2023-10-31 14:44:11', 0);
SELECT case_id INTO @check_task_id FROM api_case WHERE name='查询事项';
INSERT INTO `C137`.`common_extract` (`name`, `description`, `enable`, `case_id`, `extract_from`, `extract_type`, `extract_exp`, `extract_out_name`, `extract_index`, `extract_to`, `create_user`, `update_user`, `created_at`, `updated_at`, `deleted_at`) VALUES ('提取task_id', NULL, 1, @check_task_id, 2, 1, '$.data.task_id', 'task_id', 0, 2, 1, 1, '2023-10-31 16:34:37', '2023-10-31 16:34:39', 0);
INSERT INTO `C137`.`api_path` (`key`, value, types, enable, comment, case_id, env_id, create_user, update_user ,deleted_at) VALUES ('task_id', '${task_id}', 1, 1, '', @check_task_id, null, 1, 1, 0)


