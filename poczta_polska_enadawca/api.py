import zeep
import logging.config
from requests import Session
from requests.auth import HTTPBasicAuth


try:
    from django.conf import settings
except:
    settings = None


class PocztaPolskaSettingsObject(object):
    POCZTA_POLSKA_API_USERNAME = None
    POCZTA_POLSKA_API_PASSWORD = None
    POCZTA_POLSKA_API_SANDBOX_USERNAME = None
    POCZTA_POLSKA_API_SANDBOX_PASSWORD = None


class PocztaPolskaAPI(object):
    '''
        That's a quickly written Class for Poczta Polska e-nadawca services.
    '''

    PROD_API_WSDL = 'https://e-nadawca.poczta-polska.pl/websrv/en.wsdl'
    PROD_API_LABS_WSDL = 'https://e-nadawca.poczta-polska.pl/websrv/labs.wsdl'
    PROD_USERNAME = None
    PROD_PASSWORD = None

    SANDBOX_API_WSDL = 'https://en-testwebapi.poczta-polska.pl/websrv/en.wsdl'
    SANDBOX_API_LABS_WSDL = 'https://en-testwebapi.poczta-polska.pl/websrv/labs.wsdl'
    SANDBOX_USERNAME = None
    SANDBOX_PASSWORD = None

    client = None
    service = None
    factory = None

    def __init__(self, debugMode=False, useLabs=False, initZeep=True):
        self.debugMode = debugMode
        self.useLabs = useLabs

        #sorry for that but i liked it from JS :)
        settings and self.set_config(settings)
        initZeep and self.init_zeep()

    def __getitem__(self, key):
        '''
            Shortcut to get_from_factory.
            Use: your_instance['addressType']
        '''

        return self.get_from_factory(key)

    def __attach_service_refs(self):
        '''
            Attach service methods DIRECTLY to class instance
        '''

        for service_name in self.service.__dir__():
            #skip magic
            if service_name.startswith('__'):
                continue

            service_method = self.service_get(service_name)
            if type(service_method) is zeep.client.OperationProxy:
                setattr(self, service_name, service_method)

    def set_config(self, settings):
        '''
            We can set the config here by passing a object.
        '''

        self.PROD_USERNAME = getattr(settings, 'POCZTA_POLSKA_API_USERNAME', None)
        self.PROD_PASSWORD = getattr(settings, 'POCZTA_POLSKA_API_PASSWORD', None)
        self.SANDBOX_USERNAME = getattr(settings, 'POCZTA_POLSKA_API_SANDBOX_USERNAME', None)
        self.SANDBOX_PASSWORD = getattr(settings, 'POCZTA_POLSKA_API_SANDBOX_PASSWORD', None)

        self.check_config()

    def check_config(self):
        '''
            Are we setup ?
        '''

        if self.debugMode:
            if self.SANDBOX_USERNAME is None:
                raise UnboundLocalError('Debug Mode is active - Sandbox username is not defined')

            if self.SANDBOX_PASSWORD is None:
                raise UnboundLocalError('Debug Mode is active - Sandbox password is not defined')
        else:
            if self.PROD_USERNAME is None:
                raise UnboundLocalError('Production username is not defined')

            if self.PROD_PASSWORD is None:
                raise UnboundLocalError('Production password is not defined')

    @property
    def wsdl_url(self):
        if self.debugMode:
            return self.SANDBOX_API_LABS_WSDL if self.useLabs else self.SANDBOX_API_WSDL

        return self.PROD_API_LABS_WSDL if self.useLabs else self.SANDBOX_API_WSDL

    def init_zeep(self):
        '''
            Initialize ZEEP objects and attach service method references directly to instance.
        '''

        #are the credentials here
        self.check_config()

        #add http basic auth wrapper to http requests
        session = Session()
        session.auth = HTTPBasicAuth(
            self.PROD_USERNAME if not self.debugMode else self.SANDBOX_USERNAME,
            self.PROD_PASSWORD if not self.debugMode else self.SANDBOX_PASSWORD,
        )

        #wrapped client
        self.client = zeep.Client(self.wsdl_url, 
            transport=zeep.transports.Transport(session=session))

        self.factory = self.client.type_factory('ns0')

        #wrong service endpoint in WSDL override
        if self.debugMode:
            if self.useLabs:
                self.s = self.client.create_service('{http://e-nadawca.poczta-polska.pl}LABSBinding', 
                    'https://en-testwebapi.poczta-polska.pl/websrv/labs.php')
            else:
                self.s = self.client.create_service('{http://e-nadawca.poczta-polska.pl}ENBinding', 
                    'https://en-testwebapi.poczta-polska.pl/websrv/en.php')
        else:
            self.s = self.client.service

        self.service = self.s
        self.__attach_service_refs()

    def enable_zeep_debug(self):
        '''
            Enable verbose ZEEP debugging.
        '''
        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'verbose': {
                    'format': '%(name)s: %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                'zeep.transports': {
                    'level': 'DEBUG',
                    'propagate': True,
                    'handlers': ['console'],
                },
            }
        })

    def get_from_factory(self, object_type):
        '''
            Grab fresh type from factory.
        '''

        if not type(object_type) is type(str('')):
            raise TypeError('Object type is required to be string')

        assert self.factory, "Type Factory is unavaliable, please provide valid settings via .set_config(settings) and run .init_zeep() on instance"
        return self.factory[object_type]

    def service_get(self, method):
        '''
            That's preety much proxy get.
        '''

        assert self.s, "Service is unavaliable, please provide valid settings via .set_config(settings) and run .init_zeep() on instance"

        service_method = getattr(self.s, method, None)

        if not service_method:
            raise ('Servide does not provide the %s method' % method)

        return service_method

    def service_call(self, method, *args):
        '''
            That's preety much proxied call.
        '''
        return self.service_get(method)(*args)
