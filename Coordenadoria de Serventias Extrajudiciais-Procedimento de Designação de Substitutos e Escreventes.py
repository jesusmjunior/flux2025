{
  "titulo": "Procedimento de Designação de Substitutos e Escreventes",
  "setor": "Coordenadoria de Serventias Extrajudiciais",
  "base_legal": "Art. 270 do Código de Normas da COGEX/MA",
  "etapas": [
    {
      "id": "start",
      "tipo": "inicio",
      "texto": "Início"
    },
    {
      "id": "t1",
      "tipo": "tarefa",
      "texto": "1. Envio do Ofício\n- Delegatário titular ou interino\n- Via malote digital ou e-mail\n- Para Coordenação das Serventias Extrajudiciais"
    },
    {
      "id": "t2",
      "tipo": "tarefa",
      "texto": "2. Abertura do Processo\n- Receber documento no Malote Digital\n- Cadastrar requisição no DIGIDOC"
    },
    {
      "id": "t3",
      "tipo": "tarefa",
      "texto": "3. Distribuição do Processo\n- Aprovar requisição\n- Distribuir para servidor conforme ordem\n- Consultar tabela no drive do e-mail da Coordenação"
    },
    {
      "id": "t4",
      "tipo": "verificacao",
      "texto": "4. Análise de Documentação\n- Analisar documentos recebidos\n- Verificar sistema AUDITUS\n- Confirmar Certidões do Art. 270, II e III do CNCGJMA"
    },
    {
      "id": "d1",
      "tipo": "verificacao",
      "texto": "5. Documentação Completa?\n- Verificar presença das certidões exigidas"
    },
    {
      "id": "t5",
      "tipo": "tarefa",
      "texto": "6. Solicitação de Complementação\n- Oficiar o delegatário\n- Solicitar complementação no AUDITUS\n- Aguardar resposta"
    },
    {
      "id": "t6",
      "tipo": "verificacao",
      "texto": "7. Verificação da Regularização\n- Confirmar inclusão das certidões\n- Validar documentação complementar"
    },
    {
      "id": "t7",
      "tipo": "tarefa",
      "texto": "8. Arquivamento do Processo\n- Finalizar análise\n- Registrar conclusão\n- Arquivar documentação"
    },
    {
      "id": "end",
      "tipo": "fim",
      "texto": "Encerramento"
    }
  ],
  "conexoes": [
    ["start", "t1"],
    ["t1", "t2"],
    ["t2", "t3"],
    ["t3", "t4"],
    ["t4", "d1"],
    ["d1", "t5"],
    ["d1", "t7"],
    ["t5", "t6"],
    ["t6", "t7"],
    ["t7", "end"]
  ]
}
