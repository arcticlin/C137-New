SELECT project_id INTO @t_project_id FROM project WHERE project_name = 'SQL项目';
SELECT id INTO @t_member_id FROM project_member WHERE project_id = @t_project_id;
SELECT directory_id INTO @t_directory_id FROM directory WHERE name='根目录' AND project_id=@t_project_id;
SELECT case_id INTO @t_case_id FROM api_case WHERE name='查询task_id' and method = 'GET';
SELECT sql_id INTO @t_sql_id FROM sql_model WHERE name='飞项测试';
SELECT env_id INTO @t_env_id FROM env WHERE name='测试环境';
SELECT suffix_id INTO @t_suffix_id1 FROM common_suffix WHERE env_id=@t_env_id AND sort=1;
SELECT suffix_id INTO @t_suffix_id2 FROM common_suffix WHERE env_id=@t_env_id AND sort=2;
SELECT assert_id INTO @t_assert_id FROM common_assert WHERE env_id=@t_env_id;
SELECT suffix_id INTO @t_suffix_id3 FROM common_suffix WHERE case_id=@t_case_id AND sort=1 AND execute_type=1;
SELECT suffix_id INTO @t_suffix_id4 FROM common_suffix WHERE case_id=@t_case_id AND sort=1 AND execute_type=2;
SELECT extract_id INTO @t_extract_id FROM common_extract WHERE case_id=@t_case_id;


DELETE FROM project_member where id=@t_member_id;
DELETE FROM project where project_id=@t_project_id;
DELETE FROM directory where directory_id=@t_directory_id;
DELETE FROM api_case where case_id=@case_id;
DELETE FROM sql_model where sql_id=@t_sql_id;
DELETE FROM env where env_id=@t_env_id;
DELETE FROM common_suffix where suffix_id=@t_suffix_id1;
DELETE FROM common_suffix where suffix_id=@t_suffix_id2;
DELETE FROM common_suffix where suffix_id=@t_suffix_id3;
DELETE FROM common_suffix where suffix_id=@t_suffix_id4;
DELETE FROM common_assert where assert_id=@t_assert_id;
DELETE FROM common_extract where extract_id=@extract_id;