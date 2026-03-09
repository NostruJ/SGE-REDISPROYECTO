from flask import Flask, render_template_string, request, redirect, url_for
import redis
import uuid

app = Flask(__name__)

# Configuración de Redis
db = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Plantilla HTML con Apartado Desplegable (Details/Summary)
HTML_LAYOUT = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>SGE - Sistema de Gestión Estudiantil</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; margin: 40px; background-color: #f0f2f5; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h1 { color: #1a73e8; text-align: center; }
        .form-section { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 25px; border: 1px solid #e1e4e8; }
        input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
        .btn { border: none; padding: 10px 15px; cursor: pointer; border-radius: 6px; font-weight: bold; text-decoration: none; display: inline-block; }
        .btn-add { background: #28a745; color: white; width: 100%; margin-top: 10px; }
        .btn-upd { background: #ffc107; color: #333; font-size: 0.8em; }
        .btn-del { background: #dc3545; color: white; font-size: 0.8em; }
        
        /* Estilos del Desplegable */
        details { background: #ffffff; border: 1px solid #1a73e8; border-radius: 8px; overflow: hidden; margin-top: 20px; }
        summary { padding: 15px; background: #1a73e8; color: white; cursor: pointer; font-weight: bold; outline: none; list-style: none; }
        summary::-webkit-details-marker { display: none; }
        summary:after { content: ' 🔽'; float: right; }
        details[open] summary:after { content: ' 🔼'; }
        
        .student-card { border-bottom: 1px solid #eee; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .student-card:last-child { border-bottom: none; }
        .info { flex-grow: 1; }
        .badge { background: #e8f0fe; color: #1a73e8; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 SGE: Gestión Estudiantil</h1>
        
        <div class="form-section">
            <h2>{{ '📝 Editar Estudiante' if edit_est else '➕ Registrar Estudiante' }}</h2>
            <form method="POST" action="{{ url_for('guardar_estudiante') }}">
                <input type="hidden" name="id" value="{{ edit_est.id if edit_est else '' }}">
                <input type="text" name="nombre" placeholder="Nombre del Estudiante" value="{{ edit_est.nombre if edit_est else '' }}" required>
                <input type="text" name="curso" placeholder="Curso / Asignatura" value="{{ edit_est.curso if edit_est else '' }}" required>
                <input type="number" step="0.1" name="nota" placeholder="Calificación" value="{{ edit_est.nota if edit_est else '' }}" required>
                <button type="submit" class="btn btn-add">{{ 'Actualizar Registro' if edit_est else 'Guardar Estudiante' }}</button>
                {% if edit_est %}
                    <a href="/" style="display:block; text-align:center; margin-top:10px; color:#666; font-size:0.9em;">❌ Cancelar Edición</a>
                {% endif %}
            </form>
        </div>

        <details {{ 'open' if not edit_est and estudiantes }}>
            <summary>🔍 Consultar Listado de Estudiantes ({{ estudiantes|length }})</summary>
            <div class="list-content">
                {% for s in estudiantes %}
                    <div class="student-card">
                        <div class="info">
                            <strong>{{ s.nombre }}</strong> <span class="badge">{{ s.curso }}</span><br>
                            <small>Nota Final: {{ s.nota }} | ID: {{ s.id }}</small>
                        </div>
                        <div>
                            <a href="/editar/{{ s.id }}" class="btn btn-upd">Editar</a>
                            <a href="/eliminar/{{ s.id }}" class="btn btn-del" onclick="return confirm('¿Seguro que desea eliminar?')">Borrar</a>
                        </div>
                    </div>
                {% else %}
                    <p style="padding: 20px; text-align: center; color: #666;">No hay datos para mostrar.</p>
                {% endfor %}
            </div>
        </details>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # READ: Consulta masiva de claves con patrón 'estudiante:*' 
    keys = db.keys('estudiante:*')
    estudiantes = []
    for key in keys:
        data = db.hgetall(key)
        data['id'] = key.split(':')[1]
        estudiantes.append(data)
    return render_template_string(HTML_LAYOUT, estudiantes=estudiantes, edit_est=None)

@app.route('/guardar', methods=['POST'])
def guardar_estudiante():
    # CREATE / UPDATE: Lógica combinada 
    est_id = request.form.get('id')
    if not est_id:
        est_id = str(uuid.uuid4())[:6].upper()
    
    db.hset(f"estudiante:{est_id}", mapping={
        "nombre": request.form.get('nombre'),
        "curso": request.form.get('curso'),
        "nota": request.form.get('nota')
    })
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar_vista(id):
    # READ específico para edición 
    data = db.hgetall(f"estudiante:{id}")
    data['id'] = id
    
    keys = db.keys('estudiante:*')
    estudiantes = []
    for key in keys:
        s_data = db.hgetall(key)
        s_data['id'] = key.split(':')[1]
        estudiantes.append(s_data)
        
    return render_template_string(HTML_LAYOUT, estudiantes=estudiantes, edit_est=data)

@app.route('/eliminar/<id>')
def eliminar(id):
    # DELETE 
    db.delete(f"estudiante:{id}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)