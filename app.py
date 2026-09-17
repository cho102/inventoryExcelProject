from flask import Flask, render_template, request, send_from_directory
from main import generate_inventory
import os

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
    try: 
        output_file, successful, no_inventory, errors = generate_inventory(product_skus)

        #give excel file to user
        # return send_file(output_file, as_attachment=True)
        return render_template(
            "result.html",
            total = len(product_skus),
            successful=successful,
            no_inventory = no_inventory,
            errors = errors,
            filename = os.path.basename(output_file)
        )
    except Exception as e:
        print(f"Error generating inventory: {e}")
        return render_template("error.html", error=str(e)), 500


@app.route("/download/<filename>")
def download(filename):
    return send_from_directory("output", filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)