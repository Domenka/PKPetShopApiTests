STORE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "integer"
        },
        "petId": {
            "type": "integer"},
        "quantity": {
            "type": "integer"},
        "shipDate" : {
            "type": "string"},
        "status" : {
            "type": "string",
        "enum": ["approved", "placed", "delivered"]},
        "complete" : {
            "type": "boolean"},
    },
    "required": ["status"], #валидация обязательности действительно есть только на этот параметр, проверила в сваггере
    "additionalProperties": False
}
