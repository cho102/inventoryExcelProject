from flask import Flask, render_template, request

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
    product_skus = [
        sku.strip()
        for sku in product_input.splitlines()
        if sku.strip()
    ]

    print("Product SKUs:")
    print(product_skus)

    return "Product list received!"

if __name__ == "__main__":
    app.run(debug=True)