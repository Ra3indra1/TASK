from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    response = [{'id': proj.id, 'name': proj.name, 'description': proj.description} for proj in projects]
    return jsonify(response)

@app.route('/projects', methods=['POST'])
def add_project():
    data = request.get_json()
    if not data.get('name') or not data.get('description'):
        return jsonify({'error': 'Both name and description are required!'}), 400
    new_project = Project(name=data['name'], description=data['description'])
    db.session.add(new_project)
    db.session.commit()
    return jsonify({'message': 'Project added successfully!', 'project': {'id': new_project.id, 'name': new_project.name, 'description': new_project.description}}), 201

@app.route('/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found!'}), 404
    data = request.get_json()
    project.name = data.get('name', project.name)
    project.description = data.get('description', project.description)
    db.session.commit()
    return jsonify({'message': 'Project updated successfully!', 'project': {'id': project.id, 'name': project.name, 'description': project.description}})

@app.route('/projects/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return jsonify({'error': 'Project not found!'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)