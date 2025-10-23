Para testar:
# Dados que serão enviados (PowerShell usa @{} para criar objetos)
$body = @{ 
    nome = "Carlos Souza"; 
    cargo = "Designer UX"; 
    setor = "Design"; 
    salario = 6000.00; 
    tipo = "CLT" 
}

# Converte o objeto PowerShell em uma string JSON e envia a requisição POST
Invoke-RestMethod -Uri http://127.0.0.1:5000/pessoas `
    -Method Post `
    -ContentType "application/json" `
    -Body (ConvertTo-Json $body)



    ou
    curl -X POST -H "Content-Type: application/json" -d '{"nome": "Mariana Alves", "cargo": "RH Generalista", "setor": "Recursos Humanos", "salario": 3800.00, "tipo": "PJ"}' http://127.0.0.1:5000/pessoas

    