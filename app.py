from flask import Flask, render_template, jsonify, request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as p
import uuid
import os
import time
import threading
import sympy as sp
from sympy.parsing.sympy_parser import (
    standard_transformations,
    implicit_multiplication_application
)
transformations = standard_transformations + (
    implicit_multiplication_application,
)


app = Flask(__name__)



def dfl(filepath, delay=80):
    def delete():
        time.sleep(delay)

        if os.path.exists(filepath):
            os.remove(filepath)

    threading.Thread(target=delete, daemon=True).start()


@app.route("/")
def home():
    return render_template("test.html")


@app.route("/u2", methods=["POST"])
def u2():

    data = request.get_json()

    number1 = str(data["number1"])
    number2 = str(data["number2"])
    number3 = str(data["number3"])

    ui = number1.replace("^", "**")
    ui2 = number2.replace("^", "**")
    ui3 = number3.replace("^", "**")
    ui = sp.parse_expr(ui, transformations=transformations)
    ui2 = sp.parse_expr(ui2, transformations=transformations)       
    ui3 = sp.parse_expr(ui3, transformations=transformations)
    

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join("javascript/static", filename)

    ui = sp.sympify(ui)
    ui2 = sp.sympify(ui2)
    ui3 = sp.sympify(ui3)

    f = (ui + ui2 + ui3)**2
    r = sp.expand((ui + ui2 + ui3)**2)

    f = sp.latex(f)
    r = sp.latex(r)

    p.figure(figsize=(10, 5))
    p.text(0.1 , 0.7 , r"$(a+b+c)²$" , fontsize=20)
    p.text(0.1 , 0.5 , r'${}$'.format(f) , fontsize=20)
    p.text(0.1 , 0.3 , r'${}$'.format(r) , fontsize=20)
    p.axis('off')
    p.savefig(filepath, dpi=150, bbox_inches="tight")
    p.close()

    dfl(filepath, 80)

    return jsonify({
        "success": True,
        "image": f"/static/{filename}"
})

@app.route("/u1", methods=["POST"])
def u1():
    data = request.get_json()
    
    number4 = str(data["number4"])
    number5 = str(data["number5"])

    filename = f"{uuid.uuid4()}.png"
    filepath = os.path.join("javascript/static", filename)

    ui = number4.replace("^", "**")
    ui2 = number5.replace("^", "**")
    ui = sp.parse_expr(ui, transformations=transformations)
    ui2 = sp.parse_expr(ui2, transformations=transformations)
    ui = sp.sympify(ui)
    ui2 = sp.sympify(ui2)
    
    f = (ui + ui2)**2
    r = sp.expand((ui + ui2)**2)

    f = sp.latex(f)
    r = sp.latex(r)
    
    p.figure(figsize=(10, 5))
    p.text(0.1 , 0.7 , r"$(a+b)²$" , fontsize=20)
    p.text(0.1 , 0.5 , r'${}$'.format(f) , fontsize=20)
    p.text(0.1 , 0.3 , r'${}$'.format(r) , fontsize=20)
    p.axis('off')
    p.savefig(filepath, dpi=150, bbox_inches="tight")
    p.close()

    dfl(filepath, 80)

    return jsonify({
        "success" : True,
        "image" : f"/static/{filename}"
    })


    

