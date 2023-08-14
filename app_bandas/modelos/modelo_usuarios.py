from app_bandas.config.mysqlconnection import connectToMySQL
from app_bandas import EMAIL_REGEX, BASE_DATOS
from flask import flash


class Usuario:
    def __init__( self, data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password = data['password']
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']
        self.fecha_nacimiento = data.get('fecha_nacimiento', None)
        self.descripcion_usuario = data.get('descripcion_usuario', None)
        self.estilo_rock = data.get('estilo_rock', None)
    
    
    @classmethod
    def crear_uno( cls, data ):
        query = """
                INSERT INTO usuarios ( nombre, apellido, email, password )
                VALUES ( %(nombre)s, %(apellido)s, %(email)s, %(password)s );
                """
        id_usuario = connectToMySQL( BASE_DATOS ).query_db( query, data )
        return id_usuario
    
    @classmethod
    def obtener_email( cls, data ):
        query = """
                SELECT *
                FROM usuarios
                WHERE email = %(email)s
                """
        resultado = connectToMySQL( BASE_DATOS ).query_db( query, data )
        if len( resultado ) == 0:
            return None
        else:
            return Usuario( resultado[0] )
        
    @classmethod
    def tarjeta_usuario(cls, data):
        query = """
                SELECT usuarios.nombre, usuarios.fecha_nacimiento, usuarios.fecha_creacion, usuarios.descripcion_usuario, estilos_rock.descripcion AS estilo_rock_descripcion
                FROM usuarios
                JOIN estilos_rock ON usuarios.estilo_rock = estilos_rock.id
                WHERE usuarios.id = %(id_usuario)s
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        if len(resultado) == 0:
            return None
        else:
            return resultado[0]
    
    
    @staticmethod
    def validar_registro( data ):
        es_valido = True
        if len( data["nombre"] ) < 2:
            es_valido = False
            flash("Tu nombre debe contener al menos 2 carácteres.", "error_nombre")
        if len( data["apellido"] ) < 2:
            es_valido = False
            flash("Tu apellido debe contener al menos 2 carácteres.", "error_apellido")
        if not EMAIL_REGEX.match(data["email"]):
            es_valido = False
            flash("Por favor, proporciona un email válido.", "error_email")
        if len( data["password"] ) < 8:
            es_valido = False
            flash("Tu password debe contener al menos 8 carácteres.", "error_password")    
        if data["password"] != data["confirmacion_password"]:
            es_valido = False
            flash("Tus password no coinciden.", "error_password")
        return es_valido
