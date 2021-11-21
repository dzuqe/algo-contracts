# Roulette casino game contract

from pyteal import *

def approval():
  # zxsprectrum init
  on_init = Seq([
    # initial values for pseudo random generator
    App.globalPut(Bytes("a"), Int(75)),
    App.globalPut(Bytes("c"), Int(74)),
    App.globalPut(Bytes("m"), Int(65537)), #(1<<16)+1
    App.globalPut(Bytes("x"), Int(28652)),
    App.globalPut(Bytes("admin"), Txn.sender()),
    App.globalPut(Bytes("reserve"), Int(50000000)),
    Return(Int(1)),
  ])
  
  is_admin = Txn.sender() == App.globalGet(Bytes("admin"))

  # linear congruential generator
  # x = (a*x + c) % m
  gen_number = ((App.globalGet(Bytes("a"))*App.globalGet(Bytes("x")))+App.globalGet(Bytes("c")))%App.globalGet(Bytes("m"))

  rand = ScratchVar(TealType.uint64)

  #
  # Inside bets
  #
  bet = Btoi(Txn.application_args[1])
  bet_amount = Btoi(Txn.application_args[1])
  single_bet = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    # check for win or lose
    If(rand.load() == bet,
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Return(Int(1)),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Return(Int(1)),
      ])
    ),

    Approve(),
  ])

  first_bet = Btoi(Txn.application_args[1])
  second_bet = Btoi(Txn.application_args[2])
  split = Seq([
    Assert(Or(
      second_bet - first_bet == Int(1),
      second_bet - first_bet == Int(3),
    )),
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(Or(
      rand.load() == first_bet,
      rand.load() == second_bet,
      ),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Return(Int(1)),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Return(Int(1)),
      ]),
    ),
    Approve(),
  ])

  bet1 = Btoi(Txn.application_args[1])
  bet2 = Btoi(Txn.application_args[2])
  bet3 = Btoi(Txn.application_args[3])
  trio = Seq([
    Assert(And(
      bet1 < Int(4),
      bet2 < Int(4),
      bet3 < Int(4),
    )),
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(Or(
            rand.load() == bet1,
            rand.load() == bet2,
            rand.load() == bet3,
      ),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Return(Int(1)),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Return(Int(1)),
      ]),
    ),
    Approve(),
  ])

  #column = Seq([])
  #double_street = Seq([])
  #street = Seq([])

  #    
  # Outside bets
  #
  even = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(rand.load() % Int(2) == Int(0),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Return(Int(1)),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Return(Int(1)),
      ]),
    ),
    Approve(),
  ])

  odd = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(rand.load() % Int(2) != Int(0),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Return(Int(1)),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Return(Int(1)),
      ]),
    ),
    Approve(),
  ])

  # manque
  low = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(rand.load() <= Int(18),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Approve(),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Approve(),
      ]),
    ),
    Approve(),
  ])

  # passe
  high = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(rand.load() > Int(18),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Approve(),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Approve(),
      ]),
    ),
    Approve(),
  ])

  # first four
  first_four = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(rand.load() < Int(4),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Approve(),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Approve(),
      ]),
    ),
    Approve(),
  ])

  # dozen bet
  first_dozen = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(rand.load() <= Int(12),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Return(Int(1)),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Return(Int(1)),
      ]),
    ),
    Approve(),
  ])

  second_dozen = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(And(
      rand.load() > Int(12),
      rand.load() <= Int(24),
      ),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Approve(),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Approve(),
      ]),
    ),
    Approve(),
  ])

  third_dozen = Seq([
    App.globalPut(Bytes("x"), gen_number), # update random value
    rand.store(App.globalGet(Bytes("x")) % Int(36)),
    If(rand.load() > Int(24),
      Seq([ # win
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) - bet_amount),
        Approve(),
      ]),
      Seq([ # lose
        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
        Approve(),
      ]),
    ),
    Approve(),
  ])

#  first = ScratchVar(TealType.uint64)
#  second =  ScratchVar(TealType.uint64)
#  third =  ScratchVar(TealType.uint64)
#  forth = ScratchVar(TealType.uint64)
#
#  save = Seq([
#    forth.store(Int(32)),
#    second.store(Int(14)),
#    first.store(Int(5)),
#    third.store(Int(23)),
#    Approve(),
#  ])

#  red = Seq([
#    save,
#    App.globalPut(Bytes("x"), gen_number), # update random value
#    rand.store(App.globalGet(Bytes("x")) % Int(36)),
#    If(Or(
#      Or(
#        first.load() - Int(3) == rand.load(),
#        first.load() - Int(1) == rand.load(),
#        first.load() + Int(1) == rand.load(),
#        first.load() + Int(3) == rand.load(),
#      ),
#      Or(
#        Or(
#          second.load() - Int(3) == rand.load(),
#          second.load() - Int(1) == rand.load(),
#          second.load() + Int(1) == rand.load(),
#          second.load() + Int(3) == rand.load(),
#        ),
#        second.load() - Int(4) == rand.load(),
#      ),
#      Or(
#        third.load() - Int(3) == rand.load(),
#        third.load() - Int(1) == rand.load(),
#        third.load() + Int(1) == rand.load(),
#        third.load() + Int(3) == rand.load(),
#      ),
#      Or(
#        Or(
#          forth.load() - Int(3) == rand.load(),
#          forth.load() - Int(1) == rand.load(),
#          forth.load() + Int(1) == rand.load(),
#          forth.load() + Int(3) == rand.load(),
#        ),
#        forth.load() - Int(4) == rand.load(),
#      ),
#    ),
#    Seq([ # win
#      Approve(),
#      ]),
#    Seq([ # lose
#        App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) - bet_amount),
#        App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + bet_amount),
#      Approve(),
#      ]),
#    ),
#    Approve(),
#  ])

#  black = Seq([
#    save,
#    App.globalPut(Bytes("x"), gen_number), # update random value
#    rand.store(App.globalGet(Bytes("x")) % Int(36)),
#    If(Or(
#      Or(
#          first.load() - Int(4) == rand.load(),
#          first.load() - Int(2) == rand.load(),
#          first.load() + Int(2) == rand.load(),
#          first.load() + Int(4) == rand.load(),
#      ),
#      Or(
#          second.load() - Int(2) == rand.load(),
#          second.load() + Int(2) == rand.load(),
#          second.load() + Int(4) == rand.load(),
#      ),
#      Or(
#          third.load() - Int(3) == rand.load(),
#          third.load() - Int(1) == rand.load(),
#          third.load() + Int(1) == rand.load(),
#          third.load() + Int(3) == rand.load(),
#      ),
#      Or(
#          forth.load() - Int(2) == rand.load(),
#          forth.load() + Int(2) == rand.load(),
#          forth.load() + Int(4) == rand.load(),
#      ),
#      ),
#      Seq([ # win
#      Approve(),
#        ]),
#      Seq([
#      Approve(),
#        ]),
#      ),
#    Approve(),
#  ])

#  snake_bet = Seq([
#    App.globalPut(Bytes("x"), gen_number), # update random value
#    rand.store(App.globalGet(Bytes("x")) % Int(36)),
#    If(Or(
#      Or(
#        rand.load() == Int(1),
#        rand.load() == Int(5),
#        rand.load() == Int(9),
#        rand.load() == Int(12),
#      ),
#      Or(
#        rand.load() == Int(14),
#        rand.load() == Int(16),
#        rand.load() == Int(19),
#        rand.load() == Int(23),
#      ),
#      Or(
#        rand.load() == Int(27),
#        rand.load() == Int(30),
#        rand.load() == Int(32),
#        rand.load() == Int(34),
#      ),
#    ),
#      Seq([ # win
#      Approve(),
#
#      ]),
#      Seq([ # lose
#      Approve(),
#
#      ]),
#    ),
#    Approve(),
#  ])

  amount = Btoi(Txn.application_args[1])
  buy = Seq([
    Assert(And(
      Gtxn[1].receiver() == App.globalGet(Bytes("admin")),
      Gtxn[1].amount() >= Int(1000000) * amount,
    )),
    App.localPut(Int(0), Bytes("reserve"), App.localGet(Int(0), Bytes("reserve")) + amount),
    App.globalPut(Bytes("reserve"), App.globalGet(Bytes("reserve")) + amount),
    Approve(),
  ])

  # optin
  join = Seq([
    App.localPut(Int(0), Bytes("reserve"), Int(0)),
    Approve(),
  ])

  # closeout
  leave = Seq([
    App.globalPut(Bytes("reserve"), 
        App.globalGet(Bytes("reserve")) + App.localGet(Int(0), Bytes("reserve"))
    ),
    App.localPut(Int(0), Bytes("reserve"), Int(0)),
    Approve(),
  ])

  return Cond(
    [Txn.application_id() == Int(0), on_init],
    [Txn.on_completion() == OnComplete.UpdateApplication, Return(is_admin)],
    [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_admin)],
    [Txn.on_completion() == OnComplete.OptIn, join],
    [Txn.on_completion() == OnComplete.CloseOut, leave],
    [Txn.application_args[0] == Bytes("single_bet"), single_bet],
    [Txn.application_args[0] == Bytes("even"), even],
    [Txn.application_args[0] == Bytes("odd"), odd],
    [Txn.application_args[0] == Bytes("first_dozen"), first_dozen],
    [Txn.application_args[0] == Bytes("second_dozen"), second_dozen],
    [Txn.application_args[0] == Bytes("third_dozen"), third_dozen],
    [Txn.application_args[0] == Bytes("first_four"), first_four],
    [Txn.application_args[0] == Bytes("low"), low],
    [Txn.application_args[0] == Bytes("high"), high],
    [Txn.application_args[0] == Bytes("split"), split],
    [Txn.application_args[0] == Bytes("trio"), trio],
    #[Txn.application_args[0] == Bytes("red"), red],
    #[Txn.application_args[0] == Bytes("black"), black],
    #[Txn.application_args[0] == Bytes("snake"), snake_bet],
    [Txn.application_args[0] == Bytes("buy"), buy],
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
