class SR_to_SS(object):
    MovendoPara = 5000
    PosicaoAtual = 5001
    ValidaCaca = 5002
    ObstaculoEncontrado = 5003

class SS_to_SS(object):
    MovendoPara = 6000
    PosicaoAtual = 6001
    ValidaCaca = 6002
    ObstaculoEncontrado = 6003

    ValidaCaca_resp = 6004

class SS_to_SR(object):
    MovendoPara = 4000
    PosicaoAtual = 4001
    ValidaCaca = 4002
    ObstaculoEncontrado = 4003

class SS_to_SA(object):
    MovendoPara = 1000
    PosicaoAtual = 1001
    ValidaCaca = 1002
    ObstaculoEncontrado = 1003

    SolicitaID_Resp = 2000
    SolicitaHistorico_RESP = 2002


    SolicitaStatus_RESP = 2003

class SA_to_SS(object):
    """ENUM de mensagens SS para SR"""
    CadastraRobo = 1000
    SolicitaID = 1001
    SolicitaHistorico = 1002
    SolicitaStatus = 1003

    NovoJogo = 1100
    Pausa = 1101
    Continua = 1102
    FimJogo = 1103

    AtualizaMapa = 1200

    ValidacaoCaca = 2000