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


## Placowka type conversion:

That should come in useful :)
So after on week of trial and error i found that if you need to use pickup points, a certain type must be passed.
So i've built in a type converter ....

```

pp = PocztaInstance.getPlacowkiPocztowe(wojewodztwo.teryt_short_id)
placowkaPocztowa = [p for p in pp if p['id'] == int(adres.details['pni'])][0] #unfortunately - my request to get that by id was denied :)
urzadWydaniaEPrzesylkiType = PocztaInstance.convertPlacowkaToUrzad(placowkaPocztowa)

```


### Dude - i need something to paste ...
```
def kurier48_gen_etiquette(request, order, adres):

    PocztaInstance = PocztaPolskaAPI(useTest=settings.DEBUG)
    guid = PocztaInstance.getGuid(1)[0]

    package = PocztaInstance['przesylkaBiznesowaType']
    
    adresType = PocztaInstance['adresType']
    adresType.nazwa = adres.get_full_name()

    if adres.nazwa:
        adresType.nazwa2 = adres.get_person_name()

    adresType.ulica = adres.adres
    adresType.miejscowosc = adres.miasto
    adresType.kodPocztowy = adres.kod
    adresType.mobile = adres.mobile_no
    adresType.email = adres.email

    package.guid = guid
    package.niestandardowa = False
    package.gabaryt = shippingExtra.get('gabaryt', 'XXL')
    package.adres = adresType
    package.masa = order.waga_zamowienia(wGramach=True)
    package.ostroznie = False
    package.opis = '{o.site_name} {o.oid}'.format(o=order)
    package.wartosc = order.wartosc_zamowienia(wGroszach=True)

    if adres.details.get('pni'):
        
        wojewodztwo = Wojewodztwo.objects.get(nazwa__iexact=adres.details['province'])
        pp = PocztaInstance.getPlacowkiPocztowe(wojewodztwo.teryt_short_id)
        placowka_wydawcza = [p for p in pp if p['id'] == int(adres.details['pni'])][0]
        package['urzadWydaniaEPrzesylki'] = PocztaInstance.convertPlacowkaToUrzad(placowka_wydawcza, 'urzadWydaniaEPrzesylkiType')
    
    packageReturn = PocztaInstance.addShipment(package)
    packageReturn = packageReturn[0]

    shipping_return = {}
    shipping_return['raw'] = packageReturn

    if packageReturn['error']:
        shipping_return['success'] = False
        shipping_return['error_code'] = packageReturn['error']['errorNumber']
        shipping_return['error_message'] = packageReturn['error']['errorDesc']
    else:        
        shipping_return['numerNadania'] = packageReturn['numerNadania']
        shipping_return['guid'] = packageReturn['guid']
        shipping_return['parcelCode'] = '%s::%s' % (shipping_return['numerNadania'], shipping_return['guid'])
        shipping_return['success'] = True

    return shipping_return
```

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

