from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.core.paginator import Paginator
# HttpResponse คือ function สำหรับทำให้โชว์ข้อความหน้าเว็บได้
# Create your views here.


def Home(request):
    products = AllProduct.objects.all().order_by(
        'id').reverse()[:3]
    # AllProduct.objects.all() ดึงข้อมูลมาทั้งหมด
    # [:3] ดึงค่ามาแค่ 3 ตัว
    preorder = AllProduct.objects.filter(quantity__lte=0)
    # quantity__lt = 0 คือ หาค่า quantity ที่ < 0 lt is <
    # quantity__lte = 0 คือ หาค่า quantity ที่ <= 0 lte is <=

    # quantity__gt = 0 คือ หาค่า quantity ที่ > 0 gt is >
    # quantity__gte = 0 คือ หาค่า quantity ที่ >= 0 gte is >=

    context = {
        'AllProduct': products,
        'preorder': preorder
    }
    return render(request, 'myapp/home.html', context)


def profile(request):
    return render(request, 'myapp/profile.html')


def Apple(request):
    return render(request, 'myapp/apple.html')


def Product(request):
    products = AllProduct.objects.all().order_by(
        'id').reverse()  # ดึงข้อมูลมาทั้งหมด
    paginator = Paginator(products, 3)  # 1 หน้าโชว์แค่ 3 ชิ้นเท่านั้น
    page = request.GET.get('page')  # http://localhost:8000/product/?page=2
    products = paginator.get_page(page)  # filter เฉพาะ หน้าของ page นั้นๆ
    context = {'AllProduct': products}
    return render(request, 'myapp/product.html', context)


def AddProduct(request):

    if request.user.profile.userType != 'admin':
        return redirect('home-page')

    if request.method == 'POST' and request.FILES['imgUpload']:
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imgUrl = data.get('imgUrl')
        quantity = data.get('quantity')
        unit = data.get('unit')

        new = AllProduct()
        new.name = name
        new.price = price
        new.detail = detail
        new.imgUrl = imgUrl
        new.quantity = quantity
        new.unit = unit
        ###Save Image###
        file_image = request.FILES['imgUpload']
        file_image_name = request.FILES['imgUpload'].name.replace(' ', '')
        print('FILE_IMAGE:', file_image)
        print('FILE_IMAGE_NAME:', file_image_name)
        fs = FileSystemStorage()
        fileName = fs.save(file_image_name, file_image)
        upload_file_url = fs.url(fileName)
        new.img = upload_file_url[6:]
        ################
        new.save()

    return render(request, 'myapp/addproduct.html')


def Register(request):

    if request.method == 'POST':
        data = request.POST.copy()
        firstName = data.get('first-name')
        lastName = data.get('last-name')
        email = data.get('email')
        password = data.get('password')

        # ยังไม่ใส่ try except เพื่อป้องกันการสมัครซ้ำ
        # + alert ไปหน้าสมัครอีเมลล์นี้เคยสมัครแล้ว
        # สอน คู่กับห้วข้อ reset password

        newUser = User()
        newUser.username = email
        newUser.email = email
        newUser.first_name = firstName
        newUser.last_name = lastName
        newUser.set_password(password)
        newUser.save()

        profile = Profile()
        profile.user = User.objects.get(username=email)
        profile.save()

        user = authenticate(username=email, password=password)
        login(request, user)

    return render(request, 'myapp/register.html')


def AddToCart(request, productId):
    # localhost:8000/addtocart/1
    # {% url 'addtocart-page' product.id %}
    print('Current User : ', request.user)
    username = request.user.username
    user = User.objects.get(username=username)
    check = AllProduct.objects.get(id=productId)

    try:
        # กรณีที่ตังสินค้าซ้ำกัน
        newCart = Cart.objects.get(user=user, productId=str(productId))
        newQty = newCart.quantity + 1
        newCart.quantity = newQty
        calculate = newCart.price * newQty
        newCart.total = calculate
        newCart.save()

        # update จำนวนสินค้าที่มี
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updateQty = Profile.objects.get(user=user)
        updateQty.cartQty = count
        updateQty.save()

        return redirect('product-page')
    except:
        newCart = Cart()
        newCart.user = user
        newCart.productId = productId
        newCart.productName = check.name
        newCart.price = int(check.price)
        newCart.quantity = 1
        calculate = int(check.price) * 1
        newCart.total = calculate
        newCart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updateQty = Profile.objects.get(user=user)
        updateQty.cartQty = count
        updateQty.save()

        return redirect('product-page')


def MyCart(request):
    username = request.user.username
    user = User.objects.get(username=username)

    context = {}

    # ใช้สำหรับการลบ order
    if request.method == 'POST':
        data = request.POST.copy()
        productId = data.get('productId')
        item = Cart.objects.get(user=user, productId=productId)
        item.delete()
        context['status'] = 'delete'

        # Update ค่าที่ถูกลบ
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updateQty = Profile.objects.get(user=user)
        updateQty.cartQty = count
        updateQty.save()

    cart = Cart.objects.filter(user=user).order_by(
        'stamp').reverse()
    count = sum([c.quantity for c in cart])
    total = sum([c.total for c in cart])

    context['cart'] = cart
    context['count'] = count
    context['total'] = total
    return render(request, 'myapp/cart.html', context)


def EditMycart(request):
    # Check User
    username = request.user.username
    user = User.objects.get(username=username)
    context = {}

    if request.method == 'POST':
        data = request.POST.copy()

        if data.get('clear') == 'clear':
            Cart.objects.filter(user=user).delete()

        # editList = [] สร้างลิสต์เพื่อเก็บ id และ quantity ของสินค้า
        editList = []
        # k = key , v = value
        for k, v in data.items():
            if k[:2] == 'pd':  # เช็ค 2 ตัวอักษารแรกว่าเป็น pd หรือไม่
                pid = int(k.split('_')[1])  # แยกคำด้วย '_'
                dt = [pid, int(v)]  # แปลงค่าเป็น int
                editList.append(dt)  # ใส่ค่าตัวแปร dt เข้าไปในตัวแปร editlist

        for ed in editList:
            edit = Cart.objects.get(user=user, productId=ed[0])  # prodcutID
            edit.quantity = ed[1]  # Quantity
            calculate = edit.price * ed[1]
            edit.total = calculate
            edit.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updateQty = Profile.objects.get(user=user)
        updateQty.cartQty = count
        updateQty.save()

        return redirect('cart-page')

    cart = Cart.objects.filter(user=user).order_by(
        'stamp').reverse()
    context['cart'] = cart
    return render(request, 'myapp/editcart.html', context)


def Checkout(request):
    username = request.user.username
    user = User.objects.get(username=username)

    if request.method == 'POST':
        data = request.POST.copy()
        name = data.get('name')
        tel = data.get('tel')
        address = data.get('address')
        shipping = data.get('shipping')
        payment = data.get('payment')
        ps = data.get('ps')
        page = data.get('page')
        if page == 'info':
            context = {}
            context['name'] = name
            context['tel'] = tel
            context['address'] = address
            context['shipping'] = shipping
            context['payment'] = payment
            context['ps'] = ps

            cart = Cart.objects.filter(user=user).order_by('stamp').reverse()
            count = sum([c.quantity for c in cart])
            total = sum([c.total for c in cart])

            context['cart'] = cart
            context['count'] = count
            context['total'] = total

            return render(request, 'myapp/checkout2.html', context)
        if page == 'confirm':
            print('Confirm')
            print(data)
            cart = Cart.objects.filter(user=user)
            mid = str(user.id).zfill(4)  # mid = member id
            dt = datetime.now().strftime('%Y%m%d%H%M%S')  # dt = datatime
            orderId = 'OD' + mid + dt

            for pd in cart:
                order = OrderList()
                order.orderId = orderId
                order.productId = pd.productId
                order.productName = pd.productName
                order.price = pd.price
                order.quantity = pd.quantity
                order.total = pd.total
                order.save()

            # Create Order Pending
            odp = OrderPending()
            odp.orderId = orderId
            odp.user = user
            odp.name = name
            odp.tel = tel
            odp.address = address
            odp.shipping = shipping
            odp.payment = payment
            odp.ps = ps
            odp.save()

            # Clear Cart
            Cart.objects.filter(user=user).delete()
            updateQty = Profile.objects.get(user=user)
            updateQty.cartQty = 0
            updateQty.save()

            return redirect('cart-page')

    return render(request, 'myapp/checkout1.html')


def MyOrderList(request):
    username = request.user.username
    user = User.objects.get(username=username)

    context = {}

    order = OrderPending.objects.filter(user=user).order_by('stamp').reverse()
    '''
        -order
            - orderId : OD000420210722154935
            - user : 
            - name : ผู้รับ
    '''
    for od in order:
        orderId = od.orderId
        orderList = OrderList.objects.filter(orderId=orderId)
        '''
        -orderList
            - object : (1)
                - orderId : OD000420210722154935
                - productId : 12
                - total : 500
            - object : (2)
                - orderId : OD000420210722154935
                - productId : 11
                - total : 500
            - object : (3)
                - orderId : OD000420210722154935
                - productId : 10
                - total : 500
        '''
        total = sum([c.total for c in orderList])
        # total = [500,500,500]
        od.total = total
        # สั่งนับว่า order นี้มีจำนวนเท่าไหร่
        count = sum([c.quantity for c in orderList])

        if od.shipping == 'ems':
            # shipcost = รวมค่าทั้งหมด (หากชิ้นแรก 50 บาท ชิ้นต่อไป 10 บาท)
            shipcost = sum([50 if i == 0 else 10 for i in range(count)])
        else:
            shipcost = sum([30 if i == 0 else 10 for i in range(count)])

        if od.payment == 'cod':
            shipcost += 20
        od.shipcost = shipcost

    context['allorder'] = order

    return render(request, 'myapp/orderlist.html', context)


def AllOrderList(request):
    context = {}

    order = OrderPending.objects.all().order_by('stamp').reverse()

    for od in order:
        orderId = od.orderId
        orderList = OrderList.objects.filter(orderId=orderId)
        total = sum([c.total for c in orderList])
        od.total = total
        count = sum([c.quantity for c in orderList])

        if od.shipping == 'ems':
            # shipcost = รวมค่าทั้งหมด (หากชิ้นแรก 50 บาท ชิ้นต่อไป 10 บาท)
            shipcost = sum([50 if i == 0 else 10 for i in range(count)])
        else:
            shipcost = sum([30 if i == 0 else 10 for i in range(count)])

        if od.payment == 'cod':
            shipcost += 20
        od.shipcost = shipcost

    paginator = Paginator(order, 5)
    page = request.GET.get('page')
    order = paginator.get_page(page)

    context['allorder'] = order

    return render(request, 'myapp/allorderlist.html', context)


def UploadSlip(request, orderId):
    print('Order ID :', orderId)

    if request.method == 'POST' and request.FILES['slip']:
        data = request.POST.copy()
        slipTime = data.get('slipTime')

        update = OrderPending.objects.get(orderId=orderId)
        update.slipTime = slipTime

        file_image = request.FILES['slip']
        file_image_name = request.FILES['slip'].name.replace(' ', '')
        print('FILE_IMAGE:', file_image)
        print('FILE_IMAGE_NAME:', file_image_name)
        fs = FileSystemStorage()
        fileName = fs.save(file_image_name, file_image)
        upload_file_url = fs.url(fileName)
        update.slip = upload_file_url[6:]

        update.save()

    orderList = OrderList.objects.filter(orderId=orderId)
    total = sum([c.total for c in orderList])
    orderDetail = OrderPending.objects.get(orderId=orderId)
    count = sum([c.quantity for c in orderList])

    if orderDetail.shipping == 'ems':
        # shipcost = รวมค่าทั้งหมด (หากชิ้นแรก 50 บาท ชิ้นต่อไป 10 บาท)
        shipcost = sum([50 if i == 0 else 10 for i in range(count)])
    else:
        shipcost = sum([30 if i == 0 else 10 for i in range(count)])

    if orderDetail.payment == 'cod':
        shipcost += 20

    context = {
        'orderId': orderId,
        'total': total,
        'shipcost': shipcost,
        'grandtotal': total + shipcost,
        'oddetail': orderDetail,
        'count': count
    }

    return render(request, 'myapp/uploadslip.html', context)


def UpdatePaid(request, orderId, status):

    if request.user.profile.userType != 'admin':
        return redirect('home-page')

    order = OrderPending.objects.get(orderId=orderId)
    if status == 'confirm':
        order.paid = True
    elif status == 'cancel':
        order.paid = False
    order.save()

    return redirect('allorderlist-page')


def UpdateTracking(request, orderId):

    if request.user.profile.userType != 'admin':
        return redirect('home-page')

    if request.method == 'POST':
        order = OrderPending.objects.get(orderId=orderId)
        data = request.POST.copy()
        trackingNumber = data.get('trackingNumber')
        order.trackingNumber = trackingNumber
        order.save()
        return redirect('allorderlist-page')

    order = OrderPending.objects.get(orderId=orderId)
    orderList = OrderList.objects.filter(orderId=orderId)
    total = sum([c.total for c in orderList])
    order.total = total
    count = sum([c.quantity for c in orderList])

    if order.shipping == 'ems':
        # shipcost = รวมค่าทั้งหมด (หากชิ้นแรก 50 บาท ชิ้นต่อไป 10 บาท)
        shipcost = sum([50 if i == 0 else 10 for i in range(count)])
    else:
        shipcost = sum([30 if i == 0 else 10 for i in range(count)])

    if order.payment == 'cod':
        shipcost += 20

    order.shipcost = shipcost

    context = {
        'orderId': orderId,
        'order': order,
        'orderList': orderList,
        'total': total,
        'count': count
    }

    return render(request, 'myapp/updateTracking.html', context)


def MyOrder(request, orderId):
    username = request.user.username
    user = User.objects.get(username=username)

    order = OrderPending.objects.get(orderId=orderId)

    if user != order.user:
        return redirect('allproduct-page')

    orderList = OrderList.objects.filter(orderId=orderId)
    total = sum([c.total for c in orderList])
    order.total = total
    count = sum([c.quantity for c in orderList])

    if order.shipping == 'ems':
        # shipcost = รวมค่าทั้งหมด (หากชิ้นแรก 50 บาท ชิ้นต่อไป 10 บาท)
        shipcost = sum([50 if i == 0 else 10 for i in range(count)])
    else:
        shipcost = sum([30 if i == 0 else 10 for i in range(count)])

    if order.payment == 'cod':
        shipcost += 20

    order.shipcost = shipcost

    context = {
        'order': order,
        'orderList': orderList,
        'total': total,
        'count': count
    }

    return render(request, 'myapp/myorder.html', context)


# Source Code : https://www.uncle-engineer.com/static/django50/firstweb/myapp/views.py #
