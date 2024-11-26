# iFood Gestor de Pedidos - Automação

Automação para login no iFood Gestor de Pedidos utilizando Selenium WebDriver.

## Funcionalidades

- Login automatizado no iFood Gestor de Pedidos
- Suporte a verificação em duas etapas
- Gestão segura de credenciais via arquivo .env

## Requisitos

- Python 3.x
- Google Chrome
- ChromeDriver (instalado automaticamente via webdriver-manager)

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_SEU_REPOSITORIO]
cd gestor_pedidos
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as credenciais:
- Crie um arquivo `.env` na raiz do projeto
- Adicione suas credenciais:
```
IFOOD_EMAIL=seu_email@exemplo.com
```

## Estrutura do Projeto

```
gestor_pedidos/
├── config/
│   ├── __init__.py
│   └── config.py
├── src/
│   ├── __init__.py
│   ├── locators/
│   │   └── login_locators.py
│   ├── pages/
│   │   └── login_page.py
│   └── utils/
│       └── driver_factory.py
├── tests/
├── .env
├── .gitignore
├── open_browser3.py
└── requirements.txt
```

## Uso

Execute o script principal:
```bash
python open_browser3.py
```

O script irá:
1. Abrir o Chrome
2. Navegar até a página de login
3. Preencher o email
4. Lidar com verificação em duas etapas (se necessário)

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Segurança

- Nunca compartilhe seu arquivo `.env`
- Não commite credenciais no código
- Mantenha suas dependências atualizadas
