# bluedraftapi

Esta es una api creada para el challenge de Bluedraft. La misma consta de una simple app en la cual se puede crear, editar, listar y eliminar tanto monedas como billeteras de usuarios. Utilice Django-Rest-Framework para la construccion de la API. Esta la hice mediante clases, utilizando "APIView" para poder controlar bien cada uno de los verbos HTTP que queria realizar a bajo nivel. El proyecto esta dividido en dos aplicaciones que interactuan entre ellas (api y user). La primera, "api" contiene todo lo que es la api para el manejo de las monedas y billeteras. Y la aplicacion "user" se encarga de todo lo que es el login y el registro de usuarios a la api.

Construir y ejecutar app:
    - docker-compose up --build

Endpoints:

    COIN:
        - GET Coin list: http://localhost:8000/api/coin/
        - GET Coin by Name: http://localhost:8000/api/coin/?name=USDT
        - POST Coin: http://localhost:8000/api/coin/
        - PUT Coin: http://localhost:8000/api/coin/1
        - DELETE Coin: http://localhost:8000/api/coin/2

    WALLET:
        - GET Wallet: http://localhost:8000/api/wallet/
        - POST Wallet: http://localhost:8000/api/wallet/
        - POST Wallet Send Coins: http://localhost:8000/api/wallet/send/
        - PUT Wallet: http://localhost:8000/api/wallet/
        - DELETE Wallet: http://localhost:8000/api/wallet/

    USER:
        - POST User Register: http://localhost:8000/api/register/
        - POST User Login: http://localhost:8000/api/login/

POSTMAN:
Se deja en el repositorio una archivo .json (importar en postman) en el cual se puede encontrar una coleccion de metedos de Postman para poder probar mejor los endpoints.
Los mismos metodos dentro contienen los body correspondientes a enviar a la api para que esta funcione correctamente.