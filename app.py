from app import app
if __name__ == "__main__":
    #context = ('certificate/cert-selfsig.crt', 'certificate/key.key')
    app.run(debug=True)#ssl_context=context)