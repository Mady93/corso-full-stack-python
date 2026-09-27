from modelli.configurazione_team import ConfigurazioneTeam


def test_valore_default():
    config = ConfigurazioneTeam()

    assert config.limite_ticket_dev == 3


def test_valore_personalizzato():
    config = ConfigurazioneTeam(5)

    assert config.limite_ticket_dev == 5


def test_modifica_limite():
    config = ConfigurazioneTeam()

    config.limite_ticket_dev = 10

    assert config.limite_ticket_dev == 10