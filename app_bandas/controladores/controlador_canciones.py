from app_bandas import app
from flask import render_template, request, redirect, session, flash
from app_bandas.modelos.modelo_canciones import Cancion
from app_bandas.modelos.modelo_bandas import Banda

@app.route('/formulario/agregar/cancion/<id_banda>', methods=['GET'])
def mostrar_formulario_cancion(id_banda):
    if 'id_usuario' not in session:
        flash("Necesitas iniciar sesión primero")
        return redirect('/')
    session['id_banda'] = id_banda  
    banda = Banda.obtener_banda_por_id(id_banda)
    return render_template("crear_canciones.html", banda=banda)

@app.route('/formulario/agregar/cancion/<id_banda>', methods=['POST'])
def recibir_formulario_cancion(id_banda):
    if 'id_usuario' not in session:
        flash("Necesitas iniciar sesión primero")
        return redirect('/')
    print(request.form)
    if not Cancion.validar_cancion(request.form):
        return redirect(f'/formulario/agregar/cancion/{id_banda}')
    data = {
        "titulo_cancion": request.form["titulo_cancion"],
        "descripcion": request.form["descripcion"],
        "frase_favorita": request.form["frase_favorita"],
        "id_banda": id_banda  # Cambiamos "id_bandas" a "id_banda"
    }
    Cancion.crear_cancion(data)
    return redirect('/perfil')

@app.route('/formulario/editar/cancion/<id_cancion>', methods=['GET'])
def mostrar_formulario_editar_cancion(id_cancion):
    if 'id_usuario' not in session:
        flash("Necesitas iniciar sesión primero")
        return redirect('/')
    cancion = Cancion.obtener_cancion_por_id(id_cancion)
    banda = Banda.obtener_banda_por_id(cancion.id_banda)
    return render_template("editar_canciones.html", cancion=cancion, banda=banda)


@app.route('/formulario/editar/cancion/<id_cancion>', methods=['POST'])
def actualizar_cancion(id_cancion):
    if 'id_usuario' not in session:
        flash("Necesitas iniciar sesión primero")
        return redirect('/')
    print(request.form)
    if not Cancion.validar_cancion(request.form):
        return redirect(f'/formulario/editar/cancion/{id_cancion}')
    data = {
        "titulo_cancion": request.form["titulo_cancion"],
        "descripcion": request.form["descripcion"],
        "frase_favorita": request.form["frase_favorita"],
        "id_cancion": id_cancion,
        "id_banda": session['id_banda']
    }
    Cancion.editar_cancion(data)
    return redirect('/perfil')

@app.route('/eliminar/cancion/<id_cancion>', methods=['POST'])
def eliminar_cancion(id_cancion):
    if 'id_usuario' not in session:
        flash("Necesitas iniciar sesión primero")
        return redirect('/')
    cancion, creador = Cancion.obtener_cancion_y_creador(id_cancion)
    if creador.id != session['id_usuario']:
        flash("No tienes permiso para eliminar esta canción")
        return redirect('/perfil')
    data = {
        "id_cancion": id_cancion
    }
    Cancion.elimina_cancion(data)
    return redirect('/perfil')




