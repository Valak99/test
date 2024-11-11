from flask import Flask, render_template, request
import difflib
import re

app = Flask(__name__)


def compare_code(before_code: str, after_code: str):
    # Split the code into lines
    before_lines = before_code.splitlines(keepends=True)
    after_lines = after_code.splitlines(keepends=True)

    # Use difflib to generate the HTML diff output
    differ = difflib.HtmlDiff()
    html_diff = differ.make_table(
        before_lines, after_lines, fromdesc="Before", todesc="After", context=False, numlines=0
    )

    # Replace the default diff_add and diff_sub classes with custom classes
    html_diff = re.sub(r'class="diff_add"', 'class="diff-add"', html_diff)
    html_diff = re.sub(r'class="diff_sub"', 'class="diff-del"', html_diff)

    return html_diff


@app.route("/", methods=["GET"])
def index():
    return render_template("code_comparison.html", comparison_html=None)


@app.route("/compare", methods=["POST"])
def compare():
    before_code = request.form["before_code"]
    after_code = request.form["after_code"]
    comparison_html = compare_code(before_code, after_code)

    return render_template("code_comparison.html", comparison_html=comparison_html)


if __name__ == "__main__":
    app.run(debug=True)
