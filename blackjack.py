from pyteal import *

def approval():
    init = Seq([
        App.globalPut(Bytes("admin"), Txn.sender()),
        Return(Int(1)),
    ])

    is_admin = Txn.sender() == App.globalGet(Bytes("admin"))

    # get another card
    hit = Seq([])

    # take no more cards
    stand = Seq([])

    # 
    double_down = Seq([])

    # create two hands
    split = Seq([])

    # forfeit half the bet
    surrender = Seq([])

    bet = Seq([])

    return Cond(
        [],
        [],
    )


def clear():
    return Seq([Return(Int(1))])


