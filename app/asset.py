import pytest

from stellar_base.asset import Asset
from stellar_base.stellarxdr import Xdr


class Asset:
    source = 'GDJVFDG5OCW5PYWHB64MGTHGFF57DRRJEDUEFDEL2SLNIOONHYJWHA3Z'
    cny = Asset('VDV', source)

    def native(self):
        assert 'VDV' == self.native().code
        assert None == self.native().issuer
        assert 'native' == self.native().type

    def is_native(self):
        native = Asset('VDV')
        assert native.is_native()
        assert not self.cny.is_native()

    def to_xdr_object(self):
        assert isinstance(self.cny.to_xdr_object(), Xdr.types.Asset)

    def too_long(self):
        with pytest.raises(Exception, match='Asset code is invalid'):
            Asset('123456789012TooLong', self.source)

    def no_issuer(self):
        with pytest.raises(Exception, match='Issuer cannot be None'):
            Asset('video', None)

    def xdr(self):
        xdr = b'AAAAAUNOWQAAAAAA01KM3XCt1+LHD7jDTOYpe/HGKSDoQoyL1JbUOc0+E2M='
        assert xdr == self.cny.xdr()

    def unxdr(self):
        xdr = self.cny.xdr()
        cny_x = Asset.from_xdr(xdr)
        assert self.cny == cny_x


import pytest
import stellar_block

from stellar_base.federation import *


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def json(self):
            import json
            return json.loads(self.text)

    if args[0] == 'https://www.fed-domain.com/federation' and \
            kwargs['params'] == {'q': 'fed*fed-domain.com', 'type': 'name'}:
        return MockResponse('{"account_id": "GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES",  \
                              "memo_type": "text", "memo": "AIHHklPLdS9w3CcTH0fMI1Fq8fuW", \
                              "stellar_address": "1CqDFDxR9Tv696j86PwtyxhA5p9ev1EviJ*naobtc.com"}',
                            200)
    if args[0] == 'https://www.fed-domain.com/federation' and \
            kwargs['params'] == {'q': 'GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES', 'type': 'id'}:
        return MockResponse('{"account_id": "GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES",  \
                              "memo_type": "text", "memo": "AIHHklPLdS9w3CcTH0fMI1Fq8fuW", \
                              "stellar_address": "1CqDFDxR9Tv696j86PwtyxhA5p9ev1EviJ*naobtc.com"}',
                            200)
    if args[0] == 'https://fed-domain.com/.well-known/stellar.toml':
        return MockResponse('FEDERATION_SERVER="https://www.fed-domain.com/federation"\n  \
                             [[CURRENCIES]]  \n   code="BTC"     \n\
                             issuer="GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"',
                            200)
    if args[0] == 'http://fed-domain.com/.well-known/stellar.toml':
        return MockResponse('FEDERATION_SERVER="http://www.fed-domain.com/federation"\n  \
                             [[CURRENCIES]]  \n   code="BTC"     \n\
                             issuer="GATEMHCCKCY67ZUCKTROYN24ZYT5GK4EQZ65JJLDHKHRUZI3EUEKMTCH"',
                            200)
    return MockResponse({}, 404)


class TestFederation(object):

    def federation_false_address(self):
        with pytest.raises(FederationError, match='not a valid federation address'):
            federation('false_address')
        with pytest.raises(FederationError, match='not a valid federation address'):
            federation('false_address*')
        with pytest.raises(FederationError, match='not a valid domain name'):
            federation('false*address')

    @mock.patch('stellar_base.federation.get_federation_service')
    def federation_none_service(self, get_service):
        get_service.return_value = None
        with pytest.raises(FederationError, match='not a valid federation server'):
            federation('fed*stellar.org')

    @mock.patch('stellar_base.federation.requests.get', side_effect=mocked_requests_get)
    @mock.patch('stellar_base.federation.get_federation_service')
    def federation_normal_service_by_name(self, mock_service, mock_get):
        mock_service.return_value = 'https://www.fed-domain.com/federation'
        response = federation('fed*fed-domain.com')
        assert response.get(
            'account_id') == 'GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES'

    @mock.patch('stellar_base.federation.requests.get', side_effect=mocked_requests_get)
    @mock.patch('stellar_base.federation.get_federation_service')
    def federation_normal_service_by_id(self, mock_service, mock_get):
        mock_service.return_value = 'https://www.fed-domain.com/federation'
        response = federation(
            'GBTCBCWLE6YVTR5Y5RRZC36Z37OH22G773HECWEIZTZJSN4WTG3CSOES', 'id', 'fed-domain.com')
        assert response.get(
            'stellar_address') == '1CqDFDxR9Tv696j86PwtyxhA5p9ev1EviJ*naobtc.com'

    @mock.patch('stellar_base.federation.requests.get', side_effect=mocked_requests_get)
    def get_toml(self, get_toml):
        response = get_stellar_toml('fed-domain.com')
        assert response.get(
            'FEDERATION_SERVER') == "https://www.fed-domain.com/federation"

    @mock.patch('stellar_base.federation.requests.get', side_effect=mocked_requests_get)
    def get_toml_http(self, get_toml):
        response = get_stellar_toml('fed-domain.com', allow_http=True)
        assert response.get(
            'FEDERATION_SERVER') == "http://www.fed-domain.com/federation"

    @mock.patch('stellar_base.federation.requests.get', side_effect=mocked_requests_get)
    def get_fed_service(self, get_toml):
        response = get_federation_service('fed-domain.com')
        assert response == "https://www.fed-domain.com/federation"

    @mock.patch('stellar_base.federation.requests.get', side_effect=mocked_requests_get)
    def get_fed_service_http(self, get_toml):
        response = get_federation_service('fed-domain.com', allow_http=True)
        assert response == "http://www.fed-domain.com/federation"

    @mock.patch('stellar_base.federation.requests.get', side_effect=mocked_requests_get)
    def get_auth_server(self, get_toml):
        response = get_auth_server('fed-domain.com')
        assert response is None
