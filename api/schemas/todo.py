def taskEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "title":item["name"],
        "status":item["status"]
        
    }

def tasksEntity(entity) -> list:
    return [taskEntity(item) for item in entity]