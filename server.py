from app_bandas.controladores import controlador_usuarios, controlador_bandas, controlador_canciones
from app_bandas import app

if __name__ == "__main__":
    app.run(debug = True, port = 5031)
    