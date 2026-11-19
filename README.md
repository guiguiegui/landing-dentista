# Template de site para consultório odontológico

Página única, estática, rápida no celular. Um arquivo de configuração por cliente.

## Gerar o site de exemplo

```bash
python3 build.py
```

Saída em `dist/index.html`. Para ver: `cd dist && python3 -m http.server 8765` e abra http://127.0.0.1:8765.

## Novo cliente (cerca de 1 hora)

1. Copie `config.json` para `clientes/nome-do-consultorio.json`.
2. Troque todos os dados e ponha `"modo_exemplo": false` (tira o aviso de demonstração).
3. `python3 build.py clientes/nome-do-consultorio.json` gera `dist/nome-do-consultorio/index.html`.
4. Publique a pasta em hospedagem estática (Cloudflare Pages, Netlify ou GitHub Pages) e aponte o domínio.

Campos obrigatórios: nome, slogan, descricao_curta, responsavel, telefone_exibicao, whatsapp
(só dígitos, `55` + DDD + número), endereco, cidade, estado, servicos, horarios, sobre,
diferenciais, cor_principal, cor_escura. O build avisa o que faltar.

## Antes de entregar

- Confirme telefone, WhatsApp, endereço e CRO com o dentista. Dado errado vira problema seu.
- Teste o botão de WhatsApp no celular e o mapa.
- Fotos reais só com autorização dele. Hoje o template usa uma ilustração, sem fotos.
- Peça o nome do consultório exatamente como aparece no Google, para o mapa achar o lugar.

## Limites conhecidos

- Sem formulário de contato (o canal é o WhatsApp).
- Sem galeria de fotos nem depoimentos ainda.
- Nada foi testado em produção nem com um cliente real.
