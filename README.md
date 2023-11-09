# Trabalho-de-conclusao-de-curso
Aqui está descrito meu TCC para o curso de Tecnologia em Sistemas para Internet

Este trabalho é uma implementação de um aplicativo de cadastro e listagem de produtos, assemelhando-se a um bot de vendas. O objetivo principal é fornecer uma alternativa a aplicativos que realizam as mesmas funcionalidades, porém de forma gratuita e acessível a todos. Além disso, abrange a utilização de APIs e visualização de resultados através de outras aplicações, em especial o Discord e Telegram. Para isso, apresenta-se um protótipo inicial de interface na plataforma Figma, com o objetivo de definir categorias, campos e também os caminhos a serem preenchidos pelo usuário. Por fim, implementou-se alguns testes iniciais, e foi desenvolvido na linguagem de programação Python.


Configurações

→ Deve-se criar os bots na plataforma Discord e Telegram.
   ► Telegram: basta pesquisar por @BotFather e digitar o comando /newbot, a partir disso é só seguir o passo a passo que o aplicativo orienta, é importante salvar o TOKEN disponibilizado após a criação do bot.
   ► Discord: precisa acessar o portal do desenvolvedor (https://discord.com/developers/applications), após esse processo seleciona a opção de "new application" e escolhe a opção bot. Após criar o bot e selecionar todas as permissões que ele terá basta adicionar a um servidor existente. Igual ao Telegram é essencial copiar o TOKEN ou URL disponibilizado ao final do processo.

→ É preciso criar também a estrutura do banco de dados, as tabelas e os campos
  ► O banco de dados utilizado no projeto foi o PostgreSQL
  ► A estrutura do banco de dados foi realizado da seguinte maneira: 
     • Tabela: data
                 └ description (text)
                 └ observation (text)
                 └ code (text)
                 └ price (text)
                 └ quantity (text)
                 └ category (text)
                 └ id (integer, primary key, autoincremento)
                 └ photo (bytea)

  • Tabela: users
               └ username (text)
               └ password (text)
     
→ Após a criação dos bots e do banco de dados será necessário a criação da aplicação Flask
   ► Recomendo assistir a esse pequeno vídeo que ensina a criar uma aplicação simples, mas totalmente funcional: https://youtu.be/6M3LzGmIAso?si=xukCL-QwZI_4P3CB

→ Seguindo esses passo você terá o aplicativo já pronto, faltando apenas substituir os TOKENS disponibilizados pelo Discord e Telegram no código, está escrito como "SEU_TOKEN"
