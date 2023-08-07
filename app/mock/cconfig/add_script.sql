INSERT INTO script (name, description, tag, var_key, var_script, public, create_user, update_user, deleted_at) VALUES ("当前时间戳", "获取当前时间戳并返回整数", "时间", "current_time", "from datetime import datetime/ncurrent_time = int(datetime.now().timestamp())", 1, 1, 1, 0);
INSERT INTO script (name, description, tag, var_key, var_script, public, create_user, update_user, deleted_at) VALUES ("自动会议时间","获取当前时间未来5分钟-15分钟时间","时间","meet_time", "from datetime import datetime, timedelta\ndef future_time():\n    time_interval = [i * 5 for i in range(0, 13)]\n    now_time = datetime.now().replace(second=0, microsecond=0)\n    for i in time_interval:\n        if now_time.minute <= i:\n            now_time = now_time + timedelta(minutes=i - now_time.minute) + timedelta(minutes=15)\n            next_time = now_time + timedelta(minutes=30)\n            return int(now_time.timestamp()), int(next_time.timestamp())\nmeet_time=future_time()", 1, 1, 1, 0);