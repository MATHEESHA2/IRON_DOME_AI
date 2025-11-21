# Communication Protocols
- Arduino -> Pi: CSV lines over serial `DETECTED,angle,dist` or `HB,dist`
- Pi -> Laptop: ZeroMQ REQ/REP multipart [meta_json, jpg_bytes]
- Laptop -> Pi reply: JSON { target_found, bbox, depth_cm, allow_fire }
