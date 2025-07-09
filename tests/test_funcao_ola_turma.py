from app.funcao import funcao_ola_turma

class TestSaudacao:
  def test_funcao_ola_turma(self):
    response = funcao_ola_turma()
    assert response == 'ola turma'