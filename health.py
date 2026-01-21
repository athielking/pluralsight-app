import os
import time
from datetime import datetime
from flask import Blueprint, request

health_bp = Blueprint('health', __name__, url_prefix='/health')

start_time = time.time()
startup_delay = int(os.getenv('STARTUP_DELAY_SECONDS', '30'))

@health_bp.route('/startup', methods=['GET'])
def handle_startup():
    elapsed = time.time() - start_time
    pod_name = os.getenv('POD_NAME', 'unknown-pod')

    if elapsed < startup_delay:
        remaining = startup_delay - elapsed
        print( f'[{pod_name}] Startup Probe - Not Ready: {remaining}s remaining')
        return {'started': False, 'name': pod_name, 'remaining': remaining}, 503
    else:
        print( f'[{pod_name}] Startup Probe - Ready')
        return {'started': True, 'name': pod_name}, 200

live = True
@health_bp.route('/liveness', methods=['GET'])
def handle_liveness():
    pod_name = os.getenv('POD_NAME', 'unknown-pod')
    print(f'[{pod_name}] Liveness Check - Live: {live}')

    if live:
        return {'live': True, 'name': pod_name}, 200
    else:
        return {'live': False, 'name': pod_name}, 503

@health_bp.route('/liveness', methods=['POST'])
def handle_set_liveness():
    global live

    pod_name = os.getenv('POD_NAME', 'unknown-pod')
    value = request.args.get('value')
    print(f"Set Liveness {value}")

    if value == 'False' or value == 'false':
        live = False            
    else:
        return 'value not set', 400
        
    return {'live': live, 'name': pod_name}, 201
    
ready = True
@health_bp.route('/ready', methods=['GET'])
def handle_readiness():
    pod_name = os.getenv('POD_NAME', 'unknown-pod')
    print(f'[{pod_name}] Readiness Check - Ready: {ready}')

    if ready:
        return {'ready': True, 'name': pod_name}, 200
    else:
        return {'ready': False, 'name': pod_name}, 503

@health_bp.route('/ready', methods=['POST'])
def handle_set_readiness():
    global ready
    pod_name = os.getenv('POD_NAME', 'unknown-pod')
    value = request.args.get('value')
    print(f"Set Readiness {value}")

    if value == 'False' or value == 'false':
        ready = False            
    else:
        return 'value not set', 400
    
    return {'ready': ready, 'name': pod_name}, 201
