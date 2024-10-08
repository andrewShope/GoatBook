from django.shortcuts import redirect, render
from lists.models import Item, List

# Create your views here.
def home_page(request):
	return render(request, "home.html")

def view_list(request, list_id):
	our_list = List.objects.get(id=list_id)
	items = Item.objects.filter(list=our_list)
	return render(request, 
		"list.html", 
		{"list": our_list},
	)

def new_list(request):
	nulist = List.objects.create()
	Item.objects.create(text=request.POST["item_text"], list=nulist)
	return redirect(f"/lists/{nulist.id}/")

def add_item(request, list_id):
	Item.objects.create(text=request.POST["item_text"], list=List.objects.get(id=list_id))
	return redirect(f"/lists/{list_id}/")