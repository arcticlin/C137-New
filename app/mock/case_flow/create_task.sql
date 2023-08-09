/*
   造一个创建事项和查询事项的接口数据
   1. 添加脚本变量, today_start = 今天0点
   2. 添加脚本变量, today_end = 今天23点59分59秒
   3. 添加脚本变量, remind_at_nine = 今天9点
   4. 添加脚本变量, random_task_name
   5. 创建用例 - 创建事项
   6. 添加headers token + content_type,
   7. 用例添加断言, status_code = 200, 响应提取code = 0
   8. 提取响应值,task_id
   9. 创建用例 - 查询事项
   10. 添加headers token + content_type,
   11. 添加断言, status_code = 200, 响应提取code = 0
*/

INSERT INTO script (name, tag, var_key, var_script, public, create_user, update_user, deleted_at) VALUES ('当天全天开始时间', '时间', 'today_start', 'today_start = int(datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).timestamp())',  1, 1, 1, 0);
INSERT INTO script (name, tag, var_key, var_script, public, create_user, update_user, deleted_at) VALUES ('当天全天截止时间', '时间', 'today_end', 'today_end = int(datetime.now().replace(hour=23, minute=59, second=59, microsecond=0).timestamp())',  1, 1, 1, 0);
INSERT INTO script (name, tag, var_key, var_script, public, create_user, update_user, deleted_at) VALUES ('当天9点', '时间', 'remind_at_nine', 'remind_at_nine = int(datetime.now().replace(hour=9, minute=0, second=0, microsecond=0).timestamp())',  1, 1, 1, 0);
INSERT INTO script (name, tag, var_key, var_script, public, create_user, update_user, deleted_at) VALUES ('随机事项名', '时间', 'random_task_name', 'random_task_name = f"API_NAME{int(datetime.now().timestamp())}"',  1, 1, 1, 0);
SELECT script_id INTO @t_script_id_1 FROM script WHERE name = '当天全天开始时间';
SELECT script_id INTO @t_script_id_2 FROM script WHERE name = '当天全天截止时间';
SELECT script_id INTO @t_script_id_3 FROM script WHERE name = '当天9点';
SELECT script_id INTO @t_script_id_4 FROM script WHERE name = '随机事项名';
INSERT INTO api_case (name, request_type, url, method, body_type, body, directory_id, tag, status, priority, case_type, create_user, update_user, deleted_at) VALUES ('创建全天事项 ', 1, '/flyele/v2/task', 'POST', 1, '{"title": "${random_task_name}", "files": [], "is_dispatch": 0, "matter_type": 10701, "priority_level": 1, "repeat_type": 0, "repeat_config": {}, "operate_type": 1, "takers": [], "start_time_full_day": 2, "start_time": "${today_start}", "end_time": "${today_end}", "end_time_full_day": 2, "remind_at": {"start_remind": ["${remind_at_nine}"], "max_alone_total": 0}, "widget": {"execute_addr": false, "remind": true, "time": true, "repeat": true}, "_tagIds": [], "_tagArr": [], "_create_type": "详细创建"}', 11, '事项类', 1, 'P0', 1, 1, 1, 0);
SELECT case_id INTO @t_case_id FROM api_case WHERE name='创建全天事项' and method = 'POST';
INSERT INTO api_headers (`key`, value, value_type, enable, comment, case_id, create_user, update_user, deleted_at) VALUES ('authorization', '', 1, 1, 'Token', @t_case_id, 1, 1, 0);
INSERT INTO api_headers (`key`, value, value_type, enable, comment, case_id, create_user, update_user, deleted_at) VALUES ('content-type', 'application/json', 1, 1, '请求格式', @t_case_id, 1, 1, 0);
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, case_id, script_id, create_user, update_user, deleted_at) VALUES (1, '设置开始时间变量', true, 1, 1, @t_case_id, @t_script_id_1, 1, 1, 0);
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, case_id, script_id, create_user, update_user, deleted_at) VALUES (1, '设置截止时间变量', true, 2, 1, @t_case_id, @t_script_id_2, 1, 1, 0);
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, case_id, script_id, create_user, update_user, deleted_at) VALUES (1, '设置提醒时间变量', true, 3, 1, @t_case_id, @t_script_id_3, 1, 1, 0);
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, case_id, script_id, create_user, update_user, deleted_at) VALUES (1, '设置随机事项名', true, 4, 1, @t_case_id, @t_script_id_4, 1, 1, 0);
INSERT INTO common_assert (name, enable, env_id, assert_from, assert_type, assert_value, create_user, update_user, deleted_at) VALUES ('全局断言状态码', 1, 3, 4, 1, 200, 1,  1,  0);
INSERT INTO common_extract (name, enable, case_id, extract_from, extract_type, extract_exp, extract_out_name, create_user, update_user, deleted_at) VALUES ('提取task_id', 1, @t_case_id, 2, 1, '$.data.task_id', 'task_id', 1, 1, 0);



