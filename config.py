
class Config:
    # ========== Configuração da aplicação
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres.ymqrprlpwrhxpdwfbtjk:Lab0d2Y0sAAdh0K7z4hf@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'geesirgvj0gre8v8u8dger54ng95ngngdgdeg5yhsh'
    FLASK_APP = 'run'

    # ========= Configuração do envio de e-mail ==========

    EMAIL_DESTINE = "danilokog652@gmail.com"
    SERVIDOR = "smtp.gmail.com"
    PASWD = "hxwi kiju ofko itwb"
    PORTA_SMPT = 587
    REMEMTENTE = "quicknotes527@gmail.com"