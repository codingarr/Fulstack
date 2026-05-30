from flask_cors import CORS
from flask import Flask, request, jsonify
import time

app=Flask(__name__)
CORS(app)

rate_limit={}
alerts=[]

MAX_REQUESTS=3
WINDOW=10
THRESHOLD=100

@app.route('/api/telemetry', methods=['POST'])
def telemetry():
    data=request.json

    device_id=data.get('device_id')
    metric=data.get('metric')
    value=data.get('value')

    current_time=time.time()

    if device_id not in rate_limit:
        rate_limit[device_id]=[]
    rate_limit[device_id]=[t for t in rate_limit[device_id] if current_time-t<WINDOW]
    if len(rate_limit[device_id])>=MAX_REQUESTS:
        return jsonify({'error':'Too many requests'}), 429
    rate_limit[device_id].append(current_time)
    if metric=='temperature' and value>THRESHOLD:
        alerts.append({'device_id':device_id, 'metric':metric, 'value':value})
    return jsonify({"message":"Telemetry received"}), 200

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts)
@app.route('/api/alerts/<int:index>', methods=['DELETE'])
def delete_alert(index):
    if 0 <= index < len(alerts):
        alerts.pop(index)
        return jsonify({"message":"Alert deleted"}), 200
    return jsonify({'error':'Alert not found'}), 404
if __name__=='__main__':
    app.run(debug=True)
