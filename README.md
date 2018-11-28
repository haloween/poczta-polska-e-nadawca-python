# poczta-polska-e-nadawca-python
## Short and quick class easing use of Poczta Polska e-nadawca WSDL API.
## It exposes service methods and factory types directly on instance.

### Installation
```
pip install  poczta_polska_enadawca
```


### Setup and usage with Django

Define following variables in your project settings:

POCZTA_POLSKA_API_USERNAME
POCZTA_POLSKA_API_PASSWORD
POCZTA_POLSKA_API_SANDBOX_USERNAME
POCZTA_POLSKA_API_SANDBOX_PASSWORD

After that - use as follows:

```
from poczta_polska_enadawca import PocztaPolskaAPI


PocztaAPI = PocztaPolskaAPI()
```

and you can call:
```
PocztaAPI.hello('Poczta API')
```

### Setup and usage rest of the world :)

```
from poczta_polska_enadawca import PocztaPolskaAPI, PocztaPolskaSettingsObject


PocztaPolskaSettings = PocztaPolskaSettingsObject()
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_USERNAME = 'foo'
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_PASSWORD = 'bar'
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_SANDBOX_USERNAME = 'foo'
PocztaPolskaSettingsObject.POCZTA_POLSKA_API_SANDBOX_PASSWORD = 'bar'

PocztaAPI = PocztaPolskaAPI(initZeep=False) #we're not executing default init
PocztaAPI.set_config(PocztaPolskaSettings) #provide the object with settings defined above
PocztaAPI.init_zeep() #initialize zeep

```
That should be working at this moment.


### Class init uses following key arguments:
PocztaPolskaAPI(debugMode=False, useLabs=False, initZeep=True)

debugMode (default -> False) - run the calls against sandbox enviroment -> https://en-testwebapi.poczta-polska.pl
useLabs (default -> False) - run the calls against labs endpoints
initZeep (default -> True) - initialize zeep on init. 

## Few examples: 

#### If you need the test enviroment:
```
PocztaAPI = PocztaPolskaAPI(debugMode=True)
```

#### If you need the labs test enviroment:
```
PocztaAPI = PocztaPolskaAPI(debugMode=True, useLabs=False)
```
