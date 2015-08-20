# Py-Pagseguro

O py-pagseguro é uma pequena lib construída para facilitar a integraçaõ de assinaturas manuais no [PagSeguro](pagseguro.uol.com.br).

O Py-Pagseguro depende:
* arrow
* BeautifulSoup4
* requests
* Unidecode

## Instalando

Use o seguinte comando para instalar:

`pip install py-pagseguro`

## Começando

Iniciando uma compra de produto pontual

```python
from py-pagseguro import PagSeguroTransaction

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

Para iniciar uma assinatura no pagseguro use:


```python
from py-pagseguro import PagSeguroSignature

# Abaixo crie um objecto de transação
transaction = PagSeguroSignature('sua_token', 'seu_email', 'nome da asisnatura', 'descricao', price=3.14, reference='Referencia de seu sistema')

# Caso sua assinatura não seja mensal passe também o argumento period com uma das opções:
# WEEKLY, BIMONTHLY, TRIMONTHLY, SEMIANNUALLY, YEARLY

# Url para você redirecionar seu comprador para o PagSeguro
url = transaction.get_checkout_url()
```

Após qualquer uma das ações acima o pagseguro irá processar e lhe enviar(POST) uma notificação.
A notificação do pagseguro é um post contendo `notificationCode` e `notificationType`.

O `notificationType` pode ser Transaction ou Preapproval, para vendas simples e assinaturas respectivamente.

Caso seja uma Transaction use:

```python
from py-pagseguro import PagSeguroNotificationHandler

# Instancie o handler passando o código recebido pelo pagseguro.
handler = PagSeguroNotificationHandler('sua_token', 'seu_email', 'notificationCode')

# Use o get_notification_response para obter as informações refentes a essa transação
response = handler.get_notification_response()

# Status da transação
response.status  # 'Paga'
```


Caso seja uma assinatura use:


```python
from py-pagseguro import PagSeguroNotificationSignatureHandler

# Instancie o handler passando o código recebido pelo pagseguro.
handler = PagSeguroNotificationSignatureHandler('sua_token', 'seu_email', 'notificationCode')

# Use o get_notification_response para obter as informações refentes a essa transação
response = handler.get_notification_response()

if response.status.lower() == 'active':  # 3 estados possíveis: INITIATED, PENDING e ACTIVE
    # Faça a cobrança, veja abaixo usando o response.code
    # Para mais de uma cobrança salve o response.code em seu banco de dados
```

Uma vez que sua assinatura já está ativa podemos começar a fazer as cobranças de acordo com a periodicidade acordada:


```python
from py-pagseguro import PagSeguroSignatureCharger

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
