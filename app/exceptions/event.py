from app.exceptions import ConflictError, NotFoundError


class EventNotFoundError(NotFoundError):
    error_code = "EVENT_NOT_FOUND"

    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event {event_id} not found")


class EventAlreadyExistsError(ConflictError):
    error_code = "EVENT_ALREADY_EXISTS"

    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event {event_id} already exists")


class EventAlreadyStartsError(ConflictError):
    error_code = "EVENT_ALREADY_STARTS"

    def __init__(self, event_id: int):
        self.event_id = event_id
        super().__init__(f"Event {event_id} already starts")
