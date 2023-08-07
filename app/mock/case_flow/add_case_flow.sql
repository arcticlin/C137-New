/*
   1: 创建项目
   2: 创建一个目录
   3. 创建用例
   4. 创建环境
   5. 创建SQL配置
   5. 环境添加前置, 等待500ms
   6. 环境添加断言, status_code = 200
   7. 用例添加前置, 等待500ms
   8. 用例添加后置, SQL查询是否存在
   9. 用例添加提取参数, 提取返回值中的task_id
*/
-- 创建项目
INSERT INTO project (project_name, public, create_user, update_user, deleted_at) VALUES ('SQL项目', true, 1, 1, 0);
-- 设置项目ID
SELECT project_id INTO @t_project_id FROM project WHERE project_name = 'SQL项目';
-- member表设置成员
INSERT INTO project_member (project_id, user_id, role, create_user, update_user, deleted_at) VALUES (@t_project_id, 1, 'CREATOR', 1, 1, 0);
-- 创建项目目录
INSERT INTO directory (project_id, name, create_user, update_user, deleted_at) VALUES (@t_project_id, '飞项根目录', 1, 1, 0);
-- 设置目录ID
SELECT directory_id INTO @t_directory_id FROM directory WHERE name='飞项根目录' AND project_id=@t_project_id;
-- 创建测试用例
INSERT INTO api_case (name, request_type, url, method, body_type, directory_id, tag, status, priority, case_type, create_user, update_user, deleted_at) VALUES ('查询task_id', 1, '/flyele/task/{task_id}/ignore_auth', 'GET', 0, @t_directory_id, '事项类', 1, 'P0', 1, 1, 1, 0);
-- 设置CaseID
SELECT case_id INTO @t_case_id FROM api_case WHERE name='查询task_id' and method = 'GET';
-- 创建环境
INSERT INTO env (name, url, create_user, update_user, deleted_at) VALUES ('测试环境', 'https://api-test.flyele.vip', 1, 1, 0);
-- 创建SQL配置
INSERT INTO sql_model (name, host, port, db_user, db_password, db_name, sql_type, create_user, update_user, deleted_at) VALUES ('飞项测试', '192.168.1.30', 3306, 'feixiang_develop', 'Zic1YBXPEssAB62VrK5u', 'feixiang', 1, 1, 1, 0);
-- 查询SQL_ID
SELECT sql_id INTO @t_sql_id FROM sql_model WHERE name='飞项测试';
-- 查询环境变量
SELECT env_id INTO @t_env_id FROM env WHERE name='测试环境';
-- 设置环境前置
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, env_id, run_delay, create_user, update_user, deleted_at) VALUES (1, '前置-等待250ms-1', true, 1, 4, @t_env_id, 250, 1, 1, 0);
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, env_id, run_delay, create_user, update_user, deleted_at) VALUES (1, '前置-等待250ms-2', true, 2, 4, @t_env_id, 250, 1, 1, 0);
-- 设置环境断言
INSERT INTO common_assert (name, enable, env_id, assert_from, assert_type, assert_value, create_user, update_user, deleted_at) VALUES ('状态码=200', true, @t_env_id, 3, 1, 200, 1, 1, 0);
-- 设置用例前置
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, case_id, run_delay, create_user, update_user, deleted_at) VALUES (1, '前置-等待250ms-1', true, 1, 4, @t_case_id, 250, 1, 1, 0);
-- 设置用例后置 - 执行sql语句
INSERT INTO common_suffix (suffix_type, name, enable, sort, execute_type, case_id, sql_id, run_command, create_user, update_user, deleted_at) VALUES (2, '后置-查询数据是否存在', true, 1, 2, @t_case_id, @t_sql_id, 'SELECT task_id FROM fx_task WHERE id = 808276787200071',1, 1, 0);
-- 添加提取参数
INSERT INTO common_extract (name, description, enable, case_id, extract_from, extract_type, extract_exp, extract_out_name, create_user, update_user, deleted_at) VALUES ('提取taskName', '获取事项名称', true, @t_case_id, 2, 1, '$.data.name', 'task_name', 1, 1 ,0);
