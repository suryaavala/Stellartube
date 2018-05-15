import pytest

from stellar_base.asset import Asset
from stellar_base.stellarxdr import Xdr
from stellar_base.transaction import Transaction
from stellar_base.operation import ChangeTrust
from stellar_base.horizon import horizon_testnet
from stellar_base.transaction_envelope import TransactionEnvelope as Te
from stellar_base.builder import Builder


def trust_asset(issuingkeys, receivingkeys, assetcode):
    builder = Builder(secret=issuingkeys.seed().decode(), network='TESTNET')
    builder.append_trust_op(destination=issuingkeys.address(
    ).decode(), code=assetcode, source=receivingkeys.address().decode())
    builder.sign(secret=issuingkeys.seed().decode())
    builder.sign(secret=receivingkeys.seed().decode())
    return builder.submit()


def send_asset(issuingkeys, receivingkeys, assetcode):
    send_v1 = Builder(secret=issuingkeys.seed().decode())
    send_v1.append_payment_op(receivingkeys.address().decode(
    ), '1', assetcode, issuingkeys.address().decode())
    send_v1.sign()
    return send_v1.submit()


if __name__ == '__main__':
    from app.stellar_block import *

