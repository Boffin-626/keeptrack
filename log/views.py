from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required 

from .models import Topic 
from .forms import TopicForm, EntryForm, Entry   

def index(request):
    return render(request, 'log/index.html')

def topics(request): 
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'log/topics.html', context)

def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'log/topic.html', context) 

def new_topic(request):
    #adding a new topic 
    if request.method != 'POST':
        form = TopicForm() 
    
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log:topics')
    
    context = {'form': form}
    return render(request, 'log/new_topic.html', context)
        
        
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
 
    if request.method != 'POST':
        #create a blank form.
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('log:new_entry', topic_id=topic_id)
        
    context = {'topic': topic, 'form': form}
    return render(request, 'log/new_entry.html', context)

def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic 
    
    if request.method != "POST":
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('log:topic', topic_id=topic.id)
    
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'log/edit_entry.html', context)
    
    