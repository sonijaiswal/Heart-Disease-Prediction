from django.shortcuts import render
from django.http import FileResponse
from fpdf import FPDF

from users.models import Heart


def index(request):
    context = {}
    return render(request, "app/index.html", context=context)


def report(request):

    profile = request.user.profile
    heart = Heart.objects.get(owner=profile)

    print(heart.created)
    print(profile.user)

    sales = [

        {"item": "Name", "amount": str(profile.user)},
        {"item": "Age", "amount": str(heart.age)},
        {"item": "Sex", "amount": str(heart.get_sex_display())},
        {"item": "CP", "amount": str(heart.get_cp_display())},
        {"item": "trestbps", "amount": str(heart.trestbps)},
        {"item": "chol", "amount": str(heart.chol)},
        {"item": "fbs", "amount": str(heart.get_fbs_display())},
        {"item": "restecg", "amount": str(heart.get_restecg_display())},
        {"item": "thalach", "amount": str(heart.thalach)},
        {"item": "exang", "amount": str(heart.get_exang_display())},
        {"item": "oldpeak", "amount": str(heart.oldpeak)},
        {"item": "slope", "amount": str(heart.get_slope_display())},
        {"item": "ca", "amount": str(heart.ca)},
        {"item": "thal", "amount": str(heart.get_thal_display())},
    ]

    conditions = [

        {"item": "KNN ", "amount": str(heart.result1)},
        {"item": "Logistic Regression ", "amount": str(heart.result2)},
        {"item": "Random Forest Regression ", "amount": str(heart.result3)},

    ]

    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Medical Details',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Features'.ljust(30)} {'Value'.rjust(20)}", 0, 1)
    pdf.line(10, 30, 150, 30)
    pdf.line(10, 38, 150, 38)
    for line in sales:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    
    pdf.set_font('courier', 'B', 16)
    pdf.cell(40, 10, 'Predictions Using Different Algorithms',0,1)
    pdf.cell(40, 10, '',0,1)
    pdf.set_font('courier', '', 12)
    pdf.cell(200, 8, f"{'Algorithm'.ljust(30)} {'Result'.rjust(20)}", 0, 1)
    pdf.line(10, 170, 150, 170)
    pdf.line(10, 178, 150, 178)
    for line in conditions:
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {line['amount'].rjust(20)}", 0, 1)
    

    pdf.output('app/reports/report.pdf', 'F')

    return FileResponse(open('app/reports/report.pdf', 'rb'), as_attachment=False, content_type='application/pdf')
