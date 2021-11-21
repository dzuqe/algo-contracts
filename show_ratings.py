# A contract that attaches likes and dislikes to associated reserves

from pyteal import *

def approval():
    # this constructor has three episodes. Each episode has data, likes count and dislike count. 
    # We also have a reserve for likes, dislikes 
    # And addresses to store payments for these tokens 
    on_init = Seq([
        Assert(Txn.application_args.length() == Int(5)),

        App.globalPut(Bytes("episode1_data"), Txn.application_args[0]),
        App.globalPut(Bytes("episode2_data"), Txn.application_args[1]),
        App.globalPut(Bytes("episode3_data"), Txn.application_args[2]),

        App.globalPut(Bytes("episode1_dislikes"), Int(0)),
        App.globalPut(Bytes("episode2_dislikes"), Int(0)),
        App.globalPut(Bytes("episode3_dislikes"), Int(0)),

        App.globalPut(Bytes("episode1_likes"), Int(0)),
        App.globalPut(Bytes("episode2_likes"), Int(0)),
        App.globalPut(Bytes("episode3_likes"), Int(0)),

        App.globalPut(Bytes("likes"), Int(1000000)),
        App.globalPut(Bytes("dislikes"), Int(1000000)),
        App.globalPut(Bytes("likes_reserve"), Txn.application_args[3]),
        App.globalPut(Bytes("dislikes_reserve"), Txn.application_args[4]),
        App.globalPut(Bytes("admin"), Txn.sender()),
        Return(Int(1))
    ])

    # check for admin
    is_admin = Txn.sender() == App.globalGet(Bytes("admin"))

    # optin to the app and set the likes and dislikes to 0.
    join = Seq([
        App.localPut(Int(0), Bytes("dislikes_claim"), Int(0)),
        App.localPut(Int(0), Bytes("likes_claim"), Int(0)),
        App.localPut(Int(0), Bytes("dislikes"), Int(0)),
        App.localPut(Int(0), Bytes("likes"), Int(0)),
        Return(Int(1)),
    ])

    # optin to the app and set the likes and dislikes to 0.
    leave = Seq([
        App.localPut(Int(0), Bytes("dislikes_claim"), Int(0)),
        App.localPut(Int(0), Bytes("likes_claim"), Int(0)),
        Return(Int(1)),
    ])

    sell_likes = Seq([
        App.localPut(Int(0), Bytes("likes_claim"), App.localGet(Int(0), Bytes("likes"))),
        App.localPut(Int(0), Bytes("likes"), Int(0)),
        Return(Int(1)),
    ])

    sell_dislikes = Seq([
        App.localPut(Int(0), Bytes("dislikes_claim"), App.localGet(Int(0), Bytes("dislikes"))),
        App.localPut(Int(0), Bytes("dislikes"), Int(0)),
        Return(Int(1)),
    ])

    # atomic transfer
    # check for correct amount
    # transfer from reserve to user
    amount = Btoi(Txn.application_args[1])
    buy_dislikes = Seq([
        Assert(
            And(
                App.globalGet(Bytes("dislikes")) >= Int(0),
                App.globalGet(Bytes("dislikes")) >= amount,
                Gtxn[1].amount() >= Int(1000000), 
                Gtxn[1].receiver() == App.globalGet(Bytes("dislikes_reserve")),
            ),
        ),
        App.globalPut(Bytes("dislikes"), App.globalGet(Bytes("dislikes")) - amount),
        App.localPut(Int(0), Bytes("dislikes"), App.localGet(Int(0), Bytes("dislikes")) + amount),
        Return(Int(1))
    ])

    buy_likes = Seq([
        Assert(
            And(
                App.globalGet(Bytes("likes")) >= Int(0),
                App.globalGet(Bytes("likes")) >= amount,
                Gtxn[1].amount() >= Int(1000000), 
                Gtxn[1].receiver() == App.globalGet(Bytes("likes_reserve")),
            ),
        ),
        App.globalPut(Bytes("likes"), App.globalGet(Bytes("likes")) - amount),
        App.localPut(Int(0), Bytes("likes"), App.localGet(Int(0), Bytes("likes")) + amount),
        Return(Int(1))
    ])

    # send likes or dislikes to the episode that youre interested in
    ep_name = Txn.application_args[1]
    amount = Btoi(Txn.application_args[2])
    dislike = Seq([
        Assert(App.localGet(Int(0), Bytes("dislikes")) >= Int(0)),
        Assert(App.localGet(Int(0), Bytes("dislikes")) >= amount),
        App.globalPut(ep_name, App.globalGet(ep_name) + amount),
        App.localPut(Int(0), Bytes("dislikes"), App.localGet(Int(0), Bytes("dislikes")) - amount),
        Return(Int(1)),
    ])

    like = Seq([
        Assert(App.localGet(Int(0), Bytes("likes")) >= Int(0)),
        Assert(App.localGet(Int(0), Bytes("likes")) >= amount),
        App.globalPut(ep_name, App.globalGet(ep_name) + (amount * In)),
        App.localPut(Int(0), Bytes("likes"), App.localGet(Int(0), Bytes("likes")) - amount),
        Return(Int(1)),
    ])

    return Cond(
        [Txn.application_id() == Int(0), on_init],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_admin)],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_admin)],
        [Txn.on_completion() == OnComplete.CloseOut, leave],
        [Txn.on_completion() == OnComplete.OptIn, join],
        [Txn.application_args[0] == Bytes("buy_likes"), buy_likes],
        [Txn.application_args[0] == Bytes("buy_dislikes"), buy_dislikes],
        [Txn.application_args[0] == Bytes("sell_likes"), sell_likes],
        [Txn.application_args[0] == Bytes("sell_dislikes"), sell_dislikes],
        [Txn.application_args[0] == Bytes("like"), like],
        [Txn.application_args[0] == Bytes("dislike"), dislike],
    )

def clear():
    return Seq([Return(Int(1))])

if __name__ == '__main__':
    with open('game.teal', 'w') as f:
        compiled = compileTeal(approval(), mode=Mode.Application, version=2)
        f.write(compiled)
    with open('clear.teal', 'w') as f:
        compiled = compileTeal(clear(), mode=Mode.Application, version=2)
        f.write(compiled)    
