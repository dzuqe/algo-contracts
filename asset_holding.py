from pyteal import *

senderAssetBalance = AssetHolding.balance(Int(0), Int(0))
program1 = Seq([
    senderAssetBalance,
    senderAssetBalance.value()
])

accountAssetBalance = AssetHolding.balance(Int(1), Int(1))
program2 = Seq([
    accountAssetBalance,
    Assert(accountAssetBalance.hasValue()),
    accountAssetBalance.value()
])

if __name__ == '__main__':
    with open('sender.teal', 'w') as f:
        compiled = compileTeal(program1, mode=Mode.Application, version=2)
        f.write(compiled)
    with open('account1.teal', 'w') as f:
        compiled = compileTeal(program2, mode=Mode.Application, version=2)
        f.write(compiled)

