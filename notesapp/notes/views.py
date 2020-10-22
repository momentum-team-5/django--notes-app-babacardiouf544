from django.shortcuts import render
from django.core.mail import send_mail, mail_admins
from django.contrib.messages import success, error
from .models import Note
from .forms import NoteForm, ContactForm, SearchForm
# Create your views here.
def notes_list(request):
    notes = Note.objects.all()

    return render(request, "notes/notes_list.html")


def notes_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)

    return render(request, "notes/notes_details.html", {"note": note})
    

def notes_add(request):
    if request.method == 'GET':
        form = NoteForm()

    else:
        form = NoteForm(data=request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            return redirect(to='notes_list')

    return render(request, "notes/notes_edit.html", {"form": form}) 

def notes_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "get":
        form = NoteForm(instance=note)

    else:
        form = NoteForm(data=request.post, instance=note)

        if form.isvalid():
            form.save()
            return redirect(to="notes_list")

    return render(reques,"notes/notes_edit.html", {"form": form})

def notes_delete(request, pk):
    note = get_object_404(Note, pk=pk)
    note.delete()
    return redirect(to="notes_list")


def contact_us(request):
    if request.method == "GET":
        form = ContactForm()

    else:
        form = ContactForm(data=request.POST)

        if form.is_valid():
            send_confirmation_to = form.cleaned_data['email']
            message_title = form.cleaned_data['title']
            message_body = form.cleaned_data['body']

            send_mail("Your message was received", "A team member will get back to you within 48 hours.", recipient_list=[send_confirmation_to])
            mail_admins(message_title, message_body, fail_silently=True)

            return redirect(to='notes_list')

    return render(request, "contact_us.html", {"form": form})

def search_notes(request):
    form = SearchForm()

    return render(request, "poems/search.html", {"form": form})