from flask import Flask
from flask import render_template, request, redirect

app = Flask(__name__)

class Loan:
    def __init__(self, loanAmount, numberOfYears, annualRate):
        #properties
        self.loanAmount = loanAmount
        self.annualRate = annualRate
        self.numberOfPmts = numberOfYears * 12 #months in a year
        self.periodicIntRate = annualRate / 12 #months in a year
        self.discountFactor= 0
        self.loanPayment = 0

    #methods
    def setLoanPayment(self):
        self.discountFactor = (((1 + self.periodicIntRate)**self.numberOfPmts) -1) / (self.periodicIntRate * (1+ self.periodicIntRate) ** self.numberOfPmts)
        self.loanPayment = self.loanAmount / self.discountFactor

    def getLoanPayment(self):
        return self.loanPayment

##########

@app.route('/')
def index():
    return render_template('index.html', display="", pageTitle='My Calculator')

@app.route('/calc', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        form = request.form
        loanAmount = float(form['loanAmt'])
        numberOfYears = float(form['years'])
        annualRate = float(form['interest'])

        #loan = None

        loan = Loan(loanAmount, numberOfYears, annualRate)
        loan.setLoanPayment()
        pmt = loan.getLoanPayment()   #<--- I was missing the parenthesis.

        result = "Your monthly payment is: ${0:6.2f}".format (pmt)
        return render_template('index.html', display=result, pageTitle='My Calculator')

    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)