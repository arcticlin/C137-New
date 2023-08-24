INSERT INTO `api_case` (name, request_type, url, method, body_type, body, directory_id, tag, status, priority, case_type, create_user, update_user, deleted_at) VALUES ('测试用例1', 1, 'flyele/v2/task', 'POST', 1, '{\'task_id\': 1}', 1, '测试', 1, 'P0', 1, 1, 1,  '0');
INSERT INTO `api_path` (`key`, value, types, enable, comment, case_id, create_user, update_user, deleted_at) VALUES ('page_size', '1', 1, 1, '任务id', 1, 1, 1, '0');
INSERT INTO `api_path` (`key`, value, types, enable, comment, case_id, create_user, update_user, deleted_at) VALUES ('page_number', '2', 1, 1, '任务id', 1, 1, 1, '0');
INSERT INTO `api_path` (`key`, value, types, enable, comment, case_id, create_user, update_user, deleted_at) VALUES ('task_id', '5959595', 2, 1, '任务id', 1, 1, 1, '0');
INSERT INTO `api_headers` (`key`, value, value_type, enable, comment, case_id, create_user, update_user, deleted_at) VALUES ('token', 'ejsjsjsj_w', 1, 1, '任务id', 1, 1, 1, '0');
