import os
from django.conf import settings
from django.shortcuts import render
from .forms import UploadFileForm
from .tasks import process_small_file, process_large_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_size = file.size

            # Save the file temporarily to disk to be processed by Celery
            temp_file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(temp_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Define a size threshold (e.g., 5MB)
            size_threshold = 1 * 1024 * 1024  # 5 MB

            if file_size <= size_threshold:
                # If the file is small, process it as a whole
                process_small_file.delay(temp_file_path, file.name)
            else:
                # If the file is large, process it in chunks
                process_large_file.delay(temp_file_path, file.name, file_size)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
