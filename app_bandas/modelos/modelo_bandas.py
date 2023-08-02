from app_bandas.config.mysqlconnection import connectToMySQL
from app_bandas.modelos.modelo_usuarios import Usuario
from app_bandas import BASE_DATOS
from flask import flash


class Banda:
    def __init__( self, data ):
        self.id = data['id']
        self.nombre_banda = data['nombre_banda']
        self.genero_musical = data['genero_musical']
        self.ciudad_natal = data['ciudad_natal']
        self.id_usuario_banda = data['id_usuario_banda']
        self.usuario = None

    @classmethod
    def crear_banda( cls, data):
        query = """
                INSERT INTO bandas ( nombre_banda, genero_musical , ciudad_natal, id_usuario_banda )
                VALUES (%(nombre_banda)s,%(genero_musical)s, %(ciudad_natal)s, %(id_usuario)s);
                """
        id_banda = connectToMySQL( BASE_DATOS ).query_db( query, data )
        return id_banda
    
    @classmethod
    def obtener_mis_bandas( cls, id_usuario ):
        query = """
                SELECT *
                FROM bandas b JOIN usuarios u
                    ON b.id_usuario_banda = u.id
                WHERE u.id = %(id)s;    
                """
        data = {
        "id": id_usuario
        }
        resultado = connectToMySQL( BASE_DATOS ).query_db( query, data )
        lista_mis_bandas = []
        for renglon in resultado:
            banda = Banda(renglon)
            data_usuario = {
                "id": renglon['id'],
                "nombre": renglon['nombre'],
                "apellido": renglon['apellido'],
                "email": renglon['email'],
                "password": renglon['password'],
                "fecha_creacion": renglon['fecha_creacion'],
                "fecha_actualizacion": renglon['fecha_actualizacion']
            }
            usuario = Usuario(data_usuario)
            banda.usuario = usuario
            lista_mis_bandas.append(banda)
        return lista_mis_bandas

    @classmethod
    def obtener_todas_las_bandas( cls ):
        query = """
                SELECT *
                FROM bandas b JOIN usuarios u
                    ON b.id_usuario_banda = u.id;  
                """
        resultado = connectToMySQL( BASE_DATOS ).query_db( query )
        lista_bandas = []
        for renglon in resultado:
            banda = Banda(renglon)
            data_usuario = {
                "id": renglon['id'],
                "nombre": renglon['nombre'],
                "apellido": renglon['apellido'],
                "email": renglon['email'],
                "password": renglon['password'],
                "fecha_creacion": renglon['fecha_creacion'],
                "fecha_actualizacion": renglon['fecha_actualizacion']
            }
            usuario = Usuario(data_usuario)
            banda.usuario = usuario
            lista_bandas.append(banda)
        return lista_bandas


    @classmethod
    def editar_banda(cls, data):
        query = """
                UPDATE bandas
                SET nombre_banda = %(nombre_banda)s, genero_musical = %(genero_musical)s, ciudad_natal = %(ciudad_natal)s
                WHERE id = %(id)s AND id_usuario_banda = %(id_usuario)s;
                """
        return connectToMySQL(BASE_DATOS).query_db(query, data)
    
    @classmethod
    def obtener_banda_por_id(cls, id_banda):
        query = """
                SELECT *
                FROM bandas b JOIN usuarios u
                    ON b.id_usuario_banda = u.id
                WHERE b.id = %(id)s;    
                """
        data = {
        "id": id_banda
        }
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        if resultado:
            banda = Banda(resultado[0])
            data_usuario = {
                "id": resultado[0]['id'],
                "nombre": resultado[0]['nombre'],
                "apellido": resultado[0]['apellido'],
                "email": resultado[0]['email'],
                "password": resultado[0]['password'],
                "fecha_creacion": resultado[0]['fecha_creacion'],
                "fecha_actualizacion": resultado[0]['fecha_actualizacion']
            }
            usuario = Usuario(data_usuario)
            banda.usuario = usuario
            return banda
        else:
            return None

    @classmethod
    def obtener_bandas_canciones(cls, data):
        query = """
            SELECT b.*, c.titulo_cancion, c.id_cancion
            FROM bandas AS b
            LEFT JOIN canciones AS c ON b.id = c.id_banda
            WHERE b.id_usuario_banda = %(id_usuario)s;
            """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        bandas_canciones = []
        for renglon in resultado:
            banda = Banda(renglon)
            if not any(b.id == banda.id for b in bandas_canciones):
                banda.canciones = []
                bandas_canciones.append(banda)
            banda_cancion = next((b for b in bandas_canciones if b.id == banda.id), None)
            if banda_cancion:
                banda_cancion.canciones.append({
                    "titulo_cancion": renglon['titulo_cancion'],
                    "id_cancion": renglon['id_cancion']
                })
        return bandas_canciones


    
    @classmethod
    def elimina_una( cls, data ):
        query = """
                DELETE FROM bandas
                WHERE id = %(id)s;
                """
        return connectToMySQL( BASE_DATOS ).query_db( query, data )


    @staticmethod
    def validar_banda( data ):
        es_valido = True
        if len( data['nombre_banda'] ) < 2:
            es_valido = False
            flash("Debes proporcionar nombre de banda", "error_nombre_banda")
        if len( data['genero_musical'] ) < 2:
            es_valido = False
            flash("Debes proporcionar género musical de la banda", "error_genero_musical")
        if len( data['ciudad_natal'] ) < 2:
            es_valido = False
            flash("Debes proporcionar ciudad natal de la banda", "error_ciudad_natal")
        return es_valido