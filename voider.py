from flask import Flask, request, render_template

from base64 import b64encode
from io import BytesIO

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

from os import path

script_path = path.dirname(path.realpath(__file__))

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def root():
    name = ""
    address1 = ""
    address2 = ""
    city = ""
    state = ""
    zipcode = ""
    bank_name = ""
    check_number = ""
    account_number = ""
    aba_number = ""

    if request.method == "POST":
        name = request.form['name']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        bank_name = request.form['bank_name']
        check_number = request.form['check_number']
        account_number = request.form['account_number']
        aba_number = request.form['aba_number']

    image_data = draw_check(name, address1, address2, city, state,
                            zipcode, bank_name, check_number, account_number, aba_number)

    return render_template(
        "root.html",
        name=name,
        address1=address1,
        address2=address2,
        city=city,
        state=state,
        zipcode=zipcode,
        bank_name=bank_name,
        check_number=check_number,
        account_number=account_number,
        aba_number=aba_number,
        image_data=image_data
    )


def draw_check(name, address1, address2, city, state, zipcode, bank_name, check_number, account_number, aba_number):
    # Open blank check image
    image = Image.open(f"{script_path}/images/blankcheck.jpg")

    # Open fonts
    text_font = ImageFont.truetype(
        f"{script_path}/fonts/OpenSans-Regular.ttf", 14)
    void_font = ImageFont.truetype(
        f"{script_path}/fonts/HolliesBigInk-Regular.ttf", 180)
    micr_font = ImageFont.truetype(
        f"{script_path}/fonts/micrenc.ttf", 24)

    draw = ImageDraw.Draw(image)

    left_x_margin = 30
    right_x_margin = 840

    draw.text((680, 100), "DATE", font=text_font, fill="black")
    draw.line((720, 115, right_x_margin, 115), fill="black")

    draw.text((780, 180), "DOLLARS", font=text_font, fill="black")
    draw.line((left_x_margin, 195, 770, 195), fill="black")

    draw.text((left_x_margin, 130), "PAY TO THE\nORDER OF",
              font=text_font, fill="black")
    draw.line((110, 165, 650, 165), fill="black")

    draw.text((680, 150), "$", font=text_font, fill="black")
    draw.line((695, 165, right_x_margin, 165), fill="black")

    draw.text((left_x_margin, 290), "MEMO", font=text_font, fill="black")
    draw.line((80, 305, 400, 305), fill="black")

    # signature line
    draw.line((450, 305, right_x_margin, 305), fill="black")

    account_owner = name
    if address1 != "":
        account_owner = account_owner + f"\n{address1}"

    if address2 != "":
        account_owner = account_owner + f"\n{address2}"

    if city != "" and state != "" and zipcode != "":
        account_owner = account_owner + f"\n{city}, {state} {zipcode}"

    draw.text((left_x_margin, 30), account_owner, font=text_font, fill="black")

    draw.text((350, 30), bank_name, font=text_font, fill="black")

    draw.text((790, 30), check_number, font=text_font, fill="black")

    draw.text((220, 110), "VOID", font=void_font, fill="black")

    micr = f"C{check_number}C    A{aba_number}A    {account_number}C"
    draw.text((120, 350), micr, font=micr_font, fill="black")

    image_io = BytesIO()
    image.save(image_io, 'PNG')

    # this won't be saved to disk, pass it back as base64 data to be injected as the
    # src of an <img> tag
    return 'data:image/png;base64,' + b64encode(image_io.getvalue()).decode('ascii')
