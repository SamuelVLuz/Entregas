# views.py
from django.shortcuts import render, redirect
from rotas.forms import PDFUploadForm
from django.core.files.storage import FileSystemStorage

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['pdf_file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            # You can now process the saved PDF file (e.g., store its path in a database)
            return redirect('success_page')  # Redirect to a success page
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})

def success_page(request):
    return render(request, 'success.html')