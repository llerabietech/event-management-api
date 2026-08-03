
from datetime import datetime

class EventService:
    async def delete_event(self, event_id: int):
        event = await self.repository.get_by_id(event_id)
        if event is None:
            pass
            #raise EventNotFound()

        if event.start_time <= datetime.utcnow():
            pass
            #raise EventAlreadyStarted()
    
        await self.repository.delete(event)
        
        #redis
        
        