import zeep
import logging.config
from zeep.wsse.username import UsernameToken

try:
    from django.conf import settings as django_settings
except:
    django_settings = None


class PocztaPolskaWSTrackingAPI(object):
    '''
        That's a quickly written Class for Poczta Polska WS Tracking services.
    '''

    PROD_API_WSDL = 'http://ws.poczta-polska.pl/Sledzenie/services/Sledzenie?wsdl'
    PROD_USERNAME = None
    PROD_PASSWORD = None

    client = None
    service = None
    factory = None

    def __init__(self, initZeep=True, settings=django_settings):
        
        #sorry for that but i liked it from JS 
        settings and self.set_config(settings)
        initZeep and self.init_zeep()

    def __getitem__(self, key):
        '''
            Shortcut to get_from_factory.
            Use: your_instance['addressType']
        '''

        return self.get_from_factory(key)()

    def __attach_service_refs(self):
        '''
            Attach service methods DIRECTLY to class instance
        '''

        for service_name in self.service.__dir__():
            #skip magic
            if service_name.startswith('__'):
                continue

            service_method = self.service_get(service_name)

            #double check
            if type(service_method) is zeep.proxy.OperationProxy:
                setattr(self, service_name, service_method)

    def set_config(self, settings):
        '''
            We can set the config here by passing a proper object.
        '''

        self.PROD_USERNAME = getattr(settings, 'POCZTA_POLSKA_WSTRACKING_API_USERNAME', None)
        self.PROD_PASSWORD = getattr(settings, 'POCZTA_POLSKA_WSTRACKING_API_PASSWORD', None)
        
        self.check_config()

    def check_config(self):
        '''
            Are we setup ?
        '''

        if self.PROD_USERNAME is None:
            raise UnboundLocalError('Production username is not defined')

        if self.PROD_PASSWORD is None:
            raise UnboundLocalError('Production password is not defined')

    def init_zeep(self):
        '''
            Initialize ZEEP objects and attach service method references directly to instance.
        '''

        #are the credentials here
        self.check_config()

        #wrapped client
        self.client = zeep.Client(self.PROD_API_WSDL, 
            wsse=UsernameToken(self.PROD_USERNAME, self.PROD_PASSWORD)
        )

        self.factory = self.client.type_factory('ns0')
        
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
        
        return getattr(self.factory, object_type)

    def service_get(self, method):
        '''
            That's preety much proxy get.
        '''

        assert self.s, "Service is unavaliable, please provide valid settings via .set_config(settings) and run .init_zeep() on instance"

        service_method = getattr(self.s, method, None)

        if not service_method:
            raise ('Service does not provide the %s method' % method)

        return service_method

    def service_call(self, method, *args):
        '''
            That's preety much proxied call.
        '''
        return self.service_get(method)(*args)
    