from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from datetime import datetime

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}
        self.user_info: dict[WebSocket, dict] = {}
    
    async def connect(self, websocket: WebSocket, channel_id: int, user_data: dict):
        await websocket.accept()
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = []
        self.active_connections[channel_id].append(websocket)
        self.user_info[websocket] = user_data
        
        # Notify others user joined
        await self.broadcast(channel_id, json.dumps({
            "type": "user_joined",
            "user": user_data["name"],
            "timestamp": datetime.now().isoformat()
        }), exclude=websocket)
    
    def disconnect(self, websocket: WebSocket, channel_id: int):
        if channel_id in self.active_connections:
            if websocket in self.active_connections[channel_id]:
                self.active_connections[channel_id].remove(websocket)
        if websocket in self.user_info:
            del self.user_info[websocket]
    
    async def broadcast(self, channel_id: int, message: str, exclude: WebSocket = None):
        if channel_id in self.active_connections:
            for connection in self.active_connections[channel_id]:
                if connection != exclude:
                    try:
                        await connection.send_text(message)
                    except:
                        pass
    
    def get_online_users(self, channel_id: int) -> list:
        if channel_id not in self.active_connections:
            return []
        return [self.user_info.get(ws, {}) for ws in self.active_connections[channel_id]]

manager = ConnectionManager()

@router.websocket("/ws/channels/{channel_id}")
async def websocket_endpoint(websocket: WebSocket, channel_id: int, user_id: int = 0, user_name: str = "Anonymous"):
    user_data = {"id": user_id, "name": user_name}
    await manager.connect(websocket, channel_id, user_data)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Add server timestamp
            message_data["server_timestamp"] = datetime.now().isoformat()
            message_data["channel_id"] = channel_id
            
            # Broadcast to all users in channel
            await manager.broadcast(channel_id, json.dumps(message_data))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, channel_id)
        # Notify others user left
        await manager.broadcast(channel_id, json.dumps({
            "type": "user_left",
            "user": user_data["name"],
            "timestamp": datetime.now().isoformat()
        }))
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, channel_id)
