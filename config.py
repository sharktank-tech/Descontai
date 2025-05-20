
class Config:
    # ========== Configuração da aplicação
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:xBtnAUiVePcXNsmSviyxhIrgCeAoCyxK@shuttle.proxy.rlwy.net:33698/railway'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'geesirgvj0gre8v8u8dger54ng95ngngdgdeg5yhsh'
    FLASK_APP = 'run'

    # ========= Configuração do envio de e-mail ==========

    EMAIL_DESTINE = "danilokog652@gmail.com"
    SERVIDOR = "smtp.gmail.com"
    PASWD = "hxwi kiju ofko itwb"
    PORTA_SMPT = 587
    REMEMTENTE = "quicknotes527@gmail.com"