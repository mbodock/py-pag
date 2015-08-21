# Py-Pag

O py-pag é uma pequena lib construída para facilitar a integração de assinaturas manuais no [PagSeguro](pagseguro.uol.com.br).

O Py-Pag depende:

* arrow
* BeautifulSoup4
* requests
* Unidecode

> Todos instalados automaticamente.


## Instalando

Use o seguinte comando para instalar:

`pip install py_pag`


## Começando

Abaixo a descrição de algumas classes e suas funções


### Transação simples

Iniciando uma compra de produto pontual

```python
from py_pag import PagSeguroTransaction

# Abaixo crie um objecto de transação
transaction = PagSeguroTransaction('sua_token', 'seu_email', reference='Referencia de seu sistema')

# Crie também o item a ser cobrado, um simples dicionário
item = {
    'id': 'id',  # Nome do item no pagseguro
    'description': 'item description',  # Descrição do item
    'quantity': 1,  # Quantidade de itens vendidos
    'amount': 3.14,  # Valor do item
}

# Define qual o item da transação
transaction.set_item(item)

# Url para você redirecionar seu comprador para o PagSeguro
url = transaction.get_checkout_url()
```


### Criando uma assinatura

Para iniciar uma assinatura no pagseguro use:


```python
from py_pag import PagSeguroSignature

# Abaixo crie um objecto de transação
transaction = PagSeguroSignature('sua_token', 'seu_email', 'nome da asisnatura', 'descricao', price=3.14, reference='Referencia de seu sistema')

# Caso sua assinatura não seja mensal passe também o argumento period com uma das opções:
# WEEKLY, BIMONTHLY, TRIMONTHLY, SEMIANNUALLY, YEARLY

# Url para você redirecionar seu comprador para o PagSeguro
url = transaction.get_checkout_url()
```


### Recebendo notificaçoes

Após qualquer uma das ações acima o pagseguro irá processar e lhe enviar(POST) uma notificação.
A notificação do pagseguro é um post contendo `notificationCode` e `notificationType`.

O `notificationType` pode ser Transaction ou Preapproval, para vendas simples e assinaturas respectivamente.


##### Notificação de transição

Caso seja uma Transaction use:

```python
from py_pag import PagSeguroNotificationHandler

# Instancie o handler passando o código recebido pelo pagseguro.
handler = PagSeguroNotificationHandler('sua_token', 'seu_email', 'notificationCode')

# Use o get_notification_response para obter as informações refentes a essa transação
response = handler.get_notification_response()

# Status da transação
response.status  # 'Paga'
```


##### Notificação de assinatura

Caso seja uma assinatura use:

```python
from py_pag import PagSeguroNotificationSignatureHandler

# Instancie o handler passando o código recebido pelo pagseguro.
handler = PagSeguroNotificationSignatureHandler('sua_token', 'seu_email', 'notificationCode')

# Use o get_notification_response para obter as informações refentes a essa transação
response = handler.get_notification_response()

if response.status.lower() == 'active':  # 3 estados possíveis: INITIATED, PENDING e ACTIVE
    # Faça a cobrança, veja abaixo usando o response.code
    # Para mais de uma cobrança salve o response.code em seu banco de dados
```


### Efetuando cobranças

Uma vez que sua assinatura já está ativa podemos começar a fazer as cobranças de acordo com a periodicidade acordada:


```python
from py_pag import PagSeguroSignatureCharger

# Itens a serem cobrados
items = [{
    'id': 'nome',  # Nome do item no pagseguro
    'description': 'item description',  # Descrição do item
    'quantity': 1,  # Quantidade de itens vendidos
    'amount': 3.14,  # Valor do item
}]

# Atenção que o valor cobrado DEVE ser exatamento o mesmo da criação da assinatura
charger = PagSeguroSignatureCharger('sua_token', 'seu_email', 'codigo_da_assinatura', items)

# O charge() irá cobrar ou levantar uma exception com a mensagem do pagseguro
# O retorno consiste do códgio da operação e data da mesma.
# Após uma cobrança bem sucedida o pagseguro irá lhe enviar uma nova notificação indicando que algo foi pago
# Esta notificação será uma transação normal.
codigo_da_operacao, data = charger.charge()
```


## Executando os testes

* Clone o repositório.
* Entre na pasta raiz e instale as dependências de dev: `pip install -r requirements-dev.txt`.
* Para rodar os testes: `py.test`.
* Para obter o coverage: `py.test --cov`


## Implementações futuras

* Alterar PagSeguroTransaction para trabalhar com multiplos produtos.
* Criar documentação sobre url_redirect e outras opções.
