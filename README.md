# poczta-polska-e-nadawca-python
## Short and quick class easing use of Poczta Polska e-nadawca WSDL API. It exposes service methods and factory types directly on instance.

### Installation
```
pip install  poczta_polska_enadawca
```

### Setup and usage with Django

Define following variables in your project settings:

* POCZTA_POLSKA_API_USERNAME
* POCZTA_POLSKA_API_PASSWORD
* POCZTA_POLSKA_API_SANDBOX_USERNAME
* POCZTA_POLSKA_API_SANDBOX_PASSWORD

After that - use as follows:

```
from poczta_polska_enadawca.api import PocztaPolskaAPI


PocztaInstance = PocztaPolskaAPI()
```

and you can call:
```
PocztaInstance.hello('Poczta API')
```

### Setup and usage rest of the world :)

```
from poczta_polska_enadawca.api import PocztaPolskaAPI
from poczta_polska_enadawca.settings import PocztaPolskaSettingsObject


PocztaPolskaSettings = PocztaPolskaSettingsObject()
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_USERNAME = 'foo'
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_PASSWORD = 'bar'
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_SANDBOX_USERNAME = 'foo'
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_SANDBOX_PASSWORD = 'bar'

PocztaInstance = PocztaPolskaAPI(initZeep=False) #we're not executing default init
PocztaInstance.set_config(PocztaPolskaSettings) #provide the object with settings defined above
PocztaInstance.init_zeep() #initialize zeep

```
That should be working at this moment.

## Where is the factory and service ?!

If you insist they're avaliable as .service and .factory on instance.

BUT

Factory is exposed directly as dictionary on the API instance. It's avaliable after execution of init_zeep.

```
PocztaInstance['adresType']
PocztaInstance['przesylkaPoleconaKrajowaType']
PocztaInstance['przesylkaEPOType']
```

Service methods are also avaliable DIRECTLY on instance. They're rewired after execution of init_zeep.
WARNING ! Example below does not work it only shows few simple calls.

```
PocztaInstance = PocztaPolskaAPI() #default init, you might need the fancy one few lines above

PocztaInstance.hello("Python")

adresType = PocztaInstance['adresType']
adresType.nazwa = 'foo'
adresType.ulica = 'bar'

przesylkaPoleconaKrajowaType = PocztaInstance['przesylkaPoleconaKrajowaType']
przesylkaPoleconaKrajowaType.adres = adresType

PocztaInstance.clearEnvelope()
PocztaInstance.addShipment(przesylkaPoleconaKrajowaType)
PocztaInstance.sendEnvelope()

```

### I want testing Enviroment, Labs Endpoints ...

Class init uses following key arguments:
PocztaPolskaAPI(useTest=False, useLabs=False, initZeep=True)

* useTest (default -> False) - run the calls against sandbox enviroment -> https://en-testwebapi.poczta-polska.pl
* useLabs (default -> False) - run the calls against labs endpoints
* initZeep (default -> True) - initialize zeep on init. 


### I need to debug zeep ...
```
PocztaInstance.enable_zeep_debug()
```

## Few examples of init: 

#### If you need the test enviroment:
```
PocztaInstance = PocztaPolskaAPI(useTest=True)
```

#### If you need the labs test enviroment:
```
PocztaInstance = PocztaPolskaAPI(useTest=True, useLabs=False)
```
