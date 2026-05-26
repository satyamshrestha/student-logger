from db.redis import redis_client

def invalidate_student_cache():
    for key in redis_client.scan_iter("students:*"):
        redis_client.delete(key)