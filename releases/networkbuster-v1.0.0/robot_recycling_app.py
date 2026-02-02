"""
Robot Recycling Management System
Main application entry point
"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'networkbuster-robot-recycling-2026'

# Data storage
ROBOTS_FILE = 'data/robots.json'
RECYCLING_TASKS_FILE = 'data/recycling_tasks.json'
PARTS_INVENTORY_FILE = 'data/parts_inventory.json'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

def load_data(filename):
    """Load data from JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('robot_recycling.html')

@app.route('/api/robots', methods=['GET', 'POST'])
def robots():
    """Manage robots"""
    if request.method == 'POST':
        robots_data = load_data(ROBOTS_FILE)
        new_robot = request.json
        new_robot['id'] = len(robots_data) + 1
        new_robot['registered_date'] = datetime.now().isoformat()
        new_robot['status'] = 'active'
        robots_data.append(new_robot)
        save_data(ROBOTS_FILE, robots_data)
        return jsonify({'success': True, 'robot': new_robot})
    
    robots_data = load_data(ROBOTS_FILE)
    return jsonify(robots_data)

@app.route('/api/robots/<int:robot_id>', methods=['GET', 'PUT', 'DELETE'])
def robot_detail(robot_id):
    """Get, update, or delete a specific robot"""
    robots_data = load_data(ROBOTS_FILE)
    robot = next((r for r in robots_data if r['id'] == robot_id), None)
    
    if request.method == 'GET':
        return jsonify(robot) if robot else ('Not found', 404)
    
    if request.method == 'PUT':
        if robot:
            robot.update(request.json)
            save_data(ROBOTS_FILE, robots_data)
            return jsonify({'success': True, 'robot': robot})
        return ('Not found', 404)
    
    if request.method == 'DELETE':
        if robot:
            robots_data.remove(robot)
            save_data(ROBOTS_FILE, robots_data)
            return jsonify({'success': True})
        return ('Not found', 404)

@app.route('/api/recycling-tasks', methods=['GET', 'POST'])
def recycling_tasks():
    """Manage recycling tasks"""
    if request.method == 'POST':
        tasks_data = load_data(RECYCLING_TASKS_FILE)
        new_task = request.json
        new_task['id'] = len(tasks_data) + 1
        new_task['created_date'] = datetime.now().isoformat()
        new_task['status'] = 'pending'
        tasks_data.append(new_task)
        save_data(RECYCLING_TASKS_FILE, tasks_data)
        return jsonify({'success': True, 'task': new_task})
    
    tasks_data = load_data(RECYCLING_TASKS_FILE)
    return jsonify(tasks_data)

@app.route('/api/recycling-tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update recycling task status"""
    tasks_data = load_data(RECYCLING_TASKS_FILE)
    task = next((t for t in tasks_data if t['id'] == task_id), None)
    
    if task:
        task.update(request.json)
        task['updated_date'] = datetime.now().isoformat()
        save_data(RECYCLING_TASKS_FILE, tasks_data)
        return jsonify({'success': True, 'task': task})
    return ('Not found', 404)

@app.route('/api/parts-inventory', methods=['GET', 'POST'])
def parts_inventory():
    """Manage parts inventory"""
    if request.method == 'POST':
        parts_data = load_data(PARTS_INVENTORY_FILE)
        new_part = request.json
        new_part['id'] = len(parts_data) + 1
        new_part['added_date'] = datetime.now().isoformat()
        parts_data.append(new_part)
        save_data(PARTS_INVENTORY_FILE, parts_data)
        return jsonify({'success': True, 'part': new_part})
    
    parts_data = load_data(PARTS_INVENTORY_FILE)
    return jsonify(parts_data)

@app.route('/api/dashboard/stats')
def dashboard_stats():
    """Get dashboard statistics"""
    robots_data = load_data(ROBOTS_FILE)
    tasks_data = load_data(RECYCLING_TASKS_FILE)
    parts_data = load_data(PARTS_INVENTORY_FILE)
    
    stats = {
        'total_robots': len(robots_data),
        'active_robots': len([r for r in robots_data if r.get('status') == 'active']),
        'recycling_robots': len([r for r in robots_data if r.get('status') == 'recycling']),
        'recycled_robots': len([r for r in robots_data if r.get('status') == 'recycled']),
        'pending_tasks': len([t for t in tasks_data if t.get('status') == 'pending']),
        'in_progress_tasks': len([t for t in tasks_data if t.get('status') == 'in_progress']),
        'completed_tasks': len([t for t in tasks_data if t.get('status') == 'completed']),
        'total_parts': sum(p.get('quantity', 0) for p in parts_data),
        'parts_types': len(parts_data)
    }
    
    return jsonify(stats)

if __name__ == '__main__':
    print("🤖 Starting Robot Recycling Management System...")
    print("✅ Server running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
