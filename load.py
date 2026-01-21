import hashlib
import os
import time
from datetime import datetime
from flask import Blueprint, request

load_bp = Blueprint('load', __name__, url_prefix='/load')

@load_bp.route('', methods=['POST'])
def handle_load():
    pod_name = os.getenv('POD_NAME', 'unknown-pod')    
    duration = max(1, min(int(request.args.get('duration', 10)), 60))
    intensity = max(1, min(int(request.args.get('intensity', 5)), 100))
    print(f'[{pod_name}] Load Test - Duration: {duration} Intensity: {intensity}')

    start_time = time.time()
    count = 0
    while time.time() - start_time < duration:
        for _ in range(intensity * 10000):
            hashlib.sha256(f'{count}-{time.time}'.encode()).hexdigest()
            count+=1

    print(f'[{pod_name}] Load Test - Complete')     
    return {'duration': duration, 'intensity': intensity, 'name': pod_name}, 200
