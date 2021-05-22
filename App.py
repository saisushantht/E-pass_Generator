import requests
from flask import Flask, render_template, request
from twilio.rest import Client
from datetime import date

account_sid = 'AC327c7b2e234879320a2882900859c99b'
auth_token = '01093eac02b55a81e00ab80899ef6d8b'
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('test_page.html')


@app.route('/user_registration_dtls', methods=['GET', 'POST'])
def login_registration_dtls():
   # individual_type = request.form['type']
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    date_tr = request.form['travel']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    no_t = request.form['no_of']
    veh_no = request.form['vehno']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    print("+91"+phoneNumber)
    num="+91"+phoneNumber
    if travel_pass < 30 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to=num,
                               from_="+12564725315",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " to " +
                                    destination_dt + " " + "Has " + " " + status + " On " + " with "+veh_no+" for" + no_t +" people on "+ date_tr)
        return render_template('user_registration_dtls.html', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id,vehno=veh_no,no_tr=no_t,travel_date=date_tr)
    else:
        status = 'NOT CONFIRMED'
        client.messages.create(to=num,
                               from_="+12564725315",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " +
                                    source_dt + " to " + destination_dt + " " + "is " + " " + status + " On " + date_tr+" " +
                                    ", Apply later")
        return render_template('user_registration_dtls.html', firstname=first_name, lastname=last_name,
                               status="confirmed", email=email_id,vehno=veh_no,no_tr=no_t,travel_date=date_tr)


if __name__ == "__main__":
    app.run(port=9001, debug=True)