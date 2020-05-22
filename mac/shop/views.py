from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate,Media
from django.contrib import messages

from math import ceil
from django.views.decorators.csrf import csrf_exempt
import json
from Paytm import checksum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout


MERCHANT_KEY = '!&2@@54u7nmTcFR%';
# Create your views here.

def index(request):
    # products = Product.objects.all()
    # n= len(products)
    # nslide = n//4 + ceil(n/4 - n//4)
    #
    # param={'products':all_product,'range':range(1,nslide),'no_of_slide':nslide}
    # allprod =[[products,range(1,nslide),nslide],
    #            [products, range(1, nslide), nslide]
    #            ]

    allprod = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides= n//4 +ceil(n/4 - n//4)
        allprod.append([prod,range(1,nslides),nslides])

    param = {'all_prod':allprod}
    return render(request,'shop/index.html',param)

def searchMatch(query,item):
    query =query.lower()
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    query = request.GET.get('search')
    allprod = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        n = len(prod)
        nslides= n//4 +ceil(n/4 - n//4)
        if len(prod) !=0:
            allprod.append([prod,range(1,nslides),nslides])

    param = {'all_prod':allprod,'msg':""}
    if len(allprod) == 0 or len(query)<3:
        param = {'msg':'please enter relevent search'}

    return render(request, 'shop/search.html',param)



def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    thank = False
    if request.method == "POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html',{'thank':thank})

def tracker(request):
    if request.method == "POST":
        order_id = request.POST.get('orderId', '')
        email = request.POST.get('email','')
        try:
            order = Order.objects.filter(order_id=order_id,email=email)
            if len(order) >0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    s1 = item.timestamp.strftime("%d/%m/%Y")
                    updates.append({'text':item.update_desc, 'time':s1})
                    response= json.dumps({'status':'success','updates':updates,'itemsJson':order[0].item_Json},default=str)


                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request,'shop/prodView.html',{'product':product[0]})

def checkout(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') +request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        item_Json = request.POST.get('itemsJson', '')
        total_price = request.POST.get('total_price', '')

        order = Order(name=name, email=email,address=address,city=city,state=state,
        zip_code=zip_code,phone=phone, item_Json=item_Json,total_price=total_price)
        order.save()
        id = order.order_id
        update = OrderUpdate(order_id = id,update_desc="Order has been placed.")
        update.save()
        thank =  True
       # return render(request, 'shop/checkout.html',{'thank':thank,'id':id})
        param_dict = {

            'MID': 'mBuYms99499026878973',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(total_price),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/'

        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum1 = form[i]

    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum1)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def media1(request):
    allMedia = Media.objects.all()[1]

    return render(request,'shop/media1.html',{'allMedia':allMedia})




def handleSignUp(request):
    if request.method == "POST":

        #email as a username
        username = request.POST['email']
        name   = request.POST['name']
        phone   = request.POST['phone']
        address = request.POST.get('address1', '') +request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        pass1   = request.POST['pass1']
        pass2   = request.POST['pass2']

        # if len(username)  > 10:
        #     messages.error(request, 'Username must be under 10 character.')
        #     return redirect('shop')
        
        # if not username.isalnum():
        #     messages.error(request, 'Username should be contain lettes and numerics.')
        #     return redirect('shop')    
        
        if pass1 != pass2:
            messages.error(request, 'Password do not match.')
            return redirect('shop')
            
        user = User.objects.create_user(username,"",pass1)
        user.name = name
        user.address = address
        user.city = city
        user.state = state
        user.zip_code = zip_code

        user.save()
        messages.success(request, 'Your account is created successfuly.')
        return redirect('/')
    else:
        return HttpResponse('404 - Page Not Found') 

def handleLogin(request):
    if request.method == "POST":
        loginusername   = request.POST['loginemail']
        loginpassword   = request.POST['loginpassword']
        user = authenticate(username=loginusername,password=loginpassword)
        print(user)
        print(loginusername)
        print(loginpassword)

        if user is not None: 
            login(request,user)
            messages.success(request, 'You are successfully logged In.')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials.Please try again.')
            return redirect('/')

def handleLogout(request):
    logout(request)
    messages.success(request, 'You are successfully logged Out.')
    return redirect('/')

