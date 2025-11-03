"""WebSocket application for handling WebSocket connections."""


async def websocket_application(_scope: dict, receive: object, send: object) -> None:
    """Handle WebSocket connections with ping/pong functionality."""
    while True:
        event = await receive()

        if event["type"] == "websocket.connect":
            await send({"type": "websocket.accept"})

        if event["type"] == "websocket.disconnect":
            break

        if event["type"] == "websocket.receive" and event["text"] == "ping":
            await send({"type": "websocket.send", "text": "pong!"})
