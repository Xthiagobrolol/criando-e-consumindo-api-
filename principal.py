from flask import Flask, request, render_template, redirect, url_for
from datetime import date
import sqlite3
from sqlite3 import Error
import os

app = Flask(__name__)
DB_PATH = os.path.join('database', 'db-produtos.db')

def get_conn():
    return sqlite3.connect(DB_PATH)


# 1. Cadastro de produtos 
@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    mensagem = ''
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        precocompra = request.form.get('precocompra', '').strip()
        precovenda = request.form.get('precovenda', '').strip()
        datacriacao = date.today().isoformat()

        if descricao and precocompra and precovenda:
            try:
                conn = get_conn()
                sql = '''INSERT INTO produtos(descricao, precocompra, precovenda, datacriacao)
                         VALUES(?,?,?,?)'''
                cur = conn.cursor()
                cur.execute(sql, (descricao, float(precocompra), float(precovenda), datacriacao))
                conn.commit()
                mensagem = 'Sucesso - cadastrado'
                return redirect(url_for('listar'))
            except Error as e:
                mensagem = f'Erro ao cadastrar: {e}'
            finally:
                conn.close()
        else:
            mensagem = 'Preencha todos os campos.'
    return render_template('cadastrar.html', mensagem=mensagem)


# 2. Listar produtos
@app.route('/produtos/listar', methods=['GET'])
def listar():
    registros = []
    try:
        conn = get_conn()
        sql = 'SELECT idproduto, descricao, precocompra, precovenda, datacriacao FROM produtos ORDER BY idproduto'
        cur = conn.cursor()
        cur.execute(sql)
        registros = cur.fetchall()
    except Error as e:
        print("Erro ao listar:", e)
    finally:
        conn.close()
    return render_template('listar.html', regs=registros)


# 3. Excluir um produto
@app.route('/produtos/excluir/<int:idproduto>', methods=['GET'])
def excluir(idproduto):
    msg = ''
    try:
        conn = get_conn()
        sql = "DELETE FROM produtos WHERE idproduto = ?"
        cur = conn.cursor()
        cur.execute(sql, (idproduto,))
        conn.commit()
        msg = 'Produto excluído'
    except Error as e:
        msg = f'Erro ao excluir: {e}'
    finally:
        conn.close()
    return redirect(url_for('listar'))


# 4. Alterar um produto
@app.route('/produtos/alterar/<int:idproduto>', methods=['GET', 'POST'])
def alterar(idproduto):
    if request.method == 'POST':
        descricao = request.form.get('descricao', '').strip()
        precocompra = request.form.get('precocompra', '').strip()
        precovenda = request.form.get('precovenda', '').strip()

        if descricao and precocompra and precovenda:
            try:
                conn = get_conn()
                sql = """UPDATE produtos
                         SET descricao = ?, precocompra = ?, precovenda = ?
                         WHERE idproduto = ?"""
                cur = conn.cursor()
                cur.execute(sql, (descricao, float(precocompra), float(precovenda), idproduto))
                conn.commit()
                return redirect(url_for('listar'))
            except Error as e:
                print("Erro ao atualizar:", e)
            finally:
                conn.close()
    # buscar registro e mostrar formulário
    registro = None
    try:
        conn = get_conn()
        sql = "SELECT idproduto, descricao, precocompra, precovenda, datacriacao FROM produtos WHERE idproduto = ?"
        cur = conn.cursor()
        cur.execute(sql, (idproduto,))
        registro = cur.fetchone()
    except Error as e:
        print("Erro ao buscar registro:", e)
    finally:
        conn.close()
    if not registro:
        return render_template('404.html'), 404
    return render_template('alterar.html', reg=registro)


# Rota de Erro 404
@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    # cria pasta database 
    os.makedirs('database', exist_ok=True)
    app.run(debug=True)