from flask import Flask, render_template, request, send_file
from main import generate_inventory

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    product_input=request.form["product_list"]

    #replace commas with newlines
    product_input = product_input.replace(",", "\n")

    #create list of SKUs
    product_skus = list(dict.fromkeys(
        sku.strip().upper()
        for sku in product_input.splitlines()
        if sku.strip()
    )) 

    if not product_skus:
        return "Please enter at least one product number"
    
    print("Product SKUs:")
    print(product_skus)

    #run existing excel generator
    output_file = generate_inventory(product_skus)

    #give excel file to user
    return send_file(output_file, as_attachment=True)

    return "Product list received!"

if __name__ == "__main__":
    app.run(debug=True)