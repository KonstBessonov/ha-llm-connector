from homeassistant.helpers.storage import Store
from typing import Dict, List

class ChatManager:
    def __init__(self, store: Store):
        self.store = store
        self.history: Dict[str, List[dict]] = {}

    async def async_load(self):
        data = await self.store.async_load()
        if data is not None:
            self.history = data

    async def async_save(self):
        await self.store.async_save(self.history)

    def add_message(self, user_id: str, role: str, content: str):
        if user_id not in self.history:
            self.history[user_id] = []
        self.history[user_id].append({"role": role, "content": content})

    def get_history(self, user_id: str) -> List[dict]:
        return self.history.get(user_id, [])

    async def reset_history(self, user_id: str):
        self.history.pop(user_id, None)
        await self.async_save()