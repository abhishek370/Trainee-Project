from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from .models import Mdata, Category, Subcategory, Brand, Type
from django.core.paginator import Paginator
import openpyxl
from more_itertools import locate
import pandas as pd
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
# Create your views here.


class index2(View):
    def get(self, request):
        return render(request, "members/update.html")


def index1(request):
    if "GET" == request.method:
        return render(request, 'members/index.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row+
  
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        dbframe = excel_data.copy()
        dbframe.pop(0)
        error_data = []
        all_fields = [f.name for f in Mdata._meta.get_fields()]
        n = 0
        x = list(filter(lambda x: x.startswith("file"),excel_data[0]))
        y = list(filter(lambda x: x.startswith("file"),all_fields))
        
        f = list(locate(excel_data[0],lambda x: x.startswith("file")))
        t = list(locate(excel_data[0],lambda x: x.startswith("title")))
        t = t[0]
        st = list(locate(excel_data[0],lambda x: x.startswith("subtitle")))
        st = st[0]
        pr = list(locate(excel_data[0],lambda x: x.startswith("price")))
        pr = pr[0]
        de = list(locate(excel_data[0],lambda x: x.startswith("detailes")))
        de = de[0]
        br = list(locate(excel_data[0],lambda x: x.startswith("brand")))
        br = br[0]
        type = list(locate(excel_data[0],lambda x: x.startswith("type")))
        type = type[0]
        cat = list(locate(excel_data[0],lambda x: x.startswith("category")))
        cat = cat[0]
        subcat = list(locate(excel_data[0],lambda x: x.startswith("subcategory")))
        subcat = subcat[0]
        
        for k in dbframe:
            n = n+1 
            # Export data
            
            sql_query = Mdata.objects.values('title','subtitle','price','detailes','brand','type','category','subcategory','file1','file2','file3','file4','file5','file6')

            df = pd.DataFrame(sql_query)
            df.to_excel (r'/home/nteam/Desktop/Django/sample/05_Ecommarce/ecommarce/exported files/exported_data.xlsx', index = False)

            for i in range(f[0],len(k)):
                if excel_data[n][i] != 'None':
                    print(excel_data[n][i])
                    # urllib.request.urlretrieve(excel_data[n][i], "media/images/"+str(n)+"_"+str(i)+".jpg")

            # if k[t] != 'None' and k[st] != 'None' and k[pr] != 'None' and k[de] != 'None':
            #     obj = Mdata.objects.create(title=k[t],subtitle=k[st],price=k[pr],detailes=k[de],brand_id=k[br],type_id=k[type],category_id=k[cat],subcategory_id=k[subcat],file1="images/"+str(n)+"_"+str(f[0])+".jpg",file2="images/"+str(n)+"_"+str(f[1])+".jpg",file3="images/"+str(n)+"_"+str(f[2])+".jpg",file4="images/"+str(n)+"_"+str(f[3])+".jpg",file5="images/"+str(n)+"_"+str(f[4])+".jpg",file6="images/"+str(n)+"_"+str(f[5])+".jpg")        
     
        return render(request, 'members/index.html', {"excel_data": excel_data, "error_data": error_data})


class Home(ListView):
    paginate_by = 6
    model = Mdata
    template_name = "members/products.html"
    
    
    def categorys():
        return Category.objects.all()

    def subcategorys():
        return Subcategory.objects.all().select_related('subcategory')

    def brands():
        return Brand.objects.all()

    def types():
        return Type.objects.all()

    extra_context = {'subcategorys': subcategorys(
    ), 'categorys': categorys(), 'brands': brands(), 'types': types()}

    def post(self, request, *args, **kwargs):
        product = Mdata.objects.all()
        
        pl = [request.POST.get(j.category) for j in Category.objects.all(
        ) if request.POST.get(j.category) != 'None']
        

        if request.POST.get(Category.objects.all()) != None:
            product = Mdata.objects.filter(subcategory__id__in=pl)
          
        if request.POST.get('brands') != 'None':
            product = Mdata.objects.filter(brand=request.POST.get('brands'))

        if request.POST.get('types') != 'None':
            product = Mdata.objects.filter(type=request.POST.get('types'))
        
        a = request.POST.getlist("rating")
        
        if len(a) != 0:
            product = product.filter(rateing__in = a)                
        paginator=Paginator(product,per_page=self.paginate_by)
            
        page = self.request.GET.get('page')

        try:
            product = paginator.page(page)
        except PageNotAnInteger:
            product = paginator.page(1)
        except EmptyPage:
            product = paginator.page(paginator.num_pages)    

        context = {'page_obj': product, 'categorys': Category.objects.all(), 'subcategorys': Subcategory.objects.all(
        ).select_related('subcategory'), 'brands': Brand.objects.all(), 'types': Type.objects.all()}

        return render(request, self.template_name, context)

    def get(self, request,*args, **kwargs):
        

        sort_by = request.GET.get("lop")
        
        if sort_by == "3":
           products = Mdata.objects.order_by("price")
        elif sort_by == "5":
           products = Mdata.objects.order_by("-price")
        else:
            products = Mdata.objects.all()
        
        paginator=Paginator(products,per_page=self.paginate_by)
            
        page = self.request.GET.get('page')

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        
            

        context = {'page_obj': products,'categorys': Category.objects.all(), 'subcategorys': Subcategory.objects.all(
        ).select_related('subcategory'), 'brands': Brand.objects.all(), 'types': Type.objects.all()}
        return render (request, self.template_name,context)    


class PD(View):

    def get(self, request):
        return render(request, "members/product-details.html")


def Productview(request, id):
    product = Mdata.objects.get(id=id)
    return render(request, 'members/product-details.html', {'object': product})

def index(request):
    if request.method == "POST":

        pl = [request.POST.get(j.category) for j in Category.objects.all(
        ) if request.POST.get(j.category) != 'None']
        product = Mdata.objects.filter(subcategory__id__in=pl)
        if request.POST.get('brands'):
            product = product.filter(brand=request.POST.get('brands'))
    return render(request, "members/products.html", {"page_obj": product})


