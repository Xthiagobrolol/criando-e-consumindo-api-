import requests

BASE = "http://127.0.0.1:5000"

# cadastrar
r = requests.post(
    f"{BASE}/produtos/cadastrar",
    data={
        "descricao": "Marca Texto",
        "precocompra": "5.00",
        "precovenda": "10.00"
    },
    allow_redirects=True
)
print("Cadastrar status:", r.status_code)

# listar
r = requests.get(f"{BASE}/produtos/listar")
print("Listar status:", r.status_code)
print(r.text[:400])  # mostra só o começo do HTML

