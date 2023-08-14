from flask import render_template, request, session, redirect, flash
from app_bandas.modelos.modelo_bandas import Banda
from app_bandas import app

@app.route( '/dashboard', methods = ['GET'] ) #validado por session
def desplegar_dashboard():
    if "id_usuario" not in session:
        return redirect( '/' )
    else:
        lista_bandas = Banda.obtener_todas_las_bandas()
        return render_template('dashboard.html', lista_bandas=lista_bandas)

@app.route( '/formulario/banda', methods = ['GET'] ) #validado por session
def desplegar_crear_banda():
    if "id_usuario" not in session:
        return redirect( '/' )
    else:
        return render_template( 'crear_banda.html')

@app.route( '/nueva/banda', methods = ['POST'] )
def nueva_banda():
    data = {
        **request.form,
        "id_usuario": session['id_usuario']
    }
    if not Banda.validar_banda( data ):
        return redirect( '/formulario/banda' )
    else:
        id_banda = Banda.crear_banda( data )
        return redirect( '/dashboard' )

@app.route('/formulario/editar/banda/<int:id>', methods = ['GET'] ) #validado por session
def desplegar_editar_banda(id):
    if "id_usuario" not in session:
        return redirect( '/' )
    else:
        banda = Banda.obtener_banda_por_id(id)
        if banda:
            return render_template('editar_banda.html', banda = banda)
        else:
            return redirect('/dashboard')

@app.route('/editar/banda/<int:id>', methods = ['POST'])
def editar_banda( id ):
    if Banda.validar_banda( request.form ) == False:
        return redirect(f'/formulario/editar/banda/{id}')
    else:
        data = {
            **request.form,
            "id": id,
            "id_usuario" : session['id_usuario']
        }
        Banda.editar_banda( data )
        return redirect('/dashboard')
    
@app.route( '/mis/bandas', methods = ['GET'] ) #validado por session
def desplegar_mis_bandas():
    if "id_usuario" not in session:
        return redirect( '/' )
    else:
        lista_mis_bandas = Banda.obtener_mis_bandas(session['id_usuario'])
        return render_template('mis_bandas.html', lista_mis_bandas=lista_mis_bandas)

@app.route( '/eliminar/banda/<int:id>', methods = ['POST'] )
def eliminar_banda( id ):
    data = {
        "id" : id
    }
    Banda.elimina_una( data )
    return redirect( '/dashboard' )

