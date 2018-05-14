# creates mnemonic passphrases in BIP39 standards
# https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki
from stellar_base.utils import StellarMnemonic
# generates keypair with stellar core
from stellar_base.keypair import Keypair
# requests to interact with stellar blockchain
import requests
from stellar_base.builder import Builder
from stellar_base.address import Address


class Stellar_block():
    def __init__(self, secret=''):
        '''
        Generates mnemonic_secret from stellar base, this has to be stored in the database to retrive seed in the future
        '''
        self.stellar_url = 'https://friendbot.stellar.org'
        if not secret:
            self.mnemonic_secret = StellarMnemonic().generate()
        else:
            # TODO: check if secret is a valid mnemonic string
            self.mnemonic_secret = secret
        return

    def create_account(self):
        '''
        Creates an account on stellar test net
        '''
        kp = self._generate_keypair()
        publickey = kp.address().decode()
        url = self.stellar_url
        r = requests.get(url, params={'addr': publickey})
        if r.status_code == 200:
            return 'SUCCESS'
        return 'ERROR'

    def get_seed(self):
        '''
        Get's seed from mnemonic_secret
        '''
        kp = self._generate_keypair()
        return kp.seed().decode()

    def get_passphrase(self):
        return self.mnemonic_secret

    def get_pubkey(self):
        return self._generate_keypair().address().decode()

    def _generate_keypair(self):
        if self.mnemonic_secret:
            kp = Keypair.deterministic(self.mnemonic_secret)
        return kp

    def transfer(self, amount, to_address, description):
        '''

        '''
        if float(self._get_balance()) < float(amount):
            return 'Insufficient Balance'
        seed = self.get_seed()
        builder = Builder(secret=seed)
        # builder = Builder(secret=seed, network='public') for LIVENET
        builder.append_payment_op(to_address, amount, 'XLM')
        builder.add_text_memo(description)  # string length <= 28 bytes
        builder.sign()

        # Uses an internal horizon instance to submit over the network
        builder.submit()
        return 'SUCCESS'

    def _get_balance(self):
        address = Address(address=self._generate_keypair().address().decode())
        address.get()  # get the updated information

        return address.balances[0]['balance']

    def _get_data(self):
        address = Address(address=self._generate_keypair().address().decode())
        address.get()  # get the updated information
        return address.data

    def _string_lenght_bytes(self, s):
        return len(s.encode('utf-8'))


if __name__ == '__main__':
    user1 = Stellar_block()
    print(user1.mnemonic_secret)
    print(user1.create_account())
