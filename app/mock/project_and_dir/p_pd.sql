INSERT INTO project (project_name, project_desc, public, project_avatar, create_user, update_user) VALUES ('这是项目名称', '这是项目描述', true, '', 1, 1);
INSERT INTO directory (name, project_id, parent_id, create_user, update_user) VALUES ('这是目录名称', 1, null, 1, 1);