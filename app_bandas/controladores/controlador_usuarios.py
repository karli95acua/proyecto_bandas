from flask import render_template, request, session, redirect, flash
from app_bandas.modelos.modelo_usuarios import Usuario
from app_bandas.modelos.modelo_canciones import Cancion
from flask_bcrypt import Bcrypt
from app_bandas import app


bcrypt = Bcrypt ( app )

@app.route('/', methods = ['GET'])
def desplegar_login_registro():
    return render_template( 'login.html' )

@app.route( '/crear/usuario', methods = ['POST'] )
def nuevo_usuario():
    data = {
        **request.form
    }
    if Usuario.validar_registro( data ) == False:
        return redirect( '/' )
    else:
        password_encriptado = bcrypt.generate_password_hash( data['password'] )
        data['password'] = password_encriptado
        id_usuario = Usuario.crear_uno( data )
        session['nombre'] = data['nombre']
        session['apellido'] = data['apellido']
        session['id_usuario'] = id_usuario

        return redirect( '/perfil' )


@app.route( '/login', methods = ['POST'] )
def procesa_login():
    data = {
        "email": request.form['email_login']
    }
    usuario_existe = Usuario.obtener_email( data )
    if usuario_existe == None:
        flash( "Este usuario no existe", "error_email_login" )
        return redirect( '/' )
    else:
        if not bcrypt.check_password_hash( usuario_existe.password, request.form['password_login'] ):
            flash( "Password incorrecta", "error_password_login" )
            return redirect( '/' )
        else:
            session['nombre'] = usuario_existe.nombre
            session['apellido'] = usuario_existe.apellido
            session['id_usuario'] = usuario_existe.id
            return redirect( '/perfil' )


@app.route( '/logout', methods = ['POST'] )
def procesa_logout():
    session.clear()
    return redirect( '/' )


