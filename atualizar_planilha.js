function doPost(e) {
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var pipeId = "304524179";  // Substitua pelo ID do seu Pipe
  
    var url = 'https://api.pipefy.com/graphql';
    
    const graphql = JSON.stringify({
      query: `
        query {
          pipe(id: ${pipeId}) {
            phases {
              name
              cards {
                edges {
                  node {
                    id
                    title
                    fields {
                      field {
                        id
                        label
                      }
                      value
                    }
                  }
                }
              }
            }
          }
        }
      `,
    });
  
    var params = {
      method: 'POST',
      payload: graphql,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': "Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJQaXBlZnkiLCJpYXQiOjE3MjE4ODc1NTMsImp0aSI6IjY3MWQ2YjE0LThlNGEtNGM1OC1hODJjLWNlM2I2ZGViMjk5ZSIsInN1YiI6MzA1MDE0NTQwLCJ1c2VyIjp7ImlkIjozMDUwMTQ1NDAsImVtYWlsIjoiZmVsaXBlLnBhcGFuaUB1ZnBlLmJyIn19.qQ7jeBinfMVCkW7E8Ut0Rgz1KG0pIPWkxaA53pJ8kpTIimUH2QoCoESJIKVt3zcZQjyVNF5b_GDK0jhurbBgWQ"
      },
    };
  
    try {
      Logger.log('Enviando solicitação para Pipefy...');
      var response = UrlFetchApp.fetch(url, params);
      Logger.log('Resposta recebida: ' + response.getContentText());
  
      var data = JSON.parse(response.getContentText());
      Logger.log('Dados processados: ' + JSON.stringify(data));
  
      // Limpa a planilha
      sheet.clear();
  
      // Adiciona cabeçalhos
      sheet.appendRow(['ID', 'Nome da Atividade', 'Descrição da Atividade', 'Tipo da Atividade', 'Duração da Atividade', 'Data da Atividade']);
  
      // IDs dos campos específicos
      var fieldIdNome = 'nome_da_atividade_1';
      var fieldIdDescricao = 'descri_o_da_atividade_1';
      var fieldIdTipo = 'sele_o_de_lista';
      var fieldIdDuracao = 'dura_o_da_atividade_1';
      var fieldIdData = 'data_proposta_1';
  
      // Itera sobre todas as fases e seus respectivos cards
      data.data.pipe.phases.forEach(phase => {
        phase.cards.edges.forEach(edge => {
          var card = edge.node;
          var id = card.id;
          var nome = "";
          var descricao = "";
          var tipo = "";
          var duracao = "";
          var dataAtividade = "";
  
          card.fields.forEach(function(field) {
            if (field.field.id === fieldIdNome) {
              nome = field.value;
            } else if (field.field.id === fieldIdDescricao) {
              descricao = field.value;
            } else if (field.field.id === fieldIdTipo) {
              tipo = field.value;
            } else if (field.field.id === fieldIdDuracao) {
              duracao = field.value;
            } else if (field.field.id === fieldIdData) {
              dataAtividade = field.value;
            }
          });
  
          Logger.log('Adicionando card: ' + [id, nome, descricao, tipo, duracao, dataAtividade]);
  
          // Adiciona os dados do card na planilha
          sheet.appendRow([id, nome, descricao, tipo, duracao, dataAtividade]);
        });
      });
    } catch (error) {
      Logger.log('Erro ao buscar dados do Pipefy: ' + error.message);
    }
  }
  