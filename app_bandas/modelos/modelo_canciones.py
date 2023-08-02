from app_bandas.config.mysqlconnection import connectToMySQL
from app_bandas import BASE_DATOS
from app_bandas.modelos.modelo_usuarios import Usuario
from flask import flash

class Cancion:
    def __init__( self, data ):
        self.id_cancion = data['id_cancion']
        self.titulo_cancion = data['titulo_cancion']
        self.descripcion = data['descripcion']
        self.frase_favorita = data['frase_favorita']
        self.id_banda = data['id_banda']
        self.banda = None
    
    @classmethod
    def crear_cancion( cls, data):
        query = """
                INSERT INTO canciones ( titulo_cancion, descripcion, frase_favorita, id_banda )
                VALUES (%(titulo_cancion)s, %(descripcion)s, %(frase_favorita)s, %(id_banda)s);
                """
        id_cancion = connectToMySQL( BASE_DATOS ).query_db( query, data )
        print(id_cancion)
        return id_cancion

    @classmethod
    def obtener_canciones_banda( cls, id_banda ):
        query = """
                SELECT *
                FROM canciones c
                WHERE c.id_banda = %(id)s;
                """            
        data = {
            "id_banda": id_banda
        }
        resultado = connectToMySQL( BASE_DATOS ).query_db( query, data )
        lista_canciones = []
        for renglon in resultado:
            cancion = Cancion(renglon)
            lista_canciones.append(cancion)
        return lista_canciones
    
    @classmethod
    def editar_cancion(cls, data):
        query = """
                UPDATE canciones
                SET titulo_cancion = %(titulo_cancion)s, descripcion = %(descripcion)s, frase_favorita = %(frase_favorita)s
                WHERE id_cancion = %(id_cancion)s AND id_banda = %(id_banda)s;
                """
        return connectToMySQL(BASE_DATOS).query_db(query, data)
    
    @classmethod
    def obtener_cancion_por_id(cls, id_cancion):
        query = """
                SELECT *
                FROM canciones
                WHERE id_cancion = %(id)s;    
                """
        data = {
            "id": id_cancion
        }
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        if resultado:
            return Cancion(resultado[0])
        else:
            return None
    
    @classmethod
    def obtener_cancion_y_creador(cls, id_cancion):
        query = """
                SELECT c.*, u.*
                FROM canciones AS c
                JOIN bandas AS b ON c.id_banda = b.id
                JOIN usuarios AS u ON b.id_usuario_banda = u.id
                WHERE c.id_cancion = %(id)s;    
                """
        data = {
            "id": id_cancion
        }
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        if resultado:
            return Cancion(resultado[0]), Usuario(resultado[0])
        else:
            return None

    @classmethod
    def elimina_cancion( cls, data ):
        query = """
                DELETE FROM canciones
                WHERE id_cancion = %(id_cancion)s;
                """
        return connectToMySQL( BASE_DATOS ).query_db( query, data )

    @staticmethod
    def validar_cancion( data ):
        es_valido = True
        if len( data['titulo_cancion'] ) < 2:
            es_valido = False
            flash("Debes proporcionar un título para la canción", "error_titulo_cancion")
        if len( data['descripcion'] ) < 2:
            es_valido = False
            flash("Debes proporcionar una descripción para la canción", "error_descripcion")
        if len( data['frase_favorita'] ) < 2:
            es_valido = False
            flash("Debes proporcionar una frase favorita de la canción", "error_frase_favorita")
        return es_valido
